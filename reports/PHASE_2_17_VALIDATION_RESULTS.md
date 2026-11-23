# Phase 2.17 — Empirical Validation and Test Results Matrix

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.16 Final Independent Audit ([`reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md))  
**Date:** 2026-11-18  
**Author:** Test Infrastructure & Evidence Integrity Specialist  
**Gate Posture:** **`READY FOR CLAUDE RE-AUDIT`**  

---

## 1. Executive Summary

Phase 2.17 executed an exhaustive empirical test matrix to validate:
1. **Adversarial Failure Discrimination (Tested Preflight Conditions):** Demonstrating that the remediated runner fails closed under the five specific tested preflight failure conditions (wrong Python version, non-win32 platform string, missing interpreter path, existing output directory collision, and caller `$ErrorActionPreference = 'Stop'`). This fail-closed behavior operates within documented architectural boundaries and does not constitute an unconstrained failure guarantee; specifically, it is subject to the residual limitations documented in §4.1:
   - **Fake interpreter identity spoofing:** The active probe relies on self-reported JSON from the invoked process; a deliberate wrapper script outputting matching JSON (`{"major": 3, "minor": 12, "platform": "win32"}`) will pass preflight without binary hash pinning or `samefile()` identity verification.
   - **Custom output-directory bypass:** A caller providing an explicit custom `-OutputDir` targeting a historical phase path bypasses Python's in-process `evidence_guard.py` gateway.
   - **Ephemeral negative test cleanup:** Negative regression fixtures executed in `%TEMP%` were deleted post-assertion, surviving only via report excerpts.
2. **Preflight Failure Diagnostics:** Verifying that preflight aborts record structured diagnostic manifests (`preflight_failure_manifest.json`) rather than leaving unexplained empty folders.
3. **Full Native Windows Execution Run:** Conducting a complete, clean end-to-end execution of both the Win32 Job Object containment suite (6 checks) and the 27-vector adversarial evidence governance suite under pinned Python 3.12.16 with 100% pass rate.

The authoritative end-to-end execution (`fe82935a`) and the regression test harness were executed on the actual Windows host (Windows 11 Home, build 26300, PowerShell 5.1.26100.9818). Negative failure scenario SC-04 explicitly utilized a mock `python.bat` script to test platform rejection logic, as detailed in §2.

---

## 2. Adversarial Runner Discrimination Matrix

The table below summarizes the empirical test scenarios executed to verify runner gate behavior and error handling:

| Scenario ID | Test Condition | Invocation Parameters | Expected Result | Measured Exit Code | Manifest Recorded | Gate Verdict |
|---|---|---|---|---|---|---|
| **SC-01** | Wrong Python Version (Python 3.11) | `-PythonExe ...\Python311\python.exe` | Fail closed before suites; record failure manifest | `1` | `preflight_failure_manifest.json` | **PASS** |
| **SC-02** | Missing Python Interpreter | `-PythonExe C:\fake\python.exe` | Fail closed before suites; record failure manifest | `1` | `preflight_failure_manifest.json` | **PASS** |
| **SC-03** | Target OutputDir Already Exists | `-OutputDir <existing_dir>` | Refuse overwrite; fail closed before suites | `1` | Existing dir unmodified | **PASS** |
| **SC-04** | Mock Non-Win32 Platform (`linux`) | `-PythonExe <mock_linux_bat>` | Fail closed before suites; record failure manifest | `1` | `preflight_failure_manifest.json` | **PASS** |
| **SC-05** | Caller `$ErrorActionPreference = 'Stop'` | Caller scope Stop preference with clean tree | Evaluate clean tree safely without `$null.Trim()` error | `0` | Clean match verified | **PASS** |
| **SC-06** | Authoritative End-to-End Run | Pinned Python 3.12, clean baseline | All suites and gates pass; manifest verified | `0` | `independent_run_manifest.json` | **PASS** |

### Scenario Details & Artifact Disclosures

> [!NOTE]
> **Ephemeral Negative Test Artifacts (SC-01 through SC-04):** The scripted negative regression scenarios (`testing/scratch/run_regression_suite.ps1` and `test_fake_linux.ps1`) executed within temporary directories under `%TEMP%` (`p217_test_py311`, `p217_test_missing_py`, `p217_test_collision`, `p217_test_fake_linux`). Upon assertion of exit codes and failure manifest generation, each test block invoked `Remove-Item -Recurse -Force`. Consequently, the full disk directories were ephemeral and were deleted post-execution; evidence for these negative scenarios is preserved exclusively via the surviving console output excerpts recorded below.
>
> **Scripted Replica vs Full Runner (SC-05):** Scenario SC-05 executed `testing/scratch/test_clean_preflight_stop.ps1`, which is an isolated replica of the Git status parsing logic evaluated under caller-scope `$ErrorActionPreference = 'Stop'`. Independent reproduction of the full runner under caller Stop preference was conducted by Claude on PowerShell 7.4.

#### Scenario SC-01: Python 3.11 Rejection (Condition C3)
- **Input:** `C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe`
- **Runner Output:**
  ```text
  [2/6] Pinned Python Interpreter Identity Enforcement (C3)...
        Configured Path: C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe
        Resolved Exe:    C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe
        Python Version:  3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] -> FAIL
        Platform:        win32 (Arch: 64bit) -> MATCH (win32)

  [FATAL] Python interpreter failed active identity enforcement (C3):
          Expected: Python 3.12 on win32 platform
          Detected: Python 3.11.0 on win32
        Recorded preflight failure diagnostics to: ...\preflight_failure_manifest.json
  ```
- **Exit Code:** `1`. Failure manifest successfully written (ephemeral, deleted post-test).

#### Scenario SC-04: Mock Linux Platform Rejection (Condition C3)
- **Implementation & Scope:** Uses a temporary mock script (`python.bat` created dynamically under `%TEMP%` during regression testing and deleted post-assertion; this artifact was ephemeral and no longer exists on disk) outputting `{"major": 3, "minor": 12, "platform": "linux", ...}`.
- **What this Established:** Proves that the runner inspects the probe's returned JSON object, asserts that `platform == "win32"`, and fails closed with exit code 1 if a non-win32 string is reported.
- **What this did NOT Establish (Known Limitation):** The probe relies on self-reported JSON strings. A spoof interpreter or wrapper script that outputs the expected `win32` and `3.12` JSON response will pass preflight, because the runner does not verify that `probe.executable` equals `$PythonExe`, does not enforce architecture, and does not pin the binary cryptographic hash of `python.exe`.
- **Runner Output:**
  ```text
  [2/6] Pinned Python Interpreter Identity Enforcement (C3)...
        Configured Path: ...\python.bat
        Resolved Exe:    mock_python
        Python Version:  3.12.0 -> MATCH (3.12.x)
        Platform:        linux (Arch: 64bit) -> FAIL

  [FATAL] Python interpreter failed active identity enforcement (C3):
          Expected: Python 3.12 on win32 platform
          Detected: Python 3.12.0 on linux
        Recorded preflight failure diagnostics to: ...\preflight_failure_manifest.json
  ```
- **Exit Code:** `1`. Proves non-win32 platform string is rejected.

#### Scenario SC-05: Clean Tree under `$ErrorActionPreference = 'Stop'` (Condition C4(c))
- **Test:** Caller scope `$ErrorActionPreference = 'Stop'` invoking Git status extraction logic (`testing/scratch/test_clean_preflight_stop.ps1`).
- **Output:**
  ```text
  Testing Clean Tree Preflight Gate under ErrorActionPreference = Stop...
  Branch Match: True (dev)
  HEAD Match:   True (d74f56dd7f22925fb8148cabf5740ed8d1e39ff3)
  Clean Match:  True
  Weather DB:   True (1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98)
  Osdag DB:     True (25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91)
  Ledger Match: True (5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1)
  ALL PREFLIGHT CHECKS PASSED UNDER ErrorActionPreference = Stop!
  ```
- **Exit Code:** `0`. Safe string conversion completely prevents `$null.Trim()` terminating exception.

---

## 3. Reference Agent Execution Run (Antigravity Agent `fe82935a`)

### 3.1 Execution Profile & Provenance
- **Run ID:** `fe82935a-0927-443a-b7be-aa730468d388`
- **Output Directory:** `F:\FOSSEE internship\testing\evidence\phase_2_17\windows\runs\run_20261118_063946_fe82935a\`
- **Operator Attribution:**
  - Operator Name: `AntigravityAgent`
  - Execution Mode: `agent_execution`
  - Machine Hostname: `HP`
  - User Profile: `C:\Users\Subodh`
  - Parent Process: `powershell` (PID `28684`)
- **Environment:**
  - OS Caption: `Microsoft Windows 11 Home Single Language`
  - OS Build: `26300`
  - PowerShell Edition: `Desktop` (Version `5.1.26100.9818`)
  - Python Executable Configured: `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`
  - Python Executable Resolved: `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`
  - Python Version: `3.12.16 | packaged by conda-forge | (main, Oct 26 2026, 11:29:01) [MSC v.1944 64 bit (AMD64)]`
  - Platform / Architecture: `win32` / `64bit` (AMD64)
- **Timings:**
  - Start UTC: `2026-11-18T06:39:45.9929531Z`
  - End UTC: `2026-11-18T06:41:13.4650546Z`
  - Total Duration: `87.538s`

### 3.2 Pre-Flight Integrity Verification (All Passed)
- Git Branch: `dev` (MATCH)
- Git HEAD: `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (MATCH)
- Git Working Tree: CLEAN (0 modified, 0 untracked) (MATCH)
- `weather.sqlite`: `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` (MATCH)
- `Intg_osdag.sqlite`: `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` (MATCH)
- Production Trust Ledger: `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` (MATCH)

### 3.3 Suite 1 Results: Win32 Job Object Process Containment (`validate_windows_containment.py`)
- **Suite Duration:** `67.819s`
- **Exit Code:** `0`
- **Result:** **`PASS (6/6 Checks Verified)`**

| Check | Name | Details / Assertions | Result |
|---|---|---|---|
| **Check 1** | Suspended Process Creation & Assign-Before-Execute | Spawned PID 16036 suspended. Marker before assign: False. AssignProcessToJobObject: True. Marker before resume: False. Primary thread resumed. Marker after resume: True. | **PASS** |
| **Check 2** | Kill-On-Job-Close Enforcement | Spawned PID 34216. Closed Job handle. Child dead immediately (`is_alive = False`). | **PASS** |
| **Check 3** | Breakaway Restrictions Disallowed | Child attempted `CREATE_BREAKAWAY_FROM_JOB`. Denied (`BREAKAWAY_DENIED`). Child locked inside Job (`Total Active: 1`). | **PASS** |
| **Check 4** | Descendant Inheritance (Nested Grandchildren) | Spawned child PID 17204 launching nested grandchild. Active processes captured in Job: `3` ($\ge 2$). | **PASS** |
| **Check 5A** | Uncontained Positive Control Run | Spawned control writer PID 6004. Start marker verified with `RUN_ID` and `PID`. All 4 delayed files (`w3.txt`, `w8.txt`, `w15.txt`, `w30.txt`) created at $t = 4.50\text{s}, 9.50\text{s}, 16.50\text{s}, 31.52\text{s}$. Strictly ordered creation mtimes verified. | **PASS** |
| **Check 5B** | Contained Run Under Win32 Job Object | Spawned contained writer PID 3616. Start marker verified with `RUN_ID` and `PID`. Active in Job: `1`. Alive before term: True. Terminated early at $t = 0.078\text{s} < 3.0\text{s}$. Full 32.0s observation horizon completed. Files at milestones 3s, 8s, 15s, 30s: All `False`. Final re-check: `files present = []`. | **PASS** |
| **Check 6** | Complete Workload Termination | Terminated Job Object. Verified `all_done = True` and `ActiveProcesses == 0`. | **PASS** |

### 3.4 Suite 2 Results: Adversarial Evidence Governance (`test_evidence_governance.py -v`)
- **Suite Duration:** `18.672s`
- **Exit Code:** `0`
- **Result:** **`PASS (27/27 Vectors Verified)`**

All 27 attack vectors were executed natively against temporary, isolated fixtures. The exact test method names, docstrings, and outcomes from the authoritative Phase 2.17 governance transcript (`governance_test_output.txt`) are:
- `test_01_missing_evidence_dir_fails_closed`: Vector 1: Invocation without evidence directory or with empty string must fail closed. -> `ok`
- `test_02_protected_historical_phase_rejected`: Vector 2: Direct path targeting any historical phase directory must be refused. -> `ok`
- `test_03_path_traversal_targeting_protected_phases_rejected`: Vector 3: Traversal patterns like active/../../phase_2_6/baseline must be detected and blocked. -> `ok`
- `test_04_case_variant_targeting_protected_phases_rejected`: Vector 4: Case variants like PHASE_2_6 or Phase_2_7 must be caught on Windows/POSIX. -> `ok`
- `test_05_symlink_or_junction_to_protected_phase_rejected`: Vector 5: Symlinks or junctions pointing into protected phase directories must be caught. -> `ok`
- `test_06_populated_directory_reuse_rejected_by_default`: Vector 6: Reusing an existing populated evidence directory without allow_existing=True fails. -> `ok`
- `test_07_baseline_runner_cli_fails_on_protected_phase`: Vector 7: Executing baseline runner with protected phase directory exits with code 1. -> `ok`
- `test_08_sensitivity_runner_cli_fails_on_protected_phase`: Vector 8: Executing sensitivity runner with protected candidates directory exits with code 1. -> `ok`
- `test_09_process_lifetime_job_containment`: Vector 9: ProcessLifetimeJob contains child processes and reports process counts accurately. -> `ok`
- `test_10_post_manifest_tamper_detection`: Vector 10: Modifying an evidence file after manifest sealing is immediately detected. -> `ok`
- `test_11_direct_test_function_write_rejected_at_write_time`: Vector 11: Direct test-function calls with protected evidence_dir fail at write time. -> `ok`
- `test_12_direct_logger_write_rejected_at_write_time`: Vector 12: Direct calls to log_test_result with protected evidence_dir fail at write time. -> `ok`
- `test_13_toctou_symlink_swap_rejected_at_write_time`: Vector 13: Canonical realpath validation catches directory symlinks created after startup. -> `ok`
- `test_14_protected_directories_include_baseline_repaired_and_phase_2_11`: Vector 14: Historical directories list contains phase_2_11, phase_2_baseline, phase_2_repaired. -> `ok`
- `test_15_non_destructive_toctou_defense_never_truncates`: Vector 15: If an attacker swaps directory to a protected target, the target file is NEVER truncated. -> `ok`
- `test_16_windows_assign_before_execute_job_spawn`: Vector 16: job.spawn() assigns process to Job Object before primary thread execution. -> `ok`
- `test_17_extended_delayed_write_probes_contained`: Vector 17: Extended delayed writes (3s, 8s, 15s) are cleanly intercepted and contained on job exit. -> `ok`
- `test_18_eq_barrier_load_oracle_dynamic_derivation`: Vector 18: EQ oracle and production crash_barrier_load_from_inputs dynamically propagate genuine 'crash_barrier_load' key. -> `ok`
- `test_19_a02_raw_inputs_independent_from_production_helper`: Vector 19: A02 oracle independently derives barrier resultant from raw key, catching mutated helper. -> `ok`
- `test_20_b01_bottom_flange_width_mutation_rejected`: Vector 20: Mutating bottom flange width (410 -> 450 mm) causes test_tc_reg_b01 to fail. -> `ok`
- `test_21_c01_multi_girder_discrimination`: Vector 21: C01 rejects first-girder-only, j-end-only, i-end-only, and -1.5% low candidates. -> `ok`
- `test_22_run_seal_trust_architecture_attacks_s1_through_s11`: Vector 22: Run-Seal Trust Architecture rejects all attack classes (S1-S11) fail-closed. -> `ok`
- `test_23_missing_evidence_dir_cli_execution_no_name_error`: Vector 23: Baseline runner CLI without --evidence-dir executes without NameError: uuid. -> `ok`
- `test_24_cross_process_sealed_overwrite_prevention`: Vector 24 (Probe W1): Fresh process cannot overwrite an already-sealed directory. -> `ok`
- `test_25_workspace_root_and_reports_protection`: Vector 25 (Probes W6/W7): Gateway prohibits writing to workspace root or reports directory. -> `ok`
- `test_26_pinned_trust_directory_enforcement`: Vector 26 (Probe K14): Verification fails closed on unpinned trust directory without explicit override. -> `ok`
- `test_27_linux_cgroup_tmpfs_detection_rejection`: Vector 27 (Audit F-08): False cgroup v2 containment on tmpfs/hybrid hosts is rejected. -> `ok`

### 3.5 Post-Flight Integrity Gates (All Passed & Unchanged)
- Git Branch Post: `dev` (UNCHANGED)
- Git HEAD Post: `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (UNCHANGED)
- Git Working Tree Post: CLEAN (MATCH)
- `weather.sqlite` Post: `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` (UNCHANGED)
- `Intg_osdag.sqlite` Post: `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` (UNCHANGED)
- Production Trust Ledger Post: `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` (UNCHANGED)

### 3.6 Artifact Manifest & Hashes

The primary, authentic artifacts generated during the Phase 2.17 execution run (`run_20261118_063946_fe82935a`) are:

| Artifact File | Path in Run Folder | File Size (Bytes) | SHA-256 Digest | Status & Provenance |
|---|---|---|---|---|
| `windows_containment_validation.txt` | `runs/run_.../windows_containment_validation.txt` | 7,636 | `088eaaae0abaef27940b45f6471513917e25c588a20d69d710ba502cf952fe1c` | Primary run artifact (Tee-Object UTF-16LE) |
| `windows_containment_validation.log` | `runs/run_.../windows_containment_validation.log` | 7,636 | `088eaaae0abaef27940b45f6471513917e25c588a20d69d710ba502cf952fe1c` | Run duplicate copy (`Copy-Item` by runner) |
| `governance_test_output.txt` | `runs/run_.../governance_test_output.txt` | 15,230 | `0a66f7edcc9bb5e1e2d03e6769336462b0a70e7c71a473d3ddea317aed54a27e` | Primary run artifact (Tee-Object UTF-16LE) |
| `governance_test_output.log` | `runs/run_.../governance_test_output.log` | 15,230 | `0a66f7edcc9bb5e1e2d03e6769336462b0a70e7c71a473d3ddea317aed54a27e` | Run duplicate copy (`Copy-Item` by runner) |
| `independent_run_manifest.json` | `runs/run_.../independent_run_manifest.json` | 7,932 | `d0e791ef2a35efefeb0a6dd7df330aa0f21a922bdebd09b9251561fed8f7b682` | Verified JSON manifest on disk (7,932 bytes) |

#### Accurate Labeling of Duplicated Top-Level Transcripts
The files residing directly under `testing/evidence/phase_2_17/windows/` and `testing/evidence/phase_2_17/windows/transcripts/`:
- `testing/evidence/phase_2_17/windows/windows_containment_validation.txt` (`088eaaae...`, 7,636 B)
- `testing/evidence/phase_2_17/windows/transcripts/windows_containment_validation.log` (`088eaaae...`, 7,636 B)
- `testing/evidence/phase_2_17/windows/governance_test_output.txt` (`0a66f7ed...`, 15,230 B)
- `testing/evidence/phase_2_17/windows/transcripts/governance_test_output.log` (`0a66f7ed...`, 15,230 B)

**Provenance Disclosure:** These four files are byte-identical convenience duplicates copied at 06:41:42 UTC from the run folder `run_20261118_063946_fe82935a/` after the run concluded. They are **not separate executions** and do not contain historical materials from earlier phases.

### 3.7 Harness Script Hashes Recorded in Manifest
- `evidence_guard_py`: `19e8223f6831c4ae5538fd622dd879a423f7314d15b3ca588accde9888663df4`
- `test_evidence_governance_py`: `e1e67cbb53ccd5b66e8c54ad76a139fddcaaf256f5fd4c6ccdccee42db4330c7`
- `validate_windows_containment_py`: `d55754deb1b4cb02d036e36a5f961bcbdbe5ef298eda0ad63b44308050cc2095`
- `run_independent_validation_ps1`: `31f0ea498c7b929366a7897ab0b1693e6cc669d32673d9f60151b3e41760e183`

---

## 4. Native Operator Execution Run (Subodh `bb29f1a4`)

### 4.1 Operator Execution Profile & Provenance
- **Run ID:** `bb29f1a4-5089-4180-ad1c-96154bb405c8`
- **Output Directory:** `F:\FOSSEE internship\testing\evidence\phase_2_17\windows\runs\run_20261118_073955_bb29f1a4\`
- **Operator Attribution:**
  - Operator Name: `Subodh`
  - Execution Mode: `operator_execution`
  - Host Name: `HP`
  - User Profile: `C:\Users\Subodh`
  - Parent Process: `cmd` (PID `26676`)
- **Environment:**
  - OS Caption: `Microsoft Windows 11 Home Single Language`
  - OS Version: `10.0.26300` (Build `26300`)
  - PowerShell Edition / Version: `Desktop` / `5.1.26100.9818`
  - Python Executable Configured: `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`
  - Python Executable Resolved: `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`
  - Python Version: `3.12.16 | packaged by conda-forge | (main, Oct 26 2026, 11:29:01) [MSC v.1944 64 bit (AMD64)]`
  - Platform / Architecture: `win32` / `64bit` (AMD64)
- **Timings:**
  - Start UTC: `2026-11-18T07:39:55.7856471Z`
  - End UTC: `2026-11-18T07:41:22.4659826Z`
  - Total Duration: `86.729s`
  - Containment Suite: `67.826s` (exit code 0, passed: true)
  - Governance Suite: `17.762s` (exit code 0, passed: true)

### 4.2 Test Suite Outcomes & Integrity Gates
- **Win32 Job Object Containment Suite:** **PASS (6/6 Checks Verified)**
- **Adversarial Governance Suite:** **PASS (27/27 Vectors Verified)**
- **Preflight Integrity Gates:** 6/6 Passed (branch `dev`, HEAD `d74f56dd...`, clean tree, weather DB, osdag DB, trust ledger `5a9b9273...`)
- **Postflight Integrity Gates:** 6/6 Passed & Unchanged

### 4.3 Operator Run Artifacts & Measured Hashes

| Artifact File | Path in Operator Run Folder | File Size (Bytes) | SHA-256 Digest | Status & Provenance |
|---|---|---|---|---|
| `windows_containment_validation.txt` | `runs/run_20261118_073955_bb29f1a4/windows_containment_validation.txt` | 7,636 | `c68cbc6caba388810872c77cba408b62bed217dd81e5577b6a95706666e4104f` | Primary operator containment output |
| `windows_containment_validation.log` | `runs/run_20261118_073955_bb29f1a4/windows_containment_validation.log` | 7,636 | `c68cbc6caba388810872c77cba408b62bed217dd81e5577b6a95706666e4104f` | Runner duplicate copy |
| `governance_test_output.txt` | `runs/run_20261118_073955_bb29f1a4/governance_test_output.txt` | 15,230 | `76998aebe527175ff236cbed14a674cfae937e4b9400a207e895a6dc754c4575` | Primary operator governance output |
| `governance_test_output.log` | `runs/run_20261118_073955_bb29f1a4/governance_test_output.log` | 15,230 | `76998aebe527175ff236cbed14a674cfae937e4b9400a207e895a6dc754c4575` | Runner duplicate copy |
| `independent_run_manifest.json` | `runs/run_20261118_073955_bb29f1a4/independent_run_manifest.json` | 7,918 | `02e81c07d1eed16f134b80456b47359be18645c55eedd23090890c7064d25706` | Verified operator run manifest (UTF-8 BOM) |

### 4.4 Status & Evidential Distinction
- **Operator Execution Status:** **COMPLETED** (Executed natively by human operator `Subodh` on Windows NT under PowerShell 5.1 in `cmd` parent process, satisfying the execution component of Condition 1).
- **Independent Evidence Audit Status:** **PENDING** (Awaiting Claude's independent audit of manifest serialization, timestamp consistency, and transcript contents).

---

## 5. Validation Results Conclusion and Disclosed Limitations

### 5.1 Disclosed Audit Limitations
1. **Fake Interpreter JSON Spoofing Limitation:**  
   The runner actively checks that the interpreter returns a valid JSON string declaring Python 3.12 and win32. However, a malicious or mock wrapper that returns the expected JSON response string will pass the preflight check. The runner does not currently enforce `samefile(probe.executable, PythonExe)` or pin the binary SHA-256 of `python.exe` / `python312.dll`.
2. **Custom Output Directory Override Limitation:**  
   If a caller passes an explicit `-OutputDir` argument pointing into a historical phase (e.g. `testing\evidence\phase_2_15\windows\new_run`), the PowerShell runner creates the directory and writes outputs there. The PowerShell runner itself does not currently validate custom `-OutputDir` parameters against the Python `evidence_guard.py` protected directory inventory; the evidence guard operates as a Python application-level gateway.
3. **Tier 3 Same-User Threat Model Boundary:**  
   Local symmetric HMAC sealing and filesystem read-only attributes do not protect against an intentional attacker running under the same user profile (`Subodh`).
4. **Ephemeral Negative Test Fixtures:**  
   Negative regression fixtures executed under `%TEMP%` were deleted post-assertion and survive only through console excerpts in reports.

### 5.2 Execution Class Distinctions
- **Antigravity Reference Run (`fe82935a`):** Authentically executed on the Windows host under Windows 11 and PowerShell 5.1; correctly self-attributed as `AntigravityAgent` / `agent_execution`. It represents a verified agent readiness run, **not** an independent external execution.
- **Operator Native Windows Execution (`bb29f1a4`):** Executed natively by human operator `Subodh` under Windows PowerShell 5.1 from `cmd.exe` in `operator_execution` mode; all suites passed (6/6 containment, 27/27 governance). Independent evidence review of its artifacts by Claude is pending.
- **Claude's Independent Reproductions (IR):** Conducted in an isolated Linux cloud VM on PowerShell 7.4.6 with disposable fixtures and genuine cgroup2, validating gate failure modes, manifest error handling, and Check 5 variants.
- **Code Review (CR):** Static evaluation of Windows PowerShell 5.1 syntax, cmd quoting semantics, and Win32 Job Object API behavior.
