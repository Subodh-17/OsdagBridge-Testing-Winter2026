# Phase 2.13 Technical Execution History & Forensic Provenance Ledger

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace Root:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` (`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Controlling Audit:** `reports/PHASE_2_12_FINAL_INDEPENDENT_GATE_AUDIT.md` (Finding F-12)  
**Date:** 2026-11-17  
**Author:** Structural Engineering Software QA & Test-Infrastructure Team  

---

## 1. Compliance Statement & Purpose

In Finding F-12 of the Phase 2.12 Independent Gate Audit, Claude identified several provenance and record-keeping defects:
1. Phase 2.12 preliminary runs reused the official directories, and their evidence was deleted.
2. The authoritative seal ledger was manually edited to move preliminary seals to a secondary file.
3. No console output or transcript was preserved for the Windows containment run or the governance test runs.
4. The historical narrative regarding Phase 2.11 rerun timing misstated the time as 12:48 UTC instead of the actual sealed timestamps (12:44:30–12:45:36 UTC).

This document establishes **complete, unedited, forensic transparency** over all historical disclosures, test executions, runner commands, durations, exit codes, and cryptographic seals generated during Phase 2.13.

---

## 2. Historical Execution Disclosures & Corrections (Auditing F-12)

### 2.1 Correction of Phase 2.11 Execution Timeline
In `reports/PHASE_2_12_EXECUTION_HISTORY.md`, §2 noted that the Phase 2.11 rerun occurred at "12:48 UTC". As Claude correctly established by examining the cryptographic seals on the device, the actual timestamps recorded in the HMAC-signed seals for Phase 2.11 were:
- **Baseline Run Seal:** `2026-11-17T12:44:30.412852+00:00`
- **Sensitivity Matrix Run Seal:** `2026-11-17T12:45:36.198304+00:00`

The earlier reference to "12:48 UTC" was an imprecise narrative approximation. The authoritative, incontrovertible timestamps are **12:44:30 to 12:45:36 UTC**. This forensic ledger formally corrects that record.

### 2.2 Phase 2.12 Preliminary Evidence & Ledger Disposition
In Phase 2.12, preliminary runs 3 and 4 were executed into `testing/evidence/phase_2_12/baseline` and `testing/evidence/phase_2_12/sensitivity` before minor adjustments to the barrier load input key. The directories were then cleared and re-executed, with preliminary seals moved to `preliminary_run_seals_phase_2_12.json`.

**Phase 2.13 Architectural Correction:**
In Phase 2.13, this practice was **completely abolished**:
- Official evidence directories (`testing/evidence/phase_2_13/baseline`, `candidates`, `sensitivity`) were created fresh and written **exactly once**.
- Zero preliminary runs ever targeted or reused official directories.
- Zero entries in `trusted_run_seals.json` were deleted, modified, or moved. The authoritative ledger was maintained strictly append-only.
- All live console output for every run (including containment and governance) was preserved in `testing/evidence/phase_2_13/transcripts/`.

---

## 3. Phase 2.13 Complete Chronological Execution Ledger

### Run 1: Empirical Windows Process Containment Validation
- **Timestamp (UTC):** `2026-11-17T17:34:48Z`
- **Runner Script:** `testing/test_cases/baseline_regression/validate_windows_containment.py`
- **Command Line:**
  ```powershell
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/validate_windows_containment.py *>&1 | Tee-Object -FilePath testing/evidence/phase_2_13/windows_containment_validation.txt
  ```
- **Duration:** 36.2 s (includes 32-second delayed write observation horizon)
- **Exit Code:** `0`
- **Preserved Transcripts:**
  - `testing/evidence/phase_2_13/windows_containment_validation.txt` (3,412 B)
  - `testing/evidence/phase_2_13/transcripts/windows_containment_validation.log` (3,412 B)
- **Summary of Checks:**
  1. `[PASS]` Check 1: Suspended process creation (`CREATE_SUSPENDED`), verified 0 user instructions executed before assignment, verified `AssignProcessToJobObject` success, verified marker written only after `ResumeThread`.
  2. `[PASS]` Check 2: Kill-on-job-close enforcement confirmed; child process killed immediately upon job handle close.
  3. `[PASS]` Check 3: Breakaway restrictions enforced (`BREAKAWAY_DENIED`).
  4. `[PASS]` Check 4: Descendant inheritance confirmed (3 nested processes contained).
  5. `[PASS]` Check 5: Delayed writes prevention verified across full 32-second observation horizon (3s, 8s, 15s, and 30s writes confirmed blocked).
  6. `[PASS]` Check 6: Complete workload termination confirmed (`ActiveProcesses == 0`).
- **Verdict:** **100% PASS (6/6 checks)**

---

### Run 2: Adversarial Governance Unit Test Suite (27 Vectors)
- **Timestamp (UTC):** `2026-11-17T17:35:29Z`
- **Runner Script:** `testing/test_cases/baseline_regression/test_evidence_governance.py`
- **Command Line:**
  ```powershell
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/test_evidence_governance.py *>&1 | Tee-Object -FilePath testing/evidence/phase_2_13/governance_test_output.txt
  ```
- **Duration:** 25.55 s
- **Exit Code:** `0`
- **Preserved Transcripts:**
  - `testing/evidence/phase_2_13/governance_test_output.txt` (3,686 B)
  - `testing/evidence/phase_2_13/transcripts/governance_test_output.log` (3,686 B)
- **Summary:**
  - Evaluated all 27 attack vectors covering historical immutability, path traversal, case variants, Windows directory junction swaps (Vectors 5, 13, 15), non-destructive TOCTOU staging, process containment, tamper detection, fresh-process sealed overwrite denial (Vector 24), workspace root and reports protection (Vector 25), pinned trust store enforcement (Vector 26), and Linux cgroup tmpfs rejection (Vector 27).
- **Verdict:** **Ran 27 tests in 25.545s — OK (27/27 PASS, 0 failures, 0 errors, 0 skips)**

---

### Run 3: Official Phase 2.13 Baseline Regression Suite Run
- **Timestamp (UTC):** `2026-11-17T17:36:41Z`
- **Runner Script:** `testing/test_cases/baseline_regression/run_all_baseline_tests.py`
- **Command Line:**
  ```powershell
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline --evidence-dir testing/evidence/phase_2_13/baseline *>&1 | Tee-Object -FilePath testing/evidence/phase_2_13/transcripts/run_all_baseline_tests.log
  ```
- **Duration:** 69.23 s
- **Exit Code:** `0` (Recorded in `baseline_exit_code.txt`)
- **Run UUID:** `fb966e81-b715-4208-98c7-c258b7eb08fd`
- **Manifest SHA-256:** `b8711d3c777c2d53375dd23942238f86821e4fb3eebe5461c5b59f0056d91e38`
- **HMAC Signature:** `5fbbcf4d1fcd75f564f1714de68b771de780ae70fd46f38b76541dfa581bb916`
- **Total Files:** 19 (71,441 bytes)
- **Preserved Transcripts:**
  - `testing/evidence/phase_2_13/baseline/console_output.txt`
  - `testing/evidence/phase_2_13/baseline/console_error.txt`
  - `testing/evidence/phase_2_13/transcripts/run_all_baseline_tests.log` (Full combined execution stream)
- **Summary:**
  - 15 tests executed: 11 BASELINE_FAIL, 1 PASS, 3 BLOCKED.
  - Manifest alignment: 15 / 15 matches (100%).
  - Zero disk drift post-manifest verification: SUCCESS.
- **Verdict:** **ACCEPTED**

---

### Run 4: Official Phase 2.13 Sensitivity Matrix & Candidates Run
- **Timestamp (UTC):** `2026-11-17T17:38:07Z`
- **Runner Script:** `testing/test_cases/baseline_regression/run_sensitivity_matrix.py`
- **Command Line:**
  ```powershell
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/run_sensitivity_matrix.py --evidence-dir testing/evidence/phase_2_13/sensitivity --candidates-dir testing/evidence/phase_2_13/candidates *>&1 | Tee-Object -FilePath testing/evidence/phase_2_13/transcripts/run_sensitivity_matrix.log
  ```
- **Duration:** 178.16 s
- **Exit Code:** `0` (Recorded in `sensitivity_exit_code.txt`)
- **Run UUIDs:**
  - Sensitivity: `9aac2738-e753-49ab-84e6-7a2a61548a67` (Manifest SHA-256: `0027c52b9028e70f86e955977b1cf5cecfcf0120fff878c718ea8a208dfbff06`, HMAC: `71d658711b228329ee14afad9f966398998f869d5d79bf6d37ebd6c37376057f`)
  - Candidates: `867d222a-334a-4327-aaf2-d6cc7c633bed` (Manifest SHA-256: `465d3f1ef9d7b14bb3f4583827d56d50ab0dc808019c432e97347c6a99fe9200`, HMAC: `8ef701fcfd1d3111d7198ef41b229602686fe0925c745297b3b744bcf1d681d6`)
- **Total Files:**
  - Sensitivity: 19 files (104,183 bytes)
  - Candidates: 54 files (115,299 bytes)
- **Preserved Transcripts:**
  - `testing/evidence/phase_2_13/sensitivity/console_output.txt`
  - `testing/evidence/phase_2_13/sensitivity/console_error.txt`
  - `testing/evidence/phase_2_13/transcripts/run_sensitivity_matrix.log`
- **Summary:**
  - 15 tests evaluated under tri-state protocol (a) baseline fail, (b) correct candidate pass, (c) naive candidate fail.
  - Actionable tests verified: 12 / 12 (100%).
  - Blocked tests documented: 3 / 15.
  - Actionable gate status: PASSED.
- **Verdict:** **ACCEPTED**

---

### Run 5: Independent Post-Sealing Manifest & Integrity Verification
- **Timestamp (UTC):** `2026-11-17T17:41:21Z`
- **Runner Script:** `testing/test_cases/baseline_regression/verify_manifest.py`
- **Command Line:**
  ```powershell
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/verify_manifest.py testing/evidence/phase_2_13/baseline
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/verify_manifest.py testing/evidence/phase_2_13/candidates
  & "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/verify_manifest.py testing/evidence/phase_2_13/sensitivity
  ```
- **Exit Code:** `0` across all three directories
- **Outcome:**
  - `phase_2_13/baseline`: All 19 files match manifest and external cryptographic seal with 100% integrity.
  - `phase_2_13/candidates`: All 54 files match manifest and external cryptographic seal with 100% integrity.
  - `phase_2_13/sensitivity`: All 19 files match manifest and external cryptographic seal with 100% integrity.
  - Zero disk drift detected.

---

## 4. Preserved Transcripts Inventory

All transcripts and raw console logs generated during Phase 2.13 are preserved on disk and accessible for audit review:

| Transcript Path | Size (Bytes) | Generated By | Description |
|:---|:---:|:---|:---|
| `testing/evidence/phase_2_13/windows_containment_validation.txt` | 3,412 | `validate_windows_containment.py` | Full output of the 6 Windows Win32 Job Object containment checks |
| `testing/evidence/phase_2_13/governance_test_output.txt` | 3,686 | `test_evidence_governance.py` | Full output of the 27-vector adversarial governance test suite |
| `testing/evidence/phase_2_13/transcripts/windows_containment_validation.log` | 3,412 | Run 1 Execution | Mirrored live execution log for Windows containment |
| `testing/evidence/phase_2_13/transcripts/governance_test_output.log` | 3,686 | Run 2 Execution | Mirrored live execution log for governance suite |
| `testing/evidence/phase_2_13/transcripts/run_all_baseline_tests.log` | 32,840 | Run 3 Execution | Complete unbuffered stdout/stderr of Phase 2.13 baseline runner |
| `testing/evidence/phase_2_13/transcripts/run_sensitivity_matrix.log` | 68,912 | Run 4 Execution | Complete unbuffered stdout/stderr of Phase 2.13 sensitivity runner |
| `testing/evidence/phase_2_13/baseline/console_output.txt` | 12,515 | Baseline Runner Tee | Standard output captured inside sealed baseline directory |
| `testing/evidence/phase_2_13/baseline/console_error.txt` | 10,673 | Baseline Runner Tee | Standard error captured inside sealed baseline directory |
| `testing/evidence/phase_2_13/sensitivity/console_output.txt` | 14,096 | Sensitivity Runner Tee | Standard output captured inside sealed sensitivity directory |
| `testing/evidence/phase_2_13/sensitivity/console_error.txt` | 30,435 | Sensitivity Runner Tee | Standard error captured inside sealed sensitivity directory |
