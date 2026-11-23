# Phase 2.16 — Independent Native Windows Execution Package

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repo:** `source/OsdagBridge` on branch `dev` @ `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Purpose:** Standalone, deterministic test package allowing an independent auditor (e.g., Claude via computer-use / desktop automation) or the project owner to execute the Windows containment and governance suites natively without AI agent orchestration.

---

## 1. Package Contents

This directory (`testing/evidence/phase_2_15/`) contains:

| File | Purpose |
|---|---|
| `run_independent_validation.ps1` | Standalone PowerShell 5.1/7+ execution runner. Enforces pre-flight and post-flight integrity gates, executes containment and governance suites via safe OS-level process streams, prevents output collisions, monitors exit codes, verifies ledger immutability, and generates `independent_run_manifest.json`. |
| `run_independent_validation.bat` | One-click command-prompt wrapper around the PowerShell runner (passes through all arguments). |
| `README_INDEPENDENT_PACKAGE.md` | This technical operator guide. |
| `windows/windows_containment_validation.txt` | Antigravity readiness containment baseline transcript. |
| `windows/governance_test_output.txt` | Antigravity readiness governance baseline transcript. |
| `windows/independent_runs/` | Dedicated output directory holding unique, timestamped run subfolders (`run_<timestamp>_<uuid8>/`) populated when an external operator executes the package. |

---

## 2. Prerequisites & Enforcement Policy

1. **Host OS:** Windows 10 or Windows 11 (64-bit AMD64).
2. **Pinned Python Environment:** Must execute under the pinned Python 3.12 environment (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`). Silent fallback to an arbitrary `python` on PATH is strictly prohibited and fails closed.
3. **Privilege Level:** Standard user (non-elevated). Do **NOT** run as Administrator; tests must verify that unprivileged userland containment holds.
4. **Pre-Flight Integrity Gates (Fatal on Mismatch):**
   - Git Branch must be exactly `dev`.
   - Git commit HEAD must be exactly `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.
   - Git working tree must be strictly clean (0 modified or untracked files).
   - `weather.sqlite` SHA-256 must be `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98`.
   - `Intg_osdag.sqlite` SHA-256 must be `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91`.
   - Production trust ledger must exist and match SHA-256 `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1`.

---

## 3. How to Run Independently

### Option A: Via PowerShell (Recommended)

Open a clean, unprivileged PowerShell terminal (PowerShell 5.1 or 7+):

```powershell
Set-Location -Path "F:\FOSSEE internship"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "testing\evidence\phase_2_15\run_independent_validation.ps1"
```

### Option B: Via Command Prompt / CMD

Open a standard `cmd.exe` terminal:

```cmd
cd /d "F:\FOSSEE internship"
testing\evidence\phase_2_15\run_independent_validation.bat
```

---

## 4. Execution Workflow & Enforcement Points

When executed, the runner performs the following steps deterministically:

1. **Interpreter Validation:** Verifies existence and executability of `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`. Fails immediately if unavailable.
2. **Output Collision Guard:** Automatically generates a unique run folder `windows\independent_runs\run_<timestamp>_<uuid8>\`. Fails safely if the folder already exists.
3. **Pre-Flight Integrity Gates:** Compares Git branch, HEAD, working tree clean status, both database hashes, and the production trust ledger against established baseline values. Exits with code 1 before launching any test if any value diverges.
4. **Harness Script Hashing:** Records SHA-256 hashes of all four test harness components (`validate_windows_containment.py`, `test_evidence_governance.py`, `evidence_guard.py`, `run_independent_validation.ps1`).
5. **Win32 Job Object Containment Suite (`validate_windows_containment.py`):**
   - **Check 1:** Suspended process executes 0 instructions before Job Object assignment.
   - **Check 2:** `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` terminates process immediately upon handle closure.
   - **Check 3:** Breakaway denial prevents evasion from the containment boundary.
   - **Check 4:** Nested multi-tier process trees (grandchild/great-grandchild) are fully captured.
   - **Check 5A (Positive Control):** Uncontained writer emits line-1 start marker bound to `RUN_ID` and `PID`; proves creation of all 4 delayed files (`w3.txt`, `w8.txt`, `w15.txt`, `w30.txt`) with strictly ordered mtimes ($t = 4.50\text{ s}, 9.50\text{ s}, 16.51\text{ s}, 31.50\text{ s}$).
   - **Check 5B (Contained Run):** Rejects stale marker; verifies start marker bound to `RUN_ID` and child `PID`; asserts child alive and Job accounting $\ge 1$; terminates early ($t < 3.0\text{ s}$); observes full 32.0s horizon and confirms **0 files created** and final clean recheck.
   - **Check 6:** Total workload termination cleans up all processes.
   - *Target Duration:* ~68 seconds. Expected Exit Code: 0.
6. **Adversarial Governance Suite (`test_evidence_governance.py -v`):**
   - Executes all 27 attack vectors against disposable temporary directories.
   - Verifies path traversal, junctions, directory swaps, delayed child writes, HMAC tampering, ledger unpinning rejection, and gateway mediation.
   - *Target Duration:* ~17 seconds. Expected: 27 passed, 0 failed, 0 errors, 0 skips. Exit Code: 0.
7. **Post-Flight Integrity Gates:**
   - Re-checks Git branch, commit HEAD, and clean status.
   - Re-checks both database SHA-256 hashes.
   - Re-checks production trust ledger SHA-256 hash.
   - Fails overall run if any modification is detected.
8. **Manifest Generation:**
   - Generates `independent_run_manifest.json` recording all metrics, timings, hashes, and explicit gate/suite verdicts.

---

## 5. Output Manifest Schema (`independent_run_manifest.json`)

The run produces `independent_run_manifest.json` in the unique run directory:

```json
{
  "manifest_schema_version": "2.16.0",
  "run_id": "...",
  "session_type": "INDEPENDENT_EXTERNAL_EXECUTION",
  "overall_status": "PASS",
  "test_suites_status": "PASS",
  "integrity_gates_status": "PASS",
  "timing": {
    "overall_start_utc": "2026-11-18T...",
    "overall_end_utc": "2026-11-18T...",
    "overall_duration_s": 85.123,
    "containment_suite": {
      "start_utc": "...",
      "end_utc": "...",
      "duration_s": 67.8,
      "exit_code": 0,
      "passed": true
    },
    "governance_suite": {
      "start_utc": "...",
      "end_utc": "...",
      "duration_s": 17.2,
      "exit_code": 0,
      "passed": true
    }
  },
  "environment": {
    "platform": "win32",
    "os_caption": "Microsoft Windows 11 Enterprise",
    "os_version": "10.0.26100",
    "powershell_version": "5.1.26100.9818",
    "python_executable": "C:\\Users\\Subodh\\miniconda3\\envs\\osdagbridge-py312\\python.exe",
    "python_version": "3.12.16 ...",
    "workspace_root": "F:\\FOSSEE internship",
    "output_directory": "F:\\FOSSEE internship\\testing\\evidence\\phase_2_15\\windows\\independent_runs\\run_..."
  },
  "harness_script_hashes": {
    "validate_windows_containment_py": "...",
    "test_evidence_governance_py": "...",
    "evidence_guard_py": "...",
    "run_independent_validation_ps1": "..."
  },
  "integrity_preflight": {
    "git_branch": "dev",
    "git_branch_match": true,
    "git_head": "d74f56dd7f22925fb8148cabf5740ed8d1e39ff3",
    "git_head_match": true,
    "git_clean": true,
    "weather_db_sha256": "1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98",
    "weather_db_match": true,
    "intg_osdag_db_sha256": "25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91",
    "intg_osdag_db_match": true,
    "trust_ledger_sha256": "5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1",
    "trust_ledger_match": true,
    "all_preflight_passed": true
  },
  "integrity_postflight": {
    "git_branch": "dev",
    "git_branch_match": true,
    "git_head": "d74f56dd7f22925fb8148cabf5740ed8d1e39ff3",
    "git_head_match": true,
    "git_clean": true,
    "weather_db_sha256": "1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98",
    "weather_db_match": true,
    "intg_osdag_db_sha256": "25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91",
    "intg_osdag_db_match": true,
    "trust_ledger_sha256": "5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1",
    "trust_ledger_match": true,
    "ledger_unchanged": true,
    "databases_unchanged": true,
    "git_unchanged": true,
    "all_postflight_passed": true
  },
  "artifacts": {
    "containment_validation_txt": { "path": "...", "sha256": "...", "bytes": 3600 },
    "containment_validation_log": { "path": "...", "sha256": "...", "bytes": 3600 },
    "governance_output_txt": { "path": "...", "sha256": "...", "bytes": 7800 },
    "governance_output_log": { "path": "...", "sha256": "...", "bytes": 7800 }
  }
}
```
