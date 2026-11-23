"""
Phase 2.12 Centralized Evidence Governance, Process-Lifetime Containment, and Manifest Integrity Gateway
Workspace: F:\\FOSSEE internship

Enforces strict write-once evidence governance, prevents historical phase overwrites across all
entrypoints (CLI, test functions, loggers, module globals), eliminates TOCTOU directory swaps,
provides OS-level process containment (assign-before-execute via CREATE_SUSPENDED on Windows,
honest cgroup v2 / PID namespace probing on Linux), and cryptographic external run seals
anchored outside the workspace with HMAC-SHA256 signatures.
"""

import sys
import os
import shutil
import hashlib
import time
import datetime
import subprocess
import json
import uuid
import secrets
import hmac
import threading

# =============================================================================
# 1. Historical Phase Discovery and Protected Directory Inventory
# =============================================================================

HARDCODED_PROTECTED_PHASES = [
    "phase_1d",
    "phase_2_1",
    "phase_2_2",
    "phase_2_3",
    "phase_2_4",
    "phase_2_5",
    "phase_2_6",
    "phase_2_7",
    "phase_2_8",
    "phase_2_9",
    "phase_2_10",
    "phase_2_11",
    "phase_2_12",
    "phase_2_13",
    "phase_2_14",
    "phase_2_15",
    "phase_2_16",
    "phase_2_17",
    "phase_2_baseline",
    "phase_2_repaired",
]

ACTIVE_PHASE = "phase_3"
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

_AUTHORIZED_DIRECTORIES = set()
_SEALED_DIRECTORIES = set()
_CREATE_PROCESS_LOCK = threading.Lock()


def is_symlink_or_junction(path):
    """
    Detects whether a path is a symbolic link or a Windows directory junction / reparse point.
    Standard os.path.islink returns False for directory junctions on Windows; this function
    inspects stat attributes to reliably detect reparse points without elevation.
    """
    if not path:
        return False
    try:
        if os.path.islink(path):
            return True
        if sys.platform == "win32":
            st = os.lstat(path)
            FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            if hasattr(st, "st_file_attributes") and (st.st_file_attributes & FILE_ATTRIBUTE_REPARSE_POINT):
                return True
    except Exception:
        pass
    return False


def get_all_protected_phases():
    """
    Returns an exhaustive list of all historical protected phase directory names.
    Combines hardcoded known phases with dynamic discovery under testing/evidence.
    """
    phases = set(p.lower() for p in HARDCODED_PROTECTED_PHASES)
    # Dynamically scan workspace evidence directory if accessible
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    evidence_root = os.path.join(workspace_root, "testing", "evidence")
    if os.path.exists(evidence_root) and os.path.isdir(evidence_root):
        try:
            for item in os.listdir(evidence_root):
                item_path = os.path.join(evidence_root, item)
                if os.path.isdir(item_path):
                    item_lower = item.lower()
                    if item_lower.startswith("phase_") and item_lower != ACTIVE_PHASE.lower():
                        phases.add(item_lower)
        except Exception:
            pass
    return sorted(list(phases))


PROTECTED_PHASES = get_all_protected_phases()


def is_protected_phase_directory(path):
    """
    Returns True if path points, resolves, traverses, or aliases to any immutable historical phase directory.
    Canonicalizes path via realpath (resolving symlinks and junctions),
    normalizes separators, and checks case-insensitively on Windows.
    Detects path traversal ('..'), case variants (PHASE_2_6), symlink targets, and nested files.
    """
    if not path or not str(path).strip():
        return False
    try:
        raw_str = str(path).strip()
        # Resolve realpath to foil symlinks/junctions pointing to protected folders
        real_p = os.path.realpath(os.path.abspath(raw_str))
        norm_real = os.path.normpath(real_p).replace("\\", "/").lower()
        norm_raw = os.path.normpath(os.path.abspath(raw_str)).replace("\\", "/").lower()

        protected_list = get_all_protected_phases()
        for phase in protected_list:
            pattern = f"/{phase}/"
            suffix = f"/{phase}"
            # Check canonical resolved path
            if pattern in f"/{norm_real}/" or norm_real.endswith(suffix):
                return True
            # Check raw string path before symlink resolution
            if pattern in f"/{norm_raw}/" or norm_raw.endswith(suffix):
                return True
        return False
    except Exception:
        return False


def is_sealed_directory(path):
    """
    Returns True if the directory or file is inside an evidence directory that has already been sealed.
    Persistent across processes by checking:
      1. In-memory sealed directory cache.
      2. Persistent on-disk marker (.sealed) or co-located (manifest_hashes.json + run_seal.json).
      3. External sealed runs registry (trusted_run_seals.json in trust store).
    """
    if not path or not str(path).strip():
        return False
    try:
        raw_str = str(path).strip()
        real_p = os.path.realpath(os.path.abspath(raw_str))
        norm_real = os.path.normpath(real_p).replace("\\", "/").lower()

        # 1. In-memory set
        for sealed in _SEALED_DIRECTORIES:
            if norm_real.startswith(sealed + "/") or norm_real == sealed:
                return True

        # 2. Check disk markers in target directory or any ancestor up to workspace root
        curr = real_p if os.path.isdir(real_p) else os.path.dirname(real_p)
        while curr and os.path.splitdrive(curr)[1] not in ("\\", "/", ""):
            marker = os.path.join(curr, ".sealed")
            if os.path.exists(marker):
                norm_curr = os.path.normpath(curr).replace("\\", "/").lower()
                _SEALED_DIRECTORIES.add(norm_curr)
                return True
            parent = os.path.dirname(curr)
            if parent == curr:
                break
            curr = parent

        # 3. Check persistent ledger in trust directory
        try:
            trust_dir = get_trust_dir(allow_override=True)
            seals_ledger = os.path.join(trust_dir, "trusted_run_seals.json")
            if os.path.exists(seals_ledger):
                with open(seals_ledger, "r", encoding="utf-8") as f:
                    ledger = json.load(f)
                for s in ledger:
                    ed = os.path.normpath(s.get("evidence_dir", "")).replace("\\", "/").lower()
                    if ed and (norm_real.startswith(ed + "/") or norm_real == ed):
                        _SEALED_DIRECTORIES.add(ed)
                        return True
        except Exception:
            pass
    except Exception:
        pass
    return False


def register_sealed_directory(evidence_dir):
    """Registers an evidence directory as sealed and immutable."""
    if evidence_dir:
        norm_real = os.path.normpath(os.path.realpath(os.path.abspath(str(evidence_dir)))).replace("\\", "/").lower()
        _SEALED_DIRECTORIES.add(norm_real)


# =============================================================================
# 2. Centralized Evidence-Writing Gateway (Eliminating Direct-Write Bypasses)
# =============================================================================

def register_authorized_evidence_dir(evidence_dir):
    """Registers an authorized active directory for write gateway validation."""
    if evidence_dir:
        real_path = os.path.realpath(os.path.abspath(str(evidence_dir)))
        _AUTHORIZED_DIRECTORIES.add(os.path.normpath(real_path).replace("\\", "/").lower())


def validate_evidence_directory(evidence_dir, allow_existing=False, allow_protected=False, **kwargs):
    """
    Validates target evidence directory against accidental overwrites and historical phase corruption.
    Fails closed if directory is missing, empty, or attempts to target historical phases.
    Default allow_existing=False rejects reuse of non-empty directories unless explicitly authorized.
    """
    if not evidence_dir or not str(evidence_dir).strip():
        raise ValueError(
            "CRITICAL EVIDENCE INTEGRITY VIOLATION: --evidence-dir is required and cannot be empty. "
            "Refusing to run with implicit default directory."
        )

    evidence_dir = str(evidence_dir).strip()
    real_path = os.path.realpath(os.path.abspath(evidence_dir))
    norm_path = os.path.normpath(real_path).replace("\\", "/")
    norm_lower = norm_path.lower()

    # 1. Protect historical phases (resolves symlinks, junctions, case-insensitive, traversal)
    if not allow_protected and is_protected_phase_directory(evidence_dir):
        raise PermissionError(
            f"CRITICAL EVIDENCE OVERWRITE BLOCKED: Target directory '{evidence_dir}' (resolves to '{real_path}') "
            f"matches a protected historical phase. Historical evidence is immutable. "
            f"Output to an official active phase or scratch directory."
        )

    # 2. Refuse sealed directories
    if is_sealed_directory(real_path):
        raise PermissionError(
            f"CRITICAL EVIDENCE RE-USE REFUSAL: Target directory '{evidence_dir}' has already been sealed. "
            f"Sealed runs cannot be overwritten or extended."
        )

    # 3. Prevent reusing populated evidence directory by default
    allow_pop = allow_existing or kwargs.get("allow_populated", False)
    if os.path.exists(real_path) and os.path.isdir(real_path) and not allow_pop:
        entries = [e for e in os.listdir(real_path) if e not in (".git", "__pycache__")]
        if entries:
            raise FileExistsError(
                f"CRITICAL EVIDENCE PROTECTION: Target evidence directory '{evidence_dir}' already exists "
                f"and contains {len(entries)} items. Refusing to overwrite existing evidence. "
                f"Specify a clean target directory or pass explicit allow_existing=True."
            )

    os.makedirs(real_path, exist_ok=True)
    register_authorized_evidence_dir(norm_path)
    return norm_path


def check_write_permission(filepath):
    """
    Validates that a file write operation does not violate evidence governance.
    Canonicalizes path, verifies it does not target protected phases, checks traversal,
    prohibits writing to application source code and repository roots, and enforces
    authorized directory allowlists.
    Raises PermissionError or ValueError on violation.
    """
    if not filepath or not str(filepath).strip():
        raise ValueError("CRITICAL GATEWAY REFUSAL: Filepath cannot be empty.")

    filepath_str = str(filepath).strip()
    abs_path = os.path.abspath(filepath_str)
    real_path = os.path.realpath(abs_path)
    norm_real = os.path.normpath(real_path).replace("\\", "/").lower()

    # Check 1: Traversal detection
    norm_tokens = [t.lower() for t in filepath_str.replace("\\", "/").split("/")]
    if ".." in norm_tokens:
        # Check if resolved path is protected
        if is_protected_phase_directory(real_path):
            raise PermissionError(
                f"CRITICAL WRITE GATEWAY REFUSAL: Traversal '{filepath_str}' resolves to protected phase '{real_path}'."
            )

    # Check 2: Protect historical phases
    if is_protected_phase_directory(filepath_str) or is_protected_phase_directory(real_path):
        raise PermissionError(
            f"CRITICAL WRITE GATEWAY REFUSAL: Write target '{filepath_str}' (resolves to '{real_path}') "
            f"is inside an immutable protected historical phase. Direct writes and bypasses are strictly forbidden."
        )

    # Check 3: Refuse writes inside sealed directories
    if is_sealed_directory(real_path):
        raise PermissionError(
            f"CRITICAL WRITE GATEWAY REFUSAL: Target '{real_path}' is inside a sealed immutable directory."
        )

    # Check 4: Refuse writes into application source tree
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    src_repo_dir = os.path.normpath(os.path.realpath(os.path.join(workspace_root, "source", "OsdagBridge"))).replace("\\", "/").lower()
    if norm_real.startswith(src_repo_dir + "/") or norm_real == src_repo_dir:
        raise PermissionError(
            f"CRITICAL WRITE GATEWAY REFUSAL: Target '{filepath_str}' (resolves to '{real_path}') "
            f"is inside application source tree. Direct test writes to application code are strictly forbidden."
        )

    # Check 5: Refuse writes directly into workspace root
    norm_ws = os.path.normpath(os.path.realpath(workspace_root)).replace("\\", "/").lower()
    if os.path.dirname(norm_real) == norm_ws or norm_real == norm_ws:
        raise PermissionError(
            f"CRITICAL WRITE GATEWAY REFUSAL: Target '{filepath_str}' (resolves to '{real_path}') "
            f"is directly in workspace root. Direct writes to workspace root are strictly forbidden."
        )

    # Check 6: Refuse writes into .git metadata
    if norm_real.startswith(norm_ws + "/.git/") or norm_real == norm_ws + "/.git":
        raise PermissionError(
            f"CRITICAL WRITE GATEWAY REFUSAL: Target '{filepath_str}' is inside .git metadata."
        )

    # Check 7: Refuse writes into reports directory from test execution
    reports_dir = os.path.normpath(os.path.realpath(os.path.join(workspace_root, "reports"))).replace("\\", "/").lower()
    if norm_real.startswith(reports_dir + "/") or norm_real == reports_dir:
        raise PermissionError(
            f"CRITICAL WRITE GATEWAY REFUSAL: Target '{filepath_str}' (resolves to '{real_path}') "
            f"is inside reports directory. Test execution cannot write to audit reports."
        )

    # Check 8: Enforce authorized directory allowlist if populated
    if _AUTHORIZED_DIRECTORIES:
        is_authorized = False
        for auth_dir in _AUTHORIZED_DIRECTORIES:
            if norm_real.startswith(auth_dir + "/") or norm_real == auth_dir:
                is_authorized = True
                break
        if not is_authorized:
            # Allow writes to temp directories (for scratch / test runners)
            temp_dir = os.path.normpath(os.path.realpath(os.environ.get("TEMP", os.environ.get("TMP", "/tmp")))).replace("\\", "/").lower()
            if not norm_real.startswith(temp_dir + "/"):
                raise PermissionError(
                    f"CRITICAL WRITE GATEWAY REFUSAL: Target '{filepath_str}' (resolves to '{real_path}') "
                    f"is not within any authorized evidence directory: {sorted(list(_AUTHORIZED_DIRECTORIES))}"
                )

    # Check 9: TOCTOU Symlink / Junction detection on parent directory
    parent = os.path.dirname(abs_path)
    if parent:
        real_parent = os.path.realpath(parent)
        if is_protected_phase_directory(real_parent) or is_sealed_directory(real_parent):
            raise PermissionError(
                f"CRITICAL WRITE GATEWAY REFUSAL: Parent directory '{parent}' resolves to protected/sealed "
                f"path '{real_parent}'. Symlink/junction traversal detected."
            )
        if is_symlink_or_junction(parent):
            raise PermissionError(
                f"CRITICAL WRITE GATEWAY REFUSAL: Parent directory '{parent}' is an unverified symlink or junction."
            )

    return real_path


class SafeFileWrapper:
    """
    Context manager wrapper providing non-destructive TOCTOU defense.
    Never truncates or modifies the target file in-place before safety is established.
    Writes exclusively to a temporary staging file in the verified directory and
    commits via atomic replace only after re-verifying canonical directory and target safety.
    """
    def __init__(self, filepath, mode="w", encoding="utf-8", **kwargs):
        self.filepath = filepath
        self.mode = mode
        self.encoding = encoding
        self.kwargs = kwargs
        self.real_path = check_write_permission(filepath)
        self.target_dir = os.path.dirname(self.real_path)
        self.orig_real_dir = os.path.realpath(self.target_dir)

        if not os.path.exists(self.orig_real_dir):
            os.makedirs(self.orig_real_dir, exist_ok=True)
        if is_symlink_or_junction(self.target_dir):
            raise PermissionError(f"CRITICAL TOCTOU VIOLATION: Target directory '{self.target_dir}' is a symlink or junction.")
        if os.path.exists(self.real_path) and is_symlink_or_junction(self.real_path):
            raise PermissionError(f"CRITICAL TOCTOU VIOLATION: Destination file '{self.real_path}' is a symlink or junction.")
        if is_sealed_directory(self.real_path):
            raise PermissionError(f"CRITICAL GATEWAY REFUSAL: Target directory for '{self.real_path}' is sealed.")

        self._file = None
        self.staging_path = None

    def __enter__(self):
        # Pre-open directory verification
        curr_real_dir = os.path.realpath(self.target_dir)
        if curr_real_dir != self.orig_real_dir or is_protected_phase_directory(curr_real_dir) or is_symlink_or_junction(self.target_dir):
            raise PermissionError(f"CRITICAL TOCTOU VIOLATION: Target directory '{self.target_dir}' was swapped before open.")

        # Create secure staging file in verified target directory
        staging_name = f".{os.path.basename(self.real_path)}.tmp_{uuid.uuid4().hex}"
        self.staging_path = os.path.join(curr_real_dir, staging_name)

        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_BINARY") and "b" in self.mode:
            flags |= os.O_BINARY

        fd = os.open(self.staging_path, flags, 0o600)
        if "b" in self.mode:
            self._file = open(fd, self.mode, **self.kwargs)
        else:
            self._file = open(fd, self.mode, encoding=self.encoding, **self.kwargs)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._file and not self._file.closed:
                self._file.flush()
                self._file.close()
        except Exception:
            pass

        if exc_type is not None:
            # If write raised an exception, clean staging file and leave destination completely untouched
            if self.staging_path and os.path.exists(self.staging_path):
                try:
                    os.remove(self.staging_path)
                except Exception:
                    pass
            return False

        # Post-write TOCTOU re-validation BEFORE committing to final destination
        curr_real_dir = os.path.realpath(self.target_dir)
        if curr_real_dir != self.orig_real_dir or is_protected_phase_directory(curr_real_dir) or is_symlink_or_junction(self.target_dir):
            if self.staging_path and os.path.exists(self.staging_path):
                os.remove(self.staging_path)
            raise PermissionError(
                f"CRITICAL TOCTOU VIOLATION: Target directory was redirected to protected target '{curr_real_dir}'."
            )

        dest_real = os.path.realpath(self.real_path)
        if is_protected_phase_directory(dest_real) or is_symlink_or_junction(self.real_path) or is_sealed_directory(dest_real):
            if self.staging_path and os.path.exists(self.staging_path):
                os.remove(self.staging_path)
            raise PermissionError(
                f"CRITICAL TOCTOU VIOLATION: Destination path was redirected to protected target '{dest_real}'."
            )

        # Atomically replace destination with verified staging file (destination is never truncated on failure)
        os.replace(self.staging_path, self.real_path)
        return False


def safe_open_evidence(filepath, mode="w", encoding="utf-8", **kwargs):
    """
    Centralized Gateway for opening evidence files.
    All test functions, loggers, helper functions, and runners must use this gateway.
    Direct calls cannot bypass write-time realpath validation or cause TOCTOU truncation.
    """
    return SafeFileWrapper(filepath, mode=mode, encoding=encoding, **kwargs)


def safe_write_evidence(filepath, content, encoding="utf-8"):
    """Atomically and securely writes content through the centralized write gateway."""
    with safe_open_evidence(filepath, mode="w", encoding=encoding) as f:
        f.write(content)


def safe_copy_evidence(src, dst):
    """Safely copies a file through the centralized write gateway, immune to TOCTOU truncation."""
    with open(src, "rb") as f_src:
        with safe_open_evidence(dst, "wb") as f_dst:
            shutil.copyfileobj(f_src, f_dst)


# =============================================================================
# 3. OS-Level Process Containment (Windows Job Object & POSIX Cgroup/Namespace)
# =============================================================================

class ContainedPopen(subprocess.Popen):
    """
    Subprocess.Popen subclass enforcing assign-before-execute on Windows via CREATE_SUSPENDED,
    with thread-safe hooking of _winapi.CreateProcess.
    """
    def __init__(self, *args, job_container=None, **kwargs):
        self._job_container = job_container
        super().__init__(*args, **kwargs)

    def _execute_child(self, args, executable, preexec_fn, close_fds,
                       pass_fds, cwd, env,
                       startupinfo, creationflags, shell,
                       p2cread, p2cwrite,
                       c2pread, c2pwrite,
                       errread, errwrite,
                       unused_restore_signals,
                       unused_gid, unused_gids, unused_uid,
                       unused_umask,
                       unused_start_new_session, unused_process_group):
        if sys.platform == "win32" and self._job_container and self._job_container.hJob:
            import _winapi
            import ctypes

            CREATE_SUSPENDED = 0x00000004
            creationflags |= CREATE_SUSPENDED

            real_create_process = _winapi.CreateProcess

            def hooked_create_process(*cp_args, **cp_kwargs):
                hp, ht, pid, tid = real_create_process(*cp_args, **cp_kwargs)
                # Assign to Job Object BEFORE resuming thread!
                assigned = self._job_container.kernel32.AssignProcessToJobObject(
                    self._job_container.hJob,
                    hp
                )
                if not assigned:
                    err = ctypes.GetLastError()
                    _winapi.TerminateProcess(hp, 1)
                    _winapi.CloseHandle(hp)
                    _winapi.CloseHandle(ht)
                    raise PermissionError(
                        f"CRITICAL CONTAINMENT FAILURE: Could not assign suspended process {pid} to Job Object (WinError {err})"
                    )

                # Resume primary thread now that child is safely bound to Job Object
                prev = self._job_container.kernel32.ResumeThread(ht)
                if prev == 0xFFFFFFFF:
                    err = ctypes.GetLastError()
                    _winapi.TerminateProcess(hp, 1)
                    _winapi.CloseHandle(hp)
                    _winapi.CloseHandle(ht)
                    raise RuntimeError(
                        f"CRITICAL CONTAINMENT FAILURE: Could not resume primary thread for process {pid} (WinError {err})"
                    )
                return hp, ht, pid, tid

            with _CREATE_PROCESS_LOCK:
                try:
                    _winapi.CreateProcess = hooked_create_process
                    super()._execute_child(
                        args, executable, preexec_fn, close_fds,
                        pass_fds, cwd, env,
                        startupinfo, creationflags, shell,
                        p2cread, p2cwrite,
                        c2pread, c2pwrite,
                        errread, errwrite,
                        unused_restore_signals,
                        unused_gid, unused_gids, unused_uid,
                        unused_umask,
                        unused_start_new_session, unused_process_group
                    )
                finally:
                    _winapi.CreateProcess = real_create_process
        else:
            super()._execute_child(
                args, executable, preexec_fn, close_fds,
                pass_fds, cwd, env,
                startupinfo, creationflags, shell,
                p2cread, p2cwrite,
                c2pread, c2pwrite,
                errread, errwrite,
                unused_restore_signals,
                unused_gid, unused_gids, unused_uid,
                unused_umask,
                unused_start_new_session, unused_process_group
            )


class ProcessLifetimeJob:
    """
    OS-level process containment boundary.
    On Windows: uses Win32 Job Object with JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE, disallows breakaway,
    and assigns child processes in a SUSPENDED state before execution begins.
    On POSIX: checks for cgroup v2 / PID namespace support; if neither is available, honestly
    reports containment as unavailable (BLOCKED) without claiming false process-group cleanup.
    """
    def __init__(self):
        self.is_windows = (sys.platform == "win32")
        self.hJob = None
        self.cgroup_path = None
        self.is_contained = False
        self.containment_type = None
        self._procs = []

        if self.is_windows:
            import ctypes
            from ctypes import wintypes
            self.kernel32 = ctypes.windll.kernel32

            self.kernel32.CreateJobObjectW.restype = wintypes.HANDLE
            self.kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
            self.kernel32.SetInformationJobObject.restype = wintypes.BOOL
            self.kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
            self.kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
            self.kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
            self.kernel32.QueryInformationJobObject.restype = wintypes.BOOL
            self.kernel32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD]
            self.kernel32.ResumeThread.restype = wintypes.DWORD
            self.kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
            self.kernel32.TerminateJobObject.restype = wintypes.BOOL
            self.kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
            self.kernel32.CloseHandle.restype = wintypes.BOOL
            self.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]

            JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
            JobObjectExtendedLimitInformation = 9

            class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
                _fields_ = [
                    ("PerProcessUserTimeLimit", ctypes.c_int64),
                    ("PerJobUserTimeLimit", ctypes.c_int64),
                    ("LimitFlags", wintypes.DWORD),
                    ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t),
                    ("ActiveProcessLimit", wintypes.DWORD),
                    ("Affinity", ctypes.c_size_t),
                    ("PriorityClass", wintypes.DWORD),
                    ("SchedulingClass", wintypes.DWORD),
                ]

            class IO_COUNTERS(ctypes.Structure):
                _fields_ = [
                    ("ReadOperationCount", ctypes.c_ulonglong),
                    ("WriteOperationCount", ctypes.c_ulonglong),
                    ("OtherOperationCount", ctypes.c_ulonglong),
                    ("ReadTransferCount", ctypes.c_ulonglong),
                    ("WriteTransferCount", ctypes.c_ulonglong),
                    ("OtherTransferCount", ctypes.c_ulonglong),
                ]

            class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
                _fields_ = [
                    ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
                    ("IoCounters", IO_COUNTERS),
                    ("ProcessMemoryLimit", ctypes.c_size_t),
                    ("JobMemoryLimit", ctypes.c_size_t),
                    ("PeakProcessMemoryLimit", ctypes.c_size_t),
                    ("PeakJobMemoryLimit", ctypes.c_size_t),
                ]

            self.hJob = self.kernel32.CreateJobObjectW(None, None)
            if not self.hJob:
                raise ctypes.WinError()

            ext_limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            # KILL_ON_JOB_CLOSE without breakaway flags
            ext_limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            success = self.kernel32.SetInformationJobObject(
                self.hJob,
                JobObjectExtendedLimitInformation,
                ctypes.byref(ext_limits),
                ctypes.sizeof(ext_limits)
            )
            if not success:
                self.kernel32.CloseHandle(self.hJob)
                self.hJob = None
                raise ctypes.WinError()

            self.is_contained = True
            self.containment_type = "Win32_JobObject_Suspended"
        else:
            # POSIX: Genuine cgroup v2 verification (rejects tmpfs mounts on root/CI hosts)
            is_cgroup2 = False
            if os.path.exists("/proc/mounts"):
                try:
                    with open("/proc/mounts", "r") as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) >= 3 and parts[1] == "/sys/fs/cgroup" and parts[2] == "cgroup2":
                                is_cgroup2 = True
                                break
                except Exception:
                    pass

            cgroup_v2_root = "/sys/fs/cgroup"
            controllers_file = os.path.join(cgroup_v2_root, "cgroup.controllers")
            has_controllers = os.path.exists(controllers_file)

            # Reject if /sys/fs/cgroup is tmpfs, cgroup v1, or missing genuine cgroup.controllers
            if is_cgroup2 and has_controllers and os.access(cgroup_v2_root, os.W_OK):
                try:
                    cg_name = f"osdagbridge_cg_{uuid.uuid4().hex[:8]}"
                    cg_path = os.path.join(cgroup_v2_root, cg_name)
                    os.mkdir(cg_path)
                    procs_file = os.path.join(cg_path, "cgroup.procs")
                    # If this is genuine cgroup2, the kernel automatically provides cgroup.procs
                    if os.path.exists(procs_file):
                        self.cgroup_path = cg_path
                        self.is_contained = True
                        self.containment_type = "cgroup_v2"
                    else:
                        # Plain tmpfs created an ordinary directory; not genuine cgroup2
                        try:
                            os.rmdir(cg_path)
                        except Exception:
                            pass
                        self.is_contained = False
                        self.containment_type = None
                except Exception:
                    self.is_contained = False
                    self.containment_type = None
            else:
                # If genuine cgroup v2 is not available without root/delegation,
                # explicitly set is_contained = False (Audit directive §1, §10.1).
                self.is_contained = False
                self.containment_type = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

    def spawn(self, cmd_args, **kwargs):
        """Spawns a process contained inside the boundary from creation."""
        if self.is_windows and self.hJob:
            proc = ContainedPopen(cmd_args, job_container=self, **kwargs)
            self._procs.append(proc)
            return proc
        elif not self.is_windows and self.is_contained and self.cgroup_path:
            # cgroup v2 containment: join child BEFORE exec using preexec_fn
            cg_procs = os.path.join(self.cgroup_path, "cgroup.procs")
            def _preexec_join_cgroup():
                try:
                    with open(cg_procs, "w") as f_cg:
                        f_cg.write(str(os.getpid()))
                except Exception as e:
                    raise RuntimeError(f"CRITICAL: Failed to join child process to cgroup: {e}")

            kwargs["preexec_fn"] = _preexec_join_cgroup
            proc = subprocess.Popen(cmd_args, **kwargs)
            self._procs.append(proc)
            return proc
        else:
            # Fallback uncontained on Linux (marked BLOCKED in tests)
            proc = subprocess.Popen(cmd_args, **kwargs)
            self._procs.append(proc)
            return proc

    def get_process_count(self):
        """Returns the number of active processes currently in the containment boundary."""
        if self.is_windows and self.hJob:
            import ctypes
            from ctypes import wintypes

            class JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
                _fields_ = [
                    ("TotalUserTime", ctypes.c_int64),
                    ("TotalKernelTime", ctypes.c_int64),
                    ("ThisPeriodTotalUserTime", ctypes.c_int64),
                    ("ThisPeriodTotalKernelTime", ctypes.c_int64),
                    ("TotalPageFaultCount", wintypes.DWORD),
                    ("TotalProcesses", wintypes.DWORD),
                    ("ActiveProcesses", wintypes.DWORD),
                    ("TotalTerminatedProcesses", wintypes.DWORD),
                ]

            info = JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
            res = self.kernel32.QueryInformationJobObject(
                self.hJob,
                1,  # JobObjectBasicAccountingInformation
                ctypes.byref(info),
                ctypes.sizeof(info),
                None
            )
            if res:
                return int(info.ActiveProcesses)
            return 0
        elif not self.is_windows and self.is_contained and self.cgroup_path:
            procs_file = os.path.join(self.cgroup_path, "cgroup.procs")
            if os.path.exists(procs_file):
                try:
                    with open(procs_file, "r") as f:
                        lines = [line.strip() for line in f if line.strip()]
                    return len(lines)
                except Exception:
                    return 0
            return 0
        return 0

    def wait_for_job_completion(self, timeout_sec=5.0, poll_interval_sec=0.2):
        """
        Polls until all active processes in the Job have terminated.
        Returns True if ActiveProcesses reached 0 within timeout, False otherwise.
        """
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            if self.get_process_count() == 0:
                return True
            time.sleep(poll_interval_sec)
        return (self.get_process_count() == 0)

    def terminate(self):
        """Terminates all processes in the job/cgroup and cleans up resources."""
        if self.is_windows and self.hJob:
            self.kernel32.TerminateJobObject(self.hJob, 1)
            self.kernel32.CloseHandle(self.hJob)
            self.hJob = None
        elif not self.is_windows and self.is_contained and self.cgroup_path:
            kill_file = os.path.join(self.cgroup_path, "cgroup.kill")
            if os.path.exists(kill_file):
                try:
                    with open(kill_file, "w") as f:
                        f.write("1")
                except Exception:
                    pass
            try:
                os.rmdir(self.cgroup_path)
            except Exception:
                pass
            self.cgroup_path = None


# =============================================================================
# 4. Manifest Integrity and External Cryptographic Seal (HMAC-SHA256)
# =============================================================================

def sha256_file(filepath):
    """Compute SHA-256 hash of a file."""
    if not filepath or not os.path.exists(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


PINNED_TRUST_DIR = (
    os.path.realpath(os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), ".osdagbridge_trust"))
    if sys.platform == "win32" else
    os.path.realpath(os.path.join(os.path.expanduser("~"), ".osdagbridge_trust"))
)


def get_trust_dir(allow_override=False):
    """
    Returns the trusted verification anchor directory located OUTSIDE the project workspace.
    By default, returns the cryptographically pinned trust store.
    Overrides via OSDAGBRIDGE_TRUST_DIR are permitted only when explicitly allowed
    (e.g., during isolated test execution via OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE=1).
    """
    trust_env = os.environ.get("OSDAGBRIDGE_TRUST_DIR")
    if trust_env and str(trust_env).strip():
        is_test_override_allowed = (os.environ.get("OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE") == "1") or allow_override
        if not is_test_override_allowed:
            raise PermissionError(
                f"CRITICAL TRUST PINNING VIOLATION: OSDAGBRIDGE_TRUST_DIR override '{trust_env}' is active, "
                f"but unpinned trust directories are disallowed in production mode. "
                f"Production verification must use the pinned trust anchor: {PINNED_TRUST_DIR}"
            )
        return os.path.realpath(os.path.abspath(str(trust_env).strip()))
    return PINNED_TRUST_DIR


def get_or_create_signing_key(trust_dir=None, allow_override=False):
    """
    Retrieves or generates a 32-byte cryptographically secure signing key
    stored outside the project workspace with restricted permissions.
    """
    trust_dir = trust_dir or get_trust_dir(allow_override=allow_override)
    os.makedirs(trust_dir, exist_ok=True)
    key_file = os.path.join(trust_dir, "seal_signing_key.bin")
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
        if len(key) >= 32:
            return key

    key = secrets.token_bytes(32)
    # Write key with restricted permissions
    if hasattr(os, "O_CREAT") and hasattr(os, "O_WRONLY"):
        fd = os.open(key_file, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
        with open(fd, "wb") as f:
            f.write(key)
    else:
        with open(key_file, "wb") as f:
            f.write(key)
    return key


def compute_seal_signature(key, canonical_str):
    """Computes HMAC-SHA256 signature for a canonical seal record."""
    return hmac.new(key, canonical_str.encode("utf-8"), hashlib.sha256).hexdigest()


def generate_and_seal_manifest(evidence_dir, runner_id="baseline_runner", phase_label="Phase 2.13", trust_dir=None, allow_trust_override=False):
    """
    Scans evidence_dir, generates manifest_hashes.json, computes manifest SHA-256,
    digitally signs the run record with HMAC-SHA256, stores the trusted seal
    in an external registry outside the project workspace, writes the persistent
    .sealed marker, and applies filesystem read-only attributes (accidental-overwrite deterrent).
    Fails if evidence_dir has already been sealed.
    """
    evidence_dir = os.path.realpath(os.path.abspath(evidence_dir))
    norm_evidence_dir = os.path.normpath(evidence_dir).replace("\\", "/")

    # Refuse re-sealing
    if is_sealed_directory(evidence_dir):
        raise PermissionError(f"CRITICAL RE-SEAL REFUSAL: Evidence directory '{evidence_dir}' has already been sealed.")

    trust_dir = trust_dir or get_trust_dir(allow_override=allow_trust_override)
    signing_key = get_or_create_signing_key(trust_dir, allow_override=allow_trust_override)
    seals_ledger = os.path.join(trust_dir, "trusted_run_seals.json")

    # Check if this evidence_dir is already in trusted ledger
    if os.path.exists(seals_ledger):
        try:
            with open(seals_ledger, "r", encoding="utf-8") as f:
                existing_seals = json.load(f)
            for s in existing_seals:
                if s.get("evidence_dir", "").lower() == norm_evidence_dir.lower():
                    raise PermissionError(f"CRITICAL RE-SEAL REFUSAL: Directory '{evidence_dir}' already sealed in {seals_ledger}.")
        except PermissionError:
            raise
        except Exception:
            existing_seals = []
    else:
        existing_seals = []

    files_list = []
    total_bytes = 0

    for root, dirs, files in os.walk(evidence_dir):
        for file in sorted(files):
            if file in ("manifest_hashes.json", "run_seal.json", ".sealed"):
                continue
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, evidence_dir).replace("\\", "/")
            fsize = os.path.getsize(full_p)
            total_bytes += fsize
            files_list.append({
                "path": rel_p,
                "size_bytes": fsize,
                "sha256": sha256_file(full_p)
            })

    run_uuid = str(uuid.uuid4())
    timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    manifest_data = {
        "phase": phase_label,
        "runner_id": runner_id,
        "run_uuid": run_uuid,
        "timestamp_utc": timestamp_utc,
        "total_files": len(files_list),
        "total_bytes": total_bytes,
        "files": files_list
    }

    manifest_json_path = os.path.join(evidence_dir, "manifest_hashes.json")
    with safe_open_evidence(manifest_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    manifest_hash = sha256_file(manifest_json_path)

    # Canonical string to sign
    canonical_str = (
        f"RUN_ID={run_uuid}\n"
        f"EVIDENCE_DIR={norm_evidence_dir}\n"
        f"MANIFEST_SHA256={manifest_hash}\n"
        f"TOTAL_FILES={len(files_list)}\n"
        f"TOTAL_BYTES={total_bytes}\n"
        f"TIMESTAMP={timestamp_utc}\n"
        f"RUNNER_ID={runner_id}"
    )
    sig = compute_seal_signature(signing_key, canonical_str)

    seal_record = {
        "run_uuid": run_uuid,
        "phase_label": phase_label,
        "runner_id": runner_id,
        "timestamp_utc": timestamp_utc,
        "evidence_dir": norm_evidence_dir,
        "total_files": len(files_list),
        "total_bytes": total_bytes,
        "manifest_path": manifest_json_path.replace("\\", "/"),
        "manifest_sha256": manifest_hash,
        "signature": sig
    }

    # 1. Write run_seal.json into evidence dir
    run_seal_path = os.path.join(evidence_dir, "run_seal.json")
    with safe_open_evidence(run_seal_path, "w", encoding="utf-8") as f:
        json.dump(seal_record, f, indent=2)

    # 2. Write persistent .sealed marker into evidence dir
    sealed_marker_path = os.path.join(evidence_dir, ".sealed")
    with safe_open_evidence(sealed_marker_path, "w", encoding="utf-8") as f:
        f.write(f"SEALED:{run_uuid}:{timestamp_utc}\n")

    # 3. Record in trusted external store
    existing_seals.append(seal_record)
    with open(seals_ledger, "w", encoding="utf-8") as f:
        json.dump(existing_seals, f, indent=2)

    # Apply OS-level read-only permissions to all files in sealed directory
    import stat
    for root, dirs, files in os.walk(evidence_dir):
        for file in files:
            fp = os.path.join(root, file)
            try:
                os.chmod(fp, stat.S_IREAD)
            except Exception:
                pass

    # Register directory as sealed and immutable
    register_sealed_directory(evidence_dir)

    return manifest_data, seal_record


def verify_manifest_integrity(evidence_dir, trust_dir=None, allow_trust_override=False):
    """
    Fails closed if the external seal is missing, corrupted, forged, or inapplicable.
    Verifies:
      1. Trust store and signing key are present and readable.
      2. Trusted run seal exists and HMAC-SHA256 signature is valid.
      3. Manifest SHA-256 matches seal record.
      4. Disk walk: checks all files, flags unlisted files (S8), missing files (S9),
         and hash/size mismatches (S1-S3).
    Returns (success, mismatches, details).
    """
    evidence_dir = os.path.realpath(os.path.abspath(evidence_dir))
    norm_evidence_dir = os.path.normpath(evidence_dir).replace("\\", "/")
    manifest_path = os.path.join(evidence_dir, "manifest_hashes.json")

    if not os.path.exists(manifest_path):
        return False, ["MISSING_MANIFEST"], f"Manifest file not found: {manifest_path}"

    trust_dir = trust_dir or get_trust_dir(allow_override=allow_trust_override)
    key_file = os.path.join(trust_dir, "seal_signing_key.bin")
    seals_ledger = os.path.join(trust_dir, "trusted_run_seals.json")

    # Fail closed on missing trust store or key
    if not os.path.exists(key_file):
        return False, ["TRUST_ANCHOR_MISSING"], f"Trust anchor signing key not found in {trust_dir}."
    try:
        with open(key_file, "rb") as f:
            key = f.read()
    except Exception as e:
        return False, ["KEY_INACCESSIBLE"], f"Could not read signing key: {e}"

    # Fail closed on missing or unparseable seal ledger
    if not os.path.exists(seals_ledger):
        return False, ["SEAL_LEDGER_MISSING"], f"Trusted seal ledger not found in {trust_dir}."
    try:
        with open(seals_ledger, "r", encoding="utf-8") as f:
            seals = json.load(f)
    except Exception as e:
        return False, ["SEAL_LEDGER_CORRUPT"], f"Could not parse trusted seal ledger: {e}"

    # Locate seal record for this exact canonical evidence_dir
    matching_seal = None
    for s in reversed(seals):
        if s.get("evidence_dir", "").lower() == norm_evidence_dir.lower():
            matching_seal = s
            break

    if not matching_seal:
        return False, ["NO_SEAL_RECORD"], f"No trusted run seal found for directory '{norm_evidence_dir}'. Unsealed evidence is rejected."

    # Verify HMAC signature
    canonical_str = (
        f"RUN_ID={matching_seal.get('run_uuid')}\n"
        f"EVIDENCE_DIR={matching_seal.get('evidence_dir')}\n"
        f"MANIFEST_SHA256={matching_seal.get('manifest_sha256')}\n"
        f"TOTAL_FILES={matching_seal.get('total_files')}\n"
        f"TOTAL_BYTES={matching_seal.get('total_bytes')}\n"
        f"TIMESTAMP={matching_seal.get('timestamp_utc')}\n"
        f"RUNNER_ID={matching_seal.get('runner_id')}"
    )
    expected_sig = compute_seal_signature(key, canonical_str)
    if matching_seal.get("signature") != expected_sig:
        return False, ["FORGED_SEAL_SIGNATURE"], "Cryptographic seal signature verification failed! Seal record was forged or tampered."

    # Verify manifest hash against seal
    current_manifest_hash = sha256_file(manifest_path)
    if current_manifest_hash != matching_seal.get("manifest_sha256"):
        return False, ["MANIFEST_TAMPERED"], (
            f"Manifest hash mismatch! Seal: {matching_seal.get('manifest_sha256')}, "
            f"Disk: {current_manifest_hash}. Evidence directory has been altered."
        )

    # Read manifest
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)
    except Exception as e:
        return False, ["MANIFEST_CORRUPT"], f"Could not parse manifest: {e}"

    files_list = m.get("files", [])
    expected_files = {item["path"]: item for item in files_list}
    mismatches = []

    # Disk walk: detect extra unlisted files (S8) and verify files on disk
    disk_files_seen = set()
    for root, dirs, files in os.walk(evidence_dir):
        for file in files:
            if file in ("manifest_hashes.json", "run_seal.json", ".sealed"):
                continue
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, evidence_dir).replace("\\", "/")
            disk_files_seen.add(rel_p)

            if rel_p not in expected_files:
                mismatches.append(f"UNLISTED_FILE_INJECTED: {rel_p}")
                continue

            item = expected_files[rel_p]
            disk_size = os.path.getsize(full_p)
            disk_hash = sha256_file(full_p)
            if disk_size != item["size_bytes"] or disk_hash != item["sha256"]:
                mismatches.append(f"HASH_MISMATCH: {rel_p} (expected {item['sha256']}, got {disk_hash})")

    # Detect deleted / missing files (S9)
    for expected_rel_path in expected_files:
        if expected_rel_path not in disk_files_seen:
            mismatches.append(f"MISSING: {expected_rel_path}")

    if mismatches:
        return False, mismatches, f"{len(mismatches)} files failed verification against manifest and seal."
    return True, [], f"All {len(files_list)} files match manifest and external cryptographic seal with 100% integrity."
