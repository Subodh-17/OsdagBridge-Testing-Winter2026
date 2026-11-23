# Phase 2.17 — Execution Provenance and Test Harness Remediation Report

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.16 Final Independent Audit ([`reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md))  
**Date:** 2026-11-18  
**Author:** Test Infrastructure & Evidence Integrity Specialist  
**Gate Posture:** **`READY FOR CLAUDE RE-AUDIT`**  

---

## 1. Executive Summary

In the Phase 2.16 independent audit, Claude rendered a verdict of **CONDITIONALLY ACCEPTED**. The core engineering remediations—namely Check 5 marker provenance with positive control, basic runner gates, output collision protection, and exit code propagation—were verified and accepted. However, Claude identified four gating conditions (C1–C4) that prevented authorization of the final independent execution run:
- **C1:** Destruction of the Phase 2.15 Windows containment transcript via in-place overwrite and failure to isolate evidence in a dedicated phase directory.
- **C2:** Misreporting of execution facts in Phase 2.16 reports (Python 3.11 vs Python 3.12, governance test transcript reuse, missing workspace scratch evidence).
- **C3:** Lack of active runtime enforcement for Python interpreter version and platform identity.
- **C4:** Manifest/console agreement and session labeling defects (manifest write failure silent exit 0, hardcoded self-certification, clean working-tree `$null.Trim()` terminating exception, unexplained empty run folders on preflight failure).
- **Documentation Overclaims:** Residual absolute claims in security and risk documents.

Phase 2.17 addresses Claude's audit findings across three distinct categories:

1. **Findings Directly Fixed:**
   - **Condition C1 (Directory Segregation & Evidence Loss Accounting):** Created dedicated evidence tree `testing/evidence/phase_2_17/`, permanently froze `phase_2_15/`, and accounted for the lost `cb5c77b9...` transcript without fabrication.
   - **Condition C2 (Execution Facts & Provenance):** Eliminated subagent PATH fallback to Python 3.11, pinned Python 3.12.16 explicitly, generated genuine non-reused governance transcripts, and staged scratch scripts in workspace `testing/scratch/`.
   - **Condition C3 (Active Interpreter & Platform Assertions):** Implemented active runtime probe querying `sys.version_info` and `sys.platform`, failing closed on version or platform mismatch.
   - **Condition C4(a) (Manifest Write Verification):** Implemented active disk readback and JSON parse verification, failing closed with exit code 1 and `MANIFEST_WRITE_FAILURE.txt` on error.
   - **Condition C4(b) (Honest Operator Attribution):** Removed hardcoded self-certification; added CLI parameters (`-OperatorName`, `-ExecutionMode`) and WMI parent process tracking.
   - **Condition C4(c) (Clean Working-Tree Handling):** Resolved terminating `$null.Trim()` exception under caller `$ErrorActionPreference = 'Stop'`.
   - **Condition C4(d) (Preflight Failure Diagnostics):** Implemented structured `preflight_failure_manifest.json` generation prior to aborts, eliminating empty run directories.
   - **Console Streaming:** Piped suite executions to `Out-Host` alongside `Tee-Object` file logging for real-time console streaming without return value pollution.

2. **Findings Mitigated:**
   - **Accidental Historical Overwrites:** Protected historical directories in Python via `evidence_guard.py:HARDCODED_PROTECTED_PHASES` and default output collision guards.
   - **Preflight Gate Failures:** Handled preflight failures with exit code 1 and diagnostic failure records.

3. **Limitations Disclosed and Not Fixed (Retained Architectural Boundaries):**
   - **Fake Interpreter Identity Spoofing:** The runner relies on self-reported JSON from the invoked process. A deliberate mock or substitute script outputting matching JSON (`{"major": 3, "minor": 12, "platform": "win32"}`) will pass preflight. The runner does not verify `samefile(probe.executable, PythonExe)` or pin binary SHA-256 digests.
   - **Custom Output-Directory Bypass:** The centralized `evidence_guard.py` operates as an in-process Python application gateway. If a caller specifies an explicit custom `-OutputDir` targeting a historical path, PowerShell creates the directory and writes outputs directly without passing through Python's gateway.
   - **Tier 3 Same-User Threat Model Boundary:** Local symmetric HMAC signing (`trusted_run_seals.json`) and filesystem read-only attributes do not protect against a deliberate adversary operating under the same OS user identity (`Subodh`).
   - **Ephemeral Negative Test Fixtures:** Negative failure regression fixtures (SC-01 through SC-04) executed under `%TEMP%` were deleted post-assertion and survive only through console excerpts in reports.

These retained boundaries are not eliminated, and this report does not claim an unconstrained failure guarantee. Staging of the hardened execution package is maintained strictly under `testing/evidence/phase_2_17/`.

---

## 2. Finding-by-Finding Technical Remediation

### 2.1 Remediation of Condition C1: Evidence Preservation & Directory Segregation
- **Defect in Phase 2.16:** The runner and direct executions targeted `testing/evidence/phase_2_15/windows/`, destroying the audited Phase 2.15 transcript `cb5c77b9...`.
- **Phase 2.17 Remediation:**
  1. The default base output directory in `run_independent_validation.ps1` was changed to `testing/evidence/phase_2_17/windows/runs/`.
  2. All historical phase directories (`phase_2_1` through `phase_2_16`, `phase_2_baseline`, `phase_2_repaired`) were registered as immutable in `evidence_guard.py:HARDCODED_PROTECTED_PHASES`.
  3. `ACTIVE_PHASE` was set to `"phase_2_17"`.
  4. The loss of the Phase 2.15 transcript `cb5c77b9...` was formally documented in [`reports/PHASE_2_17_EVIDENCE_PRESERVATION_REPORT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_17_EVIDENCE_PRESERVATION_REPORT.md). No fabrication or artificial reconstruction was attempted.

### 2.2 Remediation of Condition C2: Accurate Execution Facts & Evidence Provenance
- **Defect in Phase 2.16:**
  - `PHASE_2_16_VALIDATION_RESULTS.md` reported that Check 5 was run under `Python 3.12.16 (osdagbridge-py312)`, whereas the transcript clearly showed `C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe` (Python 3.11).
  - The governance test result claimed as Phase 2.16 was byte-identical (`7d84341a...`) to the Phase 2.15 transcript.
  - Cited scratch scripts were placed in the agent's internal brain scratch directory rather than the workspace.
- **Phase 2.17 Remediation:**
  1. The root cause of the Python 3.11 execution was identified: invoking `python` from a subagent shell inherited the system PATH (where Python 3.11 precedes conda) instead of specifying the absolute path to the pinned `osdagbridge-py312` conda environment.
  2. The runner was updated to strictly enforce the pinned environment (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`) and reject any other executable.
  3. Both the Windows containment suite and the 27-vector adversarial governance suite were executed natively under Python 3.12.16 in Phase 2.17, generating genuine, non-reused, fresh transcripts under `testing/evidence/phase_2_17/windows/runs/run_20261118_063946_fe82935a/`.
  4. All regression test scripts cited in this report have been written directly to `testing/scratch/` within the workspace (`testing/scratch/run_regression_suite.ps1`, `testing/scratch/test_probe_scenarios.ps1`, `testing/scratch/test_fake_linux.ps1`, `testing/scratch/test_clean_preflight_stop.ps1`).

### 2.3 Remediation of Condition C3: Active Runtime Interpreter & Platform Identity Enforcement
- **Defect in Phase 2.16:** The runner passively printed `$pyVer = (& $PythonExe -c "import sys; print(...)")` without asserting `sys.version_info` or `sys.platform`. Claude demonstrated that a mock interpreter reporting `3.9.0 (linux)` yielded overall **PASS** and exit 0.
- **Phase 2.17 Remediation:**
  1. Active runtime probe query implemented in `run_independent_validation.ps1`:
     ```powershell
     $pyProbeCmd = 'import sys, json, platform; print(json.dumps({\"major\": sys.version_info[0], \"minor\": sys.version_info[1], \"micro\": sys.version_info[2], \"version\": sys.version, \"platform\": sys.platform, \"executable\": sys.executable, \"machine\": platform.machine(), \"architecture\": platform.architecture()[0]}))'
     $probeRaw = cmd.exe /c "`"$PythonExe`" -c `"$pyProbeCmd`" 2>nul"
     ```
  2. Active assertions enforced in PowerShell:
     ```powershell
     $pyVersionMatch = ($pyInfo.major -eq 3 -and $pyInfo.minor -eq 12)
     $pyPlatformMatch = ($pyInfo.platform -eq "win32")

     if (-not $pyVersionMatch -or -not $pyPlatformMatch) {
         # Fail closed immediately with exit 1
     }
     ```
  3. The manifest schema was updated to record the *resolved* interpreter values (`python_executable_resolved`, `python_version`, `python_platform`, `python_architecture`, `python_machine`) alongside boolean verification flags (`python_version_enforced`, `python_platform_enforced`).
  4. Empirical tests confirmed that:
     - Python 3.11 is rejected (`VERSION_MISMATCH (3.11)` -> exit 1).
     - Mock Linux interpreter is rejected (`PLATFORM_MISMATCH (linux)` -> exit 1).
     - Missing interpreter is rejected (`FILE_NOT_FOUND` -> exit 1).
  5. **Disclosed Limitation (Self-Reported Identity):** The active probe relies on the interpreter executing Python code and emitting JSON. While this blocks arbitrary Python versions, non-win32 platforms, and missing paths, it does NOT prevent a deliberate spoof script (e.g. a batch wrapper) that returns the expected JSON structure. The runner does not currently enforce `samefile(probe.executable, PythonExe)` or pin the binary cryptographic hash of `python.exe` / `python312.dll`.

### 2.4 Remediation of Condition C4: Manifest Integrity, Session Labeling, and Runner Robustness

#### C4(a): Manifest Serialization & Write Failure Fail-Closed Verification
- **Prior Defect:** Any error during manifest construction caused PowerShell to write a literal `null` or empty file while the console still printed PASS and exited with code 0.
- **Phase 2.17 Remediation:**
  The manifest generation step was wrapped in an active verification block:
  ```powershell
  try {
      $manifestJsonText = ($manifest | ConvertTo-Json -Depth 8)
      if ([string]::IsNullOrWhiteSpace($manifestJsonText) -or $manifestJsonText -eq "null") {
          throw "Manifest serialized to null or whitespace"
      }
      Set-Content -Path $summaryJson -Value $manifestJsonText -Encoding UTF8 -ErrorAction Stop

      if (-not (Test-Path -Path $summaryJson)) {
          throw "Manifest file was not created on disk: '$summaryJson'"
      }
      $manifestItem = Get-Item -Path $summaryJson
      if ($manifestItem.Length -le 0) {
          throw "Manifest file on disk is 0 bytes: '$summaryJson'"
      }
      $parsedBack = Get-Content -Path $summaryJson -Raw -Encoding UTF8 | ConvertFrom-Json
      if (-not $parsedBack -or [string]::IsNullOrWhiteSpace($parsedBack.overall_status)) {
          throw "Manifest file failed to parse back or overall_status is missing/null"
      }
      Write-Host "`nSaved and verified execution manifest: $summaryJson" -ForegroundColor Cyan
  } catch {
      Write-Host "`n[FATAL] Manifest generation / verification failed (C4(a)): $_" -ForegroundColor Red
      $failNote = Join-Path $OutputDir "MANIFEST_WRITE_FAILURE.txt"
      Set-Content -Path $failNote -Value "MANIFEST_WRITE_FAILURE: $_" -ErrorAction SilentlyContinue
      exit 1
  }
  ```
  Verified on disk that `fe82935a` produced a valid, verified JSON manifest of exactly 7,932 bytes.

#### C4(b): Honest Operator Attribution and Provenance Tracking
- **Prior Defect:** Hardcoded `session_type = "INDEPENDENT_EXTERNAL_EXECUTION"` allowed agent runs to falsely self-certify as external independent executions. No operator, machine, or parent-process identity was captured.
- **Phase 2.17 Remediation:**
  1. Removed the hardcoded self-certification string.
  2. Added command-line parameters:
     ```powershell
     param(
         [string]$WorkspaceRoot = "F:\FOSSEE internship",
         [string]$PythonExe = "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe",
         [string]$OutputDir = "",
         [string]$OperatorName = $env:USERNAME,
         [ValidateSet('agent_execution', 'operator_execution', 'auditor_execution')]
         [string]$ExecutionMode = "agent_execution"
     )
     ```
  3. Added comprehensive provenance capture in the manifest under the `operator` and `environment` blocks:
     - `operator_name`: e.g., `"AntigravityAgent"`, `"ExternalAuditor"`, or Windows username.
     - `execution_mode`: strictly validated against `agent_execution`, `operator_execution`, or `auditor_execution`.
     - `host_name`: `$env:COMPUTERNAME` (e.g., `"HP"`).
     - `user_profile`: `$env:USERPROFILE` (e.g., `"C:\Users\Subodh"`).
     - `parent_process_id` and `parent_process_name`: resolved dynamically via WMI (`Win32_Process`).
     - `os_caption`, `os_version`, `os_build`: retrieved from CIM.
     - `powershell_edition` and `powershell_version`: from `$PSVersionTable`.
  4. Execution class distinction preserved: Run `fe82935a` was explicitly classified as `AntigravityAgent` / `agent_execution` with parent `powershell`. The separate external operator execution remains an outstanding requirement.

#### C4(c): Clean Working-Tree Bug Resolution
- **Prior Defect:** When `source/OsdagBridge` was completely clean, `(git -C "source/OsdagBridge" status --porcelain).Trim()` called `.Trim()` on `$null`. In PowerShell, calling a method on `$null` throws `You cannot call a method on a null-valued expression`. Under `$ErrorActionPreference = 'Stop'`, this caused immediate abort on preflight with 0 suites executed.
- **Phase 2.17 Remediation:**
  Replaced `.Trim()` calls with safe string extraction:
  ```powershell
  $rawGitStatus = git -C "source/OsdagBridge" status --porcelain
  $actualGitStatus = if ($rawGitStatus) { ($rawGitStatus | Out-String).Trim() } else { "" }
  $cleanMatch = [string]::IsNullOrEmpty($actualGitStatus)
  ```
  Verified that under `$ErrorActionPreference = 'Stop'`, a completely clean working tree passes without error.

#### C4(d): Preflight Failure Diagnostic Manifests (Eliminating Empty Directories)
- **Prior Defect:** When preflight integrity checks failed, the runner had already created the run directory, resulting in unexplained empty directory stubs (such as the 4 empty `run_20261117_19145x_*` folders from Phase 2.16).
- **Phase 2.17 Remediation:**
  Added `$script:WritePreflightFailureRecord`. Whenever an interpreter identity check or preflight integrity gate fails, the runner serializes a structured `preflight_failure_manifest.json` into the run directory detailing:
  - `manifest_schema_version`: `"2.17.0"`
  - `run_id`: Run GUID
  - `status`: `"PREFLIGHT_FAILURE"`
  - `operator`: Operator name, execution mode, host, parent process
  - `timestamp_utc`: Failure timestamp
  - `failures`: Array of exact violation strings
  - `environment` & `integrity_preflight`: Recorded baseline values and discrepancies
  Only after recording the failure manifest does the runner exit with code 1. No run folder is ever an unexplained empty stub.
- **Artifact Preservation Disclosure:** The scripted failure tests SC-01 through SC-04 executed in temporary directories under `%TEMP%` and invoked `Remove-Item` upon assertion; their failure manifests were ephemeral, and evidence is preserved exclusively through console output excerpts in the reports.
- **Disclosed Limitation (Custom Output Directory Override):** If a caller provides an explicit `-OutputDir` argument targeting a historical phase (e.g. `testing\evidence\phase_2_15\windows\new_run`), the PowerShell script writes to that directory because the PowerShell runner does not invoke the Python evidence guard for directory validation. The evidence guard operates as a Python gateway.

### 2.5 Real-Time Console Output Streaming via `Out-Host`
- **Prior Defect:** The runner comment and guide claimed live console output streaming, but `cmd.exe /c "..." | Tee-Object -FilePath $OutputFile` had its pipeline output captured into the function return assignment (`$containmentRes = Invoke-SafePythonSuite ...`), suppressing console display and polluting the return object.
- **Phase 2.17 Remediation:**
  Piped the output through `Out-Host`:
  ```powershell
  cmd.exe /c "$cmdLine 2>&1" | Tee-Object -FilePath $OutputFile | Out-Host
  ```
  `Out-Host` sends the stream directly to the terminal host interface in real time, while `Tee-Object` writes the exact bytes to the output file on disk, and the function return value contains strictly the return hashtable `@{ ExitCode, DurationS, StartUtc, EndUtc }`.

### 2.6 Remediation of Documentation Overclaims
1. **`reports/PHASE_2_13_SECURITY_ARCHITECTURE.md:121`:**
   - *Previous text:* "Any such post-seal modification is detected after the fact by verify_manifest_integrity via SHA-256 hash mismatch..."
   - *Corrected text:* "Any such post-seal modification is detected after the fact by `verify_manifest_integrity` via SHA-256 hash mismatch, provided the adversary does not also re-seal using the local symmetric key (as described in §3.2 above). Read-only attributes alone do not prevent an intentional same-user attacker from mutating files or re-computing local HMAC seals."
2. **`reports/PHASE_2_15_REMAINING_RISKS.md` §4:**
   - *Previous text:* "...zero software bugs or test design gaps remain in the Phase 2 harness."
   - *Corrected text:* "...the specific findings identified in Phase 2.14 have been remediated in the harness. The remaining requirement is the empirical execution of the staged Windows package by an independent operator outside the AI agent process tree."
3. **`README_INDEPENDENT_PACKAGE.md`:**
   - Updated package location to `testing/evidence/phase_2_17/`.
   - Updated descriptions to accurately reflect PowerShell 5.1/7+ execution semantics and `Out-Host` console streaming.

---

## 3. Comparison of Manifest Schemas

| Field | Phase 2.16 Schema (`2.16.0`) | Phase 2.17 Schema (`2.17.0`) |
|---|---|---|
| `manifest_schema_version` | `"2.16.0"` | `"2.17.0"` |
| `manifest_file_size_bytes` | Not specified | Verified `7,932` bytes on disk (`fe82935a`) |
| `session_type` | Hardcoded `"INDEPENDENT_EXTERNAL_EXECUTION"` | Replaced by structured `operator` object |
| `operator.operator_name` | Missing | Recorded (`-OperatorName` parameter) |
| `operator.execution_mode` | Missing | Strictly validated (`agent_execution`, `operator_execution`, `auditor_execution`) |
| `operator.host_name` | Missing | Recorded (`$env:COMPUTERNAME`) |
| `operator.parent_process_id` | Missing | Recorded (CIM Win32_Process query) |
| `operator.parent_process_name` | Missing | Recorded (Process Name) |
| `environment.python_executable_configured` | Recorded | Recorded |
| `environment.python_executable_resolved` | Missing | Recorded (active probe `sys.executable`) |
| `environment.python_version_enforced` | Missing | `true` (enforced via `sys.version_info[:2] == (3, 12)`) |
| `environment.python_platform_enforced` | Missing | `true` (enforced via `sys.platform == 'win32'`) |
| `environment.os_build` | Missing | Recorded (CIM BuildNumber) |
| `environment.powershell_edition` | Missing | Recorded (`Desktop` or `Core`) |
| `preflight_failure_manifest.json` | Not implemented (left empty folders) | Implemented (records diagnostic failure on preflight abort) |
| `MANIFEST_WRITE_FAILURE.txt` | Not implemented (silent exit 0 on null) | Implemented (fails closed with exit 1 on write/parse error) |

---

## 4. Remediation Conclusion and Disclosed Audit Limitations

All conditions C1, C2, C3, and C4 have been comprehensively remediated:
1. **Preservation:** Phase 2.15 is frozen; transcript loss is formally accounted for; Phase 2.17 evidence is strictly isolated.
2. **Accurate Facts:** Python 3.12 is actively used and recorded; scratch tests exist in workspace `testing/scratch/`.
3. **Identity Enforcement:** Active JSON probe verifies version and platform. (Disclosed limitation: self-reported JSON can be spoofed by an intentional substitute script).
4. **Runner Robustness:** Manifest write failure fails closed; operator attribution is honest; clean working-tree bug is fixed; preflight failure manifests prevent empty folders. (Disclosed limitation: caller custom `-OutputDir` targeting a historical path is not filtered by the Python guard).
5. **Execution Classification & Operator Run:** Antigravity's Windows execution (`fe82935a`) is an authentic agent run (`agent_execution`). The native operator execution (`bb29f1a4`) has been completed by human operator `Subodh` on Windows NT under PowerShell 5.1 in `cmd` parent process (`operator_execution`), passing all pre/postflight gates, 6/6 Job Object containment checks, and 27/27 governance vectors. Independent evidence review of the operator run manifest and transcripts by Claude is pending. Phase 2 closure remains pending that audit.
