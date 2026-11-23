# Phase 2.17 — Independent Native Windows Execution Package

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repo:** `source/OsdagBridge` on branch `dev` @ `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Package Directory:** `testing/evidence/phase_2_17/`  
**Target Run Directory:** `testing/evidence/phase_2_17/windows/runs/run_<timestamp>_<uuid8>/`  
**Controlling Audit:** Claude's Phase 2.16 Final Independent Audit (`reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md`)  
**Package Purpose:** Standalone, deterministic test package allowing an external operator or independent auditor to execute the Windows containment and governance suites natively outside AI agent orchestration.

---

## 1. Package Contents

This directory (`testing/evidence/phase_2_17/`) contains:

| File | Purpose |
|---|---|
| `run_independent_validation.ps1` | Standalone PowerShell 5.1/7+ execution runner. Enforces Python 3.12/win32 identity, executes containment and governance suites with real-time console streaming and file logging, prevents collisions, monitors exit codes, verifies ledger immutability, records diagnostic manifests on preflight failure, validates manifest serialization, and generates `independent_run_manifest.json`. |
| `run_independent_validation.bat` | One-click command-prompt wrapper around the PowerShell runner (passes through all parameters). |
| `README_INDEPENDENT_PACKAGE.md` | This operator and auditor execution guide. |
| `windows/runs/` | Dedicated output directory holding unique, timestamped run subfolders (`run_<timestamp>_<uuid8>/`). Authoritative primary run artifacts reside here (e.g. `runs/run_20261118_063946_fe82935a/`). |
| `windows/*.txt` & `windows/transcripts/*.log` | Non-authoritative convenience duplicate copies copied at 06:41:42 UTC from primary reference run `fe82935a` for quick inspection. They are not separate executions. |

---

## 2. Phase 2.17 Remediation Highlights (Closing Conditions C1–C4)

1. **C1 — Evidence Preservation & Strict Phase Isolation:**
   - Default output directory is strictly rooted in `testing/evidence/phase_2_17/windows/runs/`.
   - Historical evidence directories (`phase_2_15`, `phase_2_16`, etc.) are protected by `evidence_guard.py` and never touched.
   - The historical overwrite of Phase 2.15's Windows containment transcript (`cb5c77b9...`) is formally documented as evidence loss without fabrication.
2. **C2 — Accurate Execution Facts & Environment Provenance:**
   - Runner records exact Python executable (`sys.executable`), platform, architecture, machine, host name, operator name, execution mode, and parent process.
3. **C3 — Active Python 3.12 / win32 Identity Enforcement:**
   - Active probe directly queries `sys.version_info` and `sys.platform`.
   - Requires `major == 3`, `minor == 12`, and `platform == 'win32'`.
   - Fails closed immediately (exit 1) if an incorrect version (e.g., Python 3.11, Python 3.9) or non-win32 platform is provided.
4. **C4(a) — Manifest Serialization Verification:**
   - Verifies manifest JSON exists on disk, size > 0, and parses back with non-null `overall_status`.
   - Fails closed with exit 1 and writes `MANIFEST_WRITE_FAILURE.txt` if serialization or verification fails.
5. **C4(b) — Honest Operator & Session Attribution:**
   - Eliminates hardcoded self-certification.
   - Accepts `-OperatorName` (default: current Windows user `$env:USERNAME`) and `-ExecutionMode` (`agent_execution`, `operator_execution`, `auditor_execution`).
   - Manifest captures host, user, parent process, OS build, and PowerShell edition.
6. **C4(c) — Safe Clean Git Working Tree Handling:**
   - Safe string conversion prevents `$null.Trim()` terminating exceptions under `$ErrorActionPreference = 'Stop'`.
7. **C4(d) — Preflight Failure Diagnostics:**
   - If any preflight gate fails, writes `preflight_failure_manifest.json` before exiting, preventing unexplained empty directory stubs.
8. **Real-Time Console Output Streaming:**
   - Invokes test suites via `cmd.exe /c "<cmdline> 2>&1" | Tee-Object -FilePath $OutputFile | Out-Host`.
   - Sends real-time output directly to the console host without capturing pipeline text into return values, while simultaneously logging full outputs to disk.

---

## 3. Prerequisites & Baseline Verification

Before launching the package, ensure the following requirements are met:
1. **Operating System:** Windows 10 or Windows 11 (64-bit AMD64).
2. **Pinned Python Environment:** Pinned Conda environment at `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` (Python 3.12.x on win32).
3. **Privileges:** Run as a standard user (non-elevated). Do NOT elevate as Administrator.
4. **Frozen Application Baseline:**
   - Git Branch: `dev`
   - Git commit HEAD: `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
   - Git status: Clean working tree
   - `weather.sqlite`: `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98`
   - `Intg_osdag.sqlite`: `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91`
   - Production Trust Store: `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json` (`5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1`)

---

## 4. How to Execute (External Operator / Auditor)

### Option A: Via PowerShell (Recommended)

Open a clean, unprivileged Windows PowerShell 5.1 or PowerShell 7+ window:

```powershell
Set-Location -Path "F:\FOSSEE internship"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "testing\evidence\phase_2_17\run_independent_validation.ps1" -OperatorName "ExternalAuditor" -ExecutionMode "operator_execution"
```

### Option B: Via Command Prompt / Batch Launcher

Open `cmd.exe`:

```cmd
cd /d "F:\FOSSEE internship"
testing\evidence\phase_2_17\run_independent_validation.bat -OperatorName "ExternalAuditor" -ExecutionMode "operator_execution"
```

---

## 5. Execution Workflow & Enforcement Steps

1. **Workspace Verification:** Ensures root path exists.
2. **Output Collision Guard:** Prepares `testing\evidence\phase_2_17\windows\runs\run_<timestamp>_<uuid8>\`.
3. **Python Interpreter Active Check (C3):** Probes `major == 3`, `minor == 12`, `platform == 'win32'`.
4. **Pre-Flight Gates:** Asserts branch, HEAD, clean tree, DB hashes, and trust ledger hash. If any fails, writes `preflight_failure_manifest.json` and exits 1 (C4(d)).
5. **Harness Script Hashing:** Records hashes of `validate_windows_containment.py`, `test_evidence_governance.py`, `evidence_guard.py`, and `run_independent_validation.ps1`.
6. **Win32 Job Object Containment Suite (`validate_windows_containment.py`):**
   - Check 1: CREATE_SUSPENDED assign-before-execute verification.
   - Check 2: Kill-on-job-close kernel enforcement.
   - Check 3: Breakaway disallowed.
   - Check 4: Multi-tier descendant inheritance.
   - Check 5A: Uncontained positive control (verifies delayed writes at 3s, 8s, 15s, 30s with strictly ordered mtimes).
   - Check 5B: Contained run (early termination at < 3s, asserts alive before term, 32s observation horizon, 0 delayed files created).
   - Check 6: Complete workload termination (`ActiveProcesses == 0`).
7. **Adversarial Governance Suite (`test_evidence_governance.py -v`):**
   - Executes 27 attack vectors against disposable temporary fixtures.
   - Expected: 27 passed, 0 failed, 0 errors, 0 skips.
8. **Post-Flight Gates:** Re-checks branch, HEAD, clean tree, DB hashes, and trust ledger hash.
9. **Manifest Generation & Verification (C4(a)):** Writes and parses back `independent_run_manifest.json`.

---

## 6. Manifest Schema (`independent_run_manifest.json`)

```json
{
  "manifest_schema_version": "2.17.0",
  "run_id": "...",
  "operator": {
    "operator_name": "ExternalAuditor",
    "execution_mode": "operator_execution",
    "host_name": "...",
    "user_profile": "...",
    "parent_process_id": 1234,
    "parent_process_name": "cmd"
  },
  "overall_status": "PASS",
  "test_suites_status": "PASS",
  "integrity_gates_status": "PASS",
  "timing": {
    "overall_start_utc": "...",
    "overall_end_utc": "...",
    "overall_duration_s": 85.2,
    "containment_suite": { "duration_s": 67.5, "exit_code": 0, "passed": true },
    "governance_suite": { "duration_s": 17.1, "exit_code": 0, "passed": true }
  },
  "environment": {
    "platform": "win32",
    "os_caption": "Microsoft Windows 11 ...",
    "os_version": "10.0.26100",
    "os_build": 26300,
    "powershell_edition": "Desktop",
    "powershell_version": "5.1.26100.9818",
    "python_executable_configured": "C:\\Users\\Subodh\\miniconda3\\envs\\osdagbridge-py312\\python.exe",
    "python_executable_resolved": "C:\\Users\\Subodh\\miniconda3\\envs\\osdagbridge-py312\\python.exe",
    "python_version": "3.12.16 ...",
    "python_platform": "win32",
    "python_architecture": "64bit",
    "python_machine": "AMD64",
    "python_version_enforced": true,
    "python_platform_enforced": true,
    "workspace_root": "F:\\FOSSEE internship",
    "output_directory": "F:\\FOSSEE internship\\testing\\evidence\\phase_2_17\\windows\\runs\\run_..."
  },
  "harness_script_hashes": { ... },
  "integrity_preflight": { ... },
  "integrity_postflight": { ... },
  "artifacts": { ... }
}
```

The authoritative manifest generated during the reference execution (`fe82935a`) has a verified file size of **7,932 bytes** on disk (SHA-256 `d0e791ef2a35efefeb0a6dd7df330aa0f21a922bdebd09b9251561fed8f7b682`).

---

## 7. Security Boundaries & Disclosed Audit Limitations

1. **Python Application-Gateway Scope vs. PowerShell Custom Output Directory:**  
   The centralized `evidence_guard.py` operates as an in-process Python application gateway hooking calls to `safe_open_evidence` and `validate_evidence_directory`. It does not provide OS-level filesystem locks (NTFS ACLs or file attributes on unsealed folders). If an external caller passes a custom `-OutputDir` targeting a historical directory (e.g. `testing\evidence\phase_2_15\windows\new_run`), PowerShell creates the directory and writes outputs there without passing through Python's validation gateway. The runner defaults safely to `testing\evidence\phase_2_17\windows\runs\`.
2. **Self-Reported Python Interpreter Identity Probe:**  
   The active preflight probe queries the configured Python executable via `cmd.exe /c "<PythonExe> -c ..."` and parses the resulting JSON string for version and platform. A malicious binary or wrapper script (e.g. `python.bat`) outputting matching JSON (`{"major": 3, "minor": 12, "platform": "win32"}`) passes this preflight gate. The runner does not verify `samefile(probe.executable, PythonExe)` or pin binary SHA-256.
3. **Ephemeral Negative Test Artifacts:**  
   The negative failure scenarios (SC-01 through SC-04: wrong version, missing path, collision, mock Linux) executed within temporary directories in `%TEMP%` and invoked `Remove-Item -Recurse -Force` upon asserting exit codes and diagnostic failure manifests. Full disk directories were deleted post-execution; evidence for these negative scenarios is preserved exclusively via console output excerpts in the reports.
4. **Execution Class Delineation:**  
   - The reference execution in `runs/run_20261118_063946_fe82935a/` was executed by the AI agent and is explicitly self-attributed as `operator_name = "AntigravityAgent"` and `execution_mode = "agent_execution"`.
   - To satisfy Condition 1 for final Phase 2 closure, this unchanged package (`run_independent_validation.ps1` SHA-256 `31f0ea49...`) must be executed by a separate external operator or auditor in `operator_execution` mode outside the AI agent process tree.
