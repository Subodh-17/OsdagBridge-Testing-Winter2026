# Phase 2.13 Remediation Report — Comprehensive Defect Resolution

**Project:** FOSSEE OsdagBridge — Baseline Regression & Verification Harness  
**Workspace Root:** `F:\FOSSEE internship`  
**Application Repo:** `source\OsdagBridge` on branch `dev` (`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Controlling Audit:** `reports/PHASE_2_12_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Date:** 2026-11-17  
**Author:** Structural Engineering Software QA & Test-Infrastructure Team  

---

## 1. Executive Remediation Matrix

The following table provides the comprehensive finding-by-finding mapping addressing every material defect and limitation identified in Claude's Phase 2.12 independent gate audit:

| Audit Finding ID | Phase 2.12 Audit Status | Root Cause in Phase 2.12 | Phase 2.13 Remediation Implemented | Verification Method & Evidence |
|:---|:---:|:---|:---|:---|
| **F-07: Trust Anchor & Same-User Resealing** | **REJECTED** | Signing key, ledger, and evidence all owned by single Windows user (`Subodh`). Same-user scripts could re-sign (K10), re-key (K11), delete ledger entries (K13), or redirect trust dir (K14). | 1. Established 4-tier threat model in `PHASE_2_13_SECURITY_ARCHITECTURE.md`, acknowledging local HMAC provides internal tamper-detection, not cryptographic non-repudiation against the executing user.<br>2. Pinned trust store in `evidence_guard.py` and `verify_manifest.py` (`PINNED_TRUST_DIR`); disallowed unauthenticated `OSDAGBRIDGE_TRUST_DIR` overrides (fails closed with `PermissionError`).<br>3. Removed directory reuse and ledger deletion from all workflows. | Verified via `test_26_pinned_trust_directory_enforcement` (Vector 26); verified `verify_manifest.py` rejects unpinned trust directories without `--allow-unpinned-trust-dir`. |
| **F-06: Gateway Scope & Fresh-Process Overwrites** | **REJECTED** | `_SEALED_DIRECTORIES` was in-memory set only. Fresh Python process had empty set; direct test function call overwrote sealed active evidence (Probe W1). Workspace root (W6) and `reports/` (W7) lacked write gateway checks. | 1. Persistent on-disk `.sealed` marker written at end of sealing.<br>2. Persistent ledger lookup in `is_sealed_directory()` cross-checks `trusted_run_seals.json` on disk.<br>3. Filesystem read-only attributes (`os.chmod(stat.S_IREAD)` / `FILE_ATTRIBUTE_READONLY`) set on all sealed files; raw `open(filepath, 'w')` fails with `[Errno 13] Permission denied` (accidental-overwrite deterrent; owner can clear via chmod).<br>4. Blocked direct writes to `WORKSPACE_ROOT`, `.git/`, and `reports/`. | Verified via `test_24_cross_process_sealed_overwrite_prevention` (Vector 24) and `test_25_workspace_root_and_reports_protection` (Vector 25). Raw open deterred by filesystem attributes. |
| **F-05: TOCTOU Truncation & Windows Reparse Points** | **ACCEPTED (Linux)** / **NOT VERIFIED (Windows)** | Vectors 5, 13, and 15 attempted `os.symlink()`, which was skipped on Windows due to non-admin account permissions. `islink` did not recognize directory junctions. | 1. Created `is_symlink_or_junction()` detecting `FILE_ATTRIBUTE_REPARSE_POINT` (0x400) without elevation.<br>2. Implemented `create_dir_alias()` using `_winapi.CreateJunction()` on Windows.<br>3. `SafeFileWrapper` validates reparse points and realpath both pre-open and pre-commit; non-destructive staging prevents target truncation. | Vectors 5, 13, and 15 executed live on Windows without skipping: 27/27 OK. Sentinel file untruncated (SHA-256 match). |
| **F-08: Linux cgroup v2 Detection on tmpfs** | **REJECTED (Detection)** | Checked only `os.access("/sys/fs/cgroup", os.W_OK)` and `os.mkdir()`. On root/CI hosts with writable `tmpfs`, `os.mkdir` succeeded, falsely claiming `cgroup_v2`. Leaked directories; failed Vector 17. | 1. Verify filesystem mount type: parse `/proc/mounts` for `/sys/fs/cgroup` with filesystem type `cgroup2`.<br>2. Check `/sys/fs/cgroup/cgroup.controllers` hierarchy.<br>3. Verify kernel-created `cgroup.procs` inside new cgroups; reject plain directory on tmpfs.<br>4. Assign child before exec via `preexec_fn`.<br>5. Honest `BLOCKED` reporting if containment unavailable. | Verified via `test_27_linux_cgroup_tmpfs_detection_rejection` (Vector 27). Clean cleanup in `terminate()`. |
| **F-09: Windows Process Containment Empirical Proof** | **BLOCKED** | Check 1 only checked child ran; did not prove zero instructions executed before assignment. Check 5 terminated at 0.5s but only waited 4s, failing to test 8s, 15s, and 30s delayed writes. No output was preserved. | 1. Check 1 updated: child script creates marker on first line; verified marker does not exist while suspended before assignment; verified assignment succeeds before resumption; marker appears only after `ResumeThread`.<br>2. Check 5 updated: observed full 32-second horizon; confirmed delayed writes at 3s, 8s, 15s, and 30s were all blocked.<br>3. Complete live output preserved in `windows_containment_validation.txt`. | Live Windows execution: 6/6 PASS. Complete output saved in `testing/evidence/phase_2_13/windows_containment_validation.txt` and `transcripts/`. |
| **F-12: Complete Execution Provenance** | **REJECTED** | Preliminary runs reused official directories; preliminary evidence deleted; ledger edited (manual ledger surgery); missing transcripts for containment and governance; inaccurate Phase 2.11 rerun time (12:48 stated vs 12:44:30–12:45:36 actual). | 1. Official baseline and sensitivity runners executed ONCE directly into clean official directories; zero reuse or deletion.<br>2. Preliminary work isolated to `testing/evidence/phase_2_13/runs/run_<timestamp>/`.<br>3. Authoritative ledger updated via append-only protocol; zero edits or deletions.<br>4. Live console logs preserved for all runs.<br>5. Explicitly disclosed historical rerun timeline. | Complete transcripts preserved in `testing/evidence/phase_2_13/transcripts/`. Manifests match disk with 100% parity. |
| **F-10: EQ/A02 Barrier Input Oracle** | **ACCEPTED WITH LIMITATIONS** | Used production constant `DEFAULT_CRASH_BARRIER_WIDTH = 0.50 m` rather than reading `typical_section.crash_barrier.width = 0.45 m`. A02 accepted errors under 1%. | Preserved valid Phase 2.12 improvements: genuine `crash_barrier_load` key used, invented keys absent, production ignoring barrier load caught (fails EQ and A02), wrong helper caught, separate component assertions prevent cancellation. Documented width constant as honest limitation. | Verified via `test_18` and `test_19` in `test_evidence_governance.py`. 15/15 baseline alignment maintained. |
| **F-11b: C01 Multi-Girder Coverage** | **ACCEPTED WITH LIMITATIONS** | Independent stresses embed composite section modulus $Z_b = 15.9416 \times 10^6\text{ mm}^3$ (short-term $m = 7.5$). 0.8% tolerance band is an engineering design choice. | Preserved multi-girder discrimination ($G_1$ End $i = 2,900\text{ kNm}$, $G_2$ End $j = 3,200\text{ kNm}$); caught all girder/end shortcuts and $-1.0\% / -1.5\%$ shortcuts. Documented $Z_b$ embedding and 0.8% band as honest engineering choice. | Verified via `test_21` in `test_evidence_governance.py` and sensitivity matrix condition (c). |
| **F-01 to F-04, F-11a, F-11c: Historical Integrity, B01, RPT** | **ACCEPTED** | N/A (Already accepted in Phase 2.12 audit). | 1. Maintained frozen baseline `d74f56d` without modifying application source.<br>2. Maintained SQLite database hashes intact.<br>3. Preserved all historical evidence directories and manifests.<br>4. Preserved accepted B01 plate geometry mutations and RPT 29/31 shortcut discrimination. | All historical manifests verified clean; git tree 100% clean; database hashes match baseline exactly. |

---

## 2. Detailed Remediation Evidence

### 2.1 Cross-Process Seal Persistence (Workstream 2)
In Phase 2.13, `is_sealed_directory(path)` was rewritten to verify on-disk persistent state:
1. It queries the target path and walks parent directories checking for `.sealed`.
2. It queries `trusted_run_seals.json` in the pinned trust store.
3. In `generate_and_seal_manifest()`, every file in the evidence directory is set to read-only via `os.chmod(fp, stat.S_IREAD)`.
4. In `test_24_cross_process_sealed_overwrite_prevention`:
   - A sealed evidence directory was created in a temporary directory.
   - A fresh Python subprocess was spawned attempting to write `overwrite.txt` into that directory via `safe_open_evidence`.
   - The fresh process was immediately denied with:
     ```
     PermissionError: CRITICAL WRITE GATEWAY REFUSAL: Target '...' is inside a sealed immutable directory.
     ```
   - Raw `open(sample_file, "a")` was attempted, resulting in operating system access denial (`PermissionError: [Errno 13] Permission denied`):
     ```
     PermissionError: [Errno 13] Permission denied: '...'
     ```

### 2.2 Pinned Trust Store Architecture (Workstream 1)
In Phase 2.13, `get_trust_dir()` and `verify_manifest.py` pin the authoritative trust directory:
1. Pinned default: `%USERPROFILE%\.osdagbridge_trust` (Windows) / `~/.osdagbridge_trust` (POSIX).
2. If `OSDAGBRIDGE_TRUST_DIR` is set without `OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE=1`, `get_trust_dir()` raises `PermissionError`.
3. In `verify_manifest.py`:
   ```bash
   python verify_manifest.py testing/evidence/phase_2_12/baseline --trust-dir /tmp/fake_trust
   ```
   Exits with code 1:
   ```
   [CRITICAL FAILURE] TRUST ANCHOR PINNING VIOLATION (FAIL-CLOSED):
     Unpinned trust directory requested: F:\tmp\fake_trust
     Pinned official trust directory:    C:\Users\Subodh\.osdagbridge_trust
     To use an unpinned directory for isolated testing, pass --allow-unpinned-trust-dir.
   ```
4. If `--allow-unpinned-trust-dir` is passed, the utility displays:
   ```
   [SECURITY WARNING] Running with UNPINNED trust directory override: ...
   ```

### 2.3 Windows Process Containment Empirical Proof (Workstream 4)
`validate_windows_containment.py` was executed directly on Windows under Python 3.12 (`osdagbridge-py312`):
- **Check 1 (Assign-Before-Execute):**
  - Child process spawned suspended with `CREATE_SUSPENDED` (PID 28616, Thread 31348).
  - Step 1: Marker exists while suspended before assign: `False` (Verified).
  - Step 2: `AssignProcessToJobObject` success: `1` | Active in Job: `1` (Verified).
  - Step 3: Marker exists after assign but before resume: `False` (Verified).
  - Step 4: Primary thread resumed (Previous suspend count: `1`).
  - Step 5: Marker exists after resume: `True` (Verified).
  - Verdict: **PASS**.
- **Check 2 (Kill-On-Job-Close Enforcement):**
  - Child spawned (PID 37380). Job handle closed directly without terminate.
  - Child alive after close: `False`.
  - Verdict: **PASS**.
- **Check 3 (Breakaway Restrictions):**
  - Child attempted `CREATE_BREAKAWAY_FROM_JOB` (0x01000000).
  - Output: `BREAKAWAY_DENIED` | Total Active in Job: `1`.
  - Verdict: **PASS**.
- **Check 4 (Descendant Inheritance):**
  - Nested subprocesses spawned (child -> grandchild -> great-grandchild).
  - Active Processes in Job: `3` (Expected $\ge 2$).
  - Verdict: **PASS**.
- **Check 5 (Delayed Writes Across 32s Horizon):**
  - Delayed writer spawned (PID 11864). Job Object terminated at $t = 0.5\text{ s}$.
  - Observed milestones:
    - $t = 4.5\text{ s}$: Check 3s write exists = `False`
    - $t = 9.5\text{ s}$: Check 8s write exists = `False`
    - $t = 16.5\text{ s}$: Check 15s write exists = `False`
    - $t = 31.5\text{ s}$: Check 30s write exists = `False`
  - All files created after termination: 3s=`False`, 8s=`False`, 15s=`False`, 30s=`False`.
  - Verdict: **PASS**.
- **Check 6 (Complete Workload Termination):**
  - All terminated: `True` | Active processes: `0`.
  - Verdict: **PASS**.

Overall Windows Containment Status: **VERIFIED (100% Pass, 6/6)**. Output captured in `testing/evidence/phase_2_13/windows_containment_validation.txt`.

### 2.4 Windows Directory Junction TOCTOU Attack Tests (Workstream 5)
In Phase 2.13, `create_dir_alias()` replaced `os.symlink()` with `_winapi.CreateJunction()` on Windows:
- **Vector 5 (Junction to protected phase rejected):** Passed without skips.
- **Vector 13 (TOCTOU junction swap rejected at write time):** Passed without skips.
- **Vector 15 (Non-destructive TOCTOU defense never truncates target):**
  - Directory swapped to protected directory using Windows junction.
  - Target file content: `ORIGINAL_AUTHENTIC_SENTINEL_CONTENT_DO_NOT_TRUNCATE`.
  - Gateway raised `PermissionError` pre-open. Target file size (52 bytes) and SHA-256 hash remained 100% identical. Zero truncation occurred.
- All 27 tests in `test_evidence_governance.py` passed live in 25.55 s with 0 failures, 0 errors, and 0 skips on Windows. Output captured in `testing/evidence/phase_2_13/governance_test_output.txt`.

### 2.5 Complete Execution Provenance & Pristine Directories (Workstream 6)
- **Zero Official Directory Reuse:** The official baseline regression suite and sensitivity matrix were executed once directly into their dedicated directories (`testing/evidence/phase_2_13/baseline`, `candidates`, `sensitivity`). No preliminary runs ever touched or reused the official directories.
- **Append-Only Ledger:** The authoritative trust ledger was never edited or rolled back.
- **Preserved Transcripts:**
  - `testing/evidence/phase_2_13/transcripts/run_all_baseline_tests.log` (Full live baseline execution log)
  - `testing/evidence/phase_2_13/transcripts/run_sensitivity_matrix.log` (Full live sensitivity matrix log)
  - `testing/evidence/phase_2_13/transcripts/windows_containment_validation.log` (Full live Windows containment validation log)
  - `testing/evidence/phase_2_13/transcripts/governance_test_output.log` (Full live 27-vector governance test log)
- **Historical Timeline Disclosure:** Phase 2.11 historical rerun occurred between 12:44:30 and 12:45:36 UTC (as confirmed by the cryptographic seal timestamps), correcting the earlier rounded narrative of 12:48 UTC.
