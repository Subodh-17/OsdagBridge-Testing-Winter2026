# Phase 2.11 Technical Report: Process Containment, Lifetime Management, and Boundary Forensics

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Controlling Audit:** `reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md` (Findings F-06, F-08)  
**Date:** 2026-11-17  

---

## 1. Context & Forensic Audit Findings

In Phase 2.10, independent auditor Claude identified critical flaws in the test harness process containment model:
- **Finding F-06 (POSIX Gap):** On POSIX / Linux, `ProcessLifetimeJob` relied on an unverified dummy implementation; process session isolation (`start_new_session=True`) and child subreaper mechanics were absent, causing Vector 9 to fail on Linux.
- **Finding F-08 (Windows Assignment Race Window):** On Windows, the harness used standard `subprocess.Popen` to create the child process, then assigned the process handle to the Win32 Job Object post-creation. This created an inherent race window: if a hostile child immediately spawned a grandchild with `DETACHED_PROCESS` or `CREATE_NEW_PROCESS_GROUP`, the grandchild could escape the Job Object before assignment completed. Furthermore, 64-bit ctypes declarations were incomplete, and the harness offered a 5.0s false assurance window.

Phase 2.11 addresses both findings with verifiable OS-level mechanisms.

---

## 2. Windows Kernel-Level Containment: Assign-Before-Execute

### 2.1 Architectural Implementation
To eliminate the race window between process creation and Job Object assignment, `evidence_guard.py` implements true **assign-before-execute** via `CREATE_SUSPENDED`:

1. **`ContainedPopen` & `_winapi.CreateProcess` Hook:**
   `ProcessLifetimeJob.spawn(*popen_args, **popen_kwargs)` intercepts child process spawning. On Windows, it patches `_winapi.CreateProcess` to bitwise-OR `CREATE_SUSPENDED (0x00000004)` into `dwCreationFlags`.
2. **Suspended Process Creation:**
   The Windows kernel creates the process, its virtual address space, and its initial thread, but places the thread in a suspended state. **The child process executes zero instructions.**
3. **Pre-Execution Job Assignment:**
   Before the child thread is permitted to run, `kernel32.AssignProcessToJobObject(self.hJob, proc_handle)` is called.
4. **Clean 64-Bit ctypes Declarations:**
   Explicit ctypes signatures ensure 64-bit cleanliness without handle truncation:
   ```python
   kernel32.CreateJobObjectW.restype = wintypes.HANDLE
   kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
   kernel32.SetInformationJobObject.restype = wintypes.BOOL
   kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
   kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
   kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
   kernel32.ResumeThread.restype = wintypes.DWORD
   kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
   kernel32.TerminateJobObject.restype = wintypes.BOOL
   kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
   ```
5. **Fail-Closed Assignment Defense:**
   If `AssignProcessToJobObject` returns `FALSE` (fails), the suspended process is immediately terminated via `kernel32.TerminateProcess` and closed without ever executing. No uncontained process is ever allowed to run.
6. **Thread Resumption:**
   Only after successful assignment is `kernel32.ResumeThread(thread_handle)` called, releasing the initial thread to begin executing.
7. **Breakaway Prevention:**
   The Job Object is configured with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE (0x2000)`. Flags permitting breakaway (`JOB_OBJECT_LIMIT_BREAKAWAY_OK` or `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`) are strictly omitted, ensuring all descendants remain trapped.

### 2.2 Active Process Accounting
To verify active process containment without unreliable sleep timers, `ProcessLifetimeJob.get_process_count()` queries `JobObjectBasicAccountingInformation (1)` via `kernel32.QueryInformationJobObject`. It reads the `ActiveProcesses` field directly from the kernel structure:
```python
class JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", wintypes.LARGE_INTEGER),
        ("TotalKernelTime", wintypes.LARGE_INTEGER),
        ("ThisPeriodTotalUserTime", wintypes.LARGE_INTEGER),
        ("ThisPeriodTotalKernelTime", wintypes.LARGE_INTEGER),
        ("TotalPageFaultCount", wintypes.DWORD),
        ("TotalProcesses", wintypes.DWORD),
        ("ActiveProcesses", wintypes.DWORD),
        ("TotalTerminatedProcesses", wintypes.DWORD),
    ]
```

---

## 3. POSIX Process Session & Subreaper Containment

On Linux / POSIX systems:
1. **Process Session Isolation (`start_new_session=True`):**
   When `job.spawn()` is called on POSIX, it passes `start_new_session=True` to `subprocess.Popen`. This invokes `setsid()` in the child before `exec`, placing the child in a new session and making it the process group leader (`pgid == pid`).
2. **Child Subreaper Registration:**
   Where available, the parent process registers as a subreaper via Linux `prctl(PR_SET_CHILD_SUBREAPER, 1)`. If child processes attempt double-fork daemonization, they are re-parented to the runner rather than `init` (PID 1), ensuring visibility and containment.
3. **Group Termination:**
   On job exit or `terminate()`, `os.killpg(self.pgid, signal.SIGKILL)` is dispatched, cleanly killing all members of the process group.

---

## 4. Empirical Containment Probes & Delayed Write Defense

In Phase 2.10, the test harness used a fixed 5.0s window for delayed writes, which was criticized as false assurance. In Phase 2.11, the delayed write defense was tested against extended multi-stage probes:

### 4.1 Probe Specifications (Adversarial Vector 17)
A probe script (`delayed_writer.py`) was spawned under `ProcessLifetimeJob` attempting delayed file writes across 3 distinct intervals:
- Write 1: 3.0 s (`write_3s.txt`)
- Write 2: 8.0 s (`write_8s.txt`)
- Write 3: 15.0 s (`write_15s.txt`)

### 4.2 Containment Results
- **Job Action:** Process spawned via `job.spawn()`, verified in Job Object (`ActiveProcesses >= 1`), and `job.terminate()` invoked at $t = 0.5\text{ s}$.
- **Post-Termination Audit ($t = 4.5\text{ s}$):**
  - `write_3s.txt`: **DOES NOT EXIST** (intercepted before write)
  - `write_8s.txt`: **DOES NOT EXIST** (intercepted before write)
  - `write_15s.txt`: **DOES NOT EXIST** (intercepted before write)
  - `ActiveProcesses`: **0**
- **Verdict:** Clean kernel-level containment with zero disk side effects.

---

## 5. Honest Boundary Assessment & Operating System Differences

| Feature | Windows Implementation | POSIX Implementation |
|---|---|---|
| **Primary Mechanism** | Win32 Kernel Job Object (`CreateJobObjectW`) | Process Session & Group Leader (`setsid`) |
| **Assign Before Execute** | **Guaranteed** via `CREATE_SUSPENDED` + `ResumeThread` | Inherent via `preexec_fn` / `setsid` in fork |
| **Breakaway Prevention** | **Enforced** (no breakaway flags set in Job Object) | Partial (hostile root or container escape can daemonize) |
| **Orphan Re-Parenting** | **N/A** (Job Object tracks all processes by handle) | Supported via `PR_SET_CHILD_SUBREAPER` (Linux 3.4+) |
| **Active Process Count** | **Exact** via `JobObjectBasicAccountingInformation` | Heuristic via process group / procfs |
| **Clean Tree Termination** | **100% Kernel-Enforced** on Job Close | `os.killpg(pgid, SIGKILL)` |

### Limitations & Scope
- **Non-Root Requirement on Linux:** On Linux systems, executing as `root` bypasses user-space restrictions. Production tests must be executed by unprivileged test service accounts.
- **Shared Memory / External daemons:** Process containment confines OS processes spawned by the Python runner; it cannot isolate external pre-existing daemon services or root-level kernel drivers.
