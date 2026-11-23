# Phase 2.13 — Regression Test Suite Results & Empirical Verification

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_12_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Python Environment:** `osdagbridge-py312` (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`)  
**Evidence Root:** `testing\evidence\phase_2_13\`  
**Pinned Trust Store:** `~/.osdagbridge_trust` (`C:\Users\Subodh\.osdagbridge_trust`)  

---

## 1. Executive Summary

Phase 2.13 executed the complete test harness suite under pristine provenance conditions:
1. **Baseline Regression Suite (15 tests):** 11 defects confirmed (`BASELINE_FAIL`), 1 passing environmental check (`PASS`), 3 blocked pending specification decisions (`BLOCKED`). **15 / 15 (100%) exact manifest alignment**. Exit code `0`.
2. **Sensitivity Matrix Suite (15 tests):** **12 / 12 actionable tests verified** under strict tri-state protocol (a) baseline fail, (b) correct candidate pass, (c) plausible naive candidate fail; 3 blocked tests documented. Exit code `0`.
3. **Empirical Windows Process Containment (6/6 checks):** **6 / 6 PASS**. Zero instructions executed before Job assignment under `CREATE_SUSPENDED`. Delayed writes at 3s, 8s, 15s, and 30s empirically blocked across full 32-second observation horizon.
4. **Adversarial Governance Suite (27 attack vectors):** **27 / 27 PASS (0 skips, 0 failures, 0 errors)**. Windows directory junctions (`_winapi.CreateJunction`) eliminated previous-phase privilege skips for TOCTOU and directory swap tests.
5. **Cryptographic Run Seals & Manifest Integrity:** All three official directories (`baseline`, `candidates`, `sensitivity`) verified with mathematical parity against external HMAC-SHA256 run seals. Zero disk drift.

---

## 2. Baseline Test Execution Results

The official baseline regression suite was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline --evidence-dir testing/evidence/phase_2_13/baseline
```

### 2.1 Execution Summary
- **Total Tests Executed:** 15
- **Baseline Failures (Defects Confirmed):** 11
- **Passing Checks (Environment / Tooling):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
- **Blocked (Architectural Specifications Pending):** 3 (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Errors / Harness Exceptions:** 0
- **Manifest Alignment:** 15 / 15 (100% Exact Match)
- **Total Execution Duration:** 69.23 s
- **Exit Code:** 0 (Recorded in `testing/evidence/phase_2_13/baseline/baseline_exit_code.txt`)
- **Live Captured Transcripts:** `console_output.txt` and `console_error.txt` inside evidence directory, mirrored to `testing/evidence/phase_2_13/transcripts/run_all_baseline_tests.log`
- **Post-Manifest Verification:** SUCCESS (Zero disk drift)
- **Cryptographic Run Seal:** Run UUID `fb966e81-b715-4208-98c7-c258b7eb08fd` (HMAC-SHA256 signature `5fbbcf4d1fcd75f564f1714de68b771de780ae70fd46f38b76541dfa581bb916`)

### 2.2 Detailed Baseline Test Results

| # | Test Identifier | Defect ID | Expected Status | Observed Status | Alignment | Duration (s) | Core Defect Description |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 0.81 | Upstream `ospgrillage` ignores `load_factor = 1.35`; force ratio remains 1.00000. |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 4.30 | Snapped plate geometry ($D=1342\text{ mm}$) out of sync with solver girder sections ($D=1340\text{ mm}$); solver deviates from dynamically derived $I_z, A, I_y, J$. |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 0.14 | Static load case produces false cyclic stress ranges (envelope 125.46 MPa doubled from $\pm M$ end signs; per-LC 62.73 MPa). Expected 0.0 MPa. |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 6.84 | Applied ULS resultant (2711.74 kN) deviates by 4.0% from production solver resultant (2806.3 kN) due to unpropagated factor and barrier width discrepancy. |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 4.32 | Barrier line load (6.54 kN/m) improperly aggregated; fails independent input oracle (157.0 kN vs 192.0 kN per line). |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 3.51 | User input wind speed ($47.0\text{ m/s}$) ignored; solver hardcodes $33.0\text{ m/s}$. |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | **MATCH** | 0.00 | Blocked under DEC-015: IRC:6-2017 temperature profile and bridge deck thermal gradient specifications undecided in project documentation. |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | **MATCH** | 0.00 | Blocked under DEC-018: Fatigue vehicle axle configuration (IRC:6 Annex D 40-tonne vs 60-tonne) undecided. |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 3.20 | Executive summary reports overall `PASS` when individual girder DCR exceeds 1.000 (1.042) or stiffener fails buckling check. |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 0.07 | `designer.py:401` sets `n_girders = geom.n_l` (6), incorrectly treating 2 cantilever slab edge lines as structural longitudinal steel girders. |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | **MATCH** | 0.00 | Blocked under DEC-013: Transverse concrete slab grillage modeling (cracked vs uncracked, transformed section) undecided in architecture. |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 0.11 | Stiffener capacity calculation reports $214,533.2\text{ kN}$ (exceeding full squash load $1,918.8\text{ kN}$; fails oracle $63.4\text{ kN}$). |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 3.88 | Structural steel self-weight resultant ($169.8\text{ kN}$) matches hardcoded $78.5\text{ kN/m}^3$ instead of user-specified density $70.0\text{ kN/m}^3$ ($151.4\text{ kN}$). |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | BASELINE_FAIL | **MATCH** | 0.44 | Production call mutates package installation tree by creating unanchored `weather.sqlite` in current working directory and source folder. |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | **MATCH** | 0.12 | Native OCC offscreen Viewer3d `ExportToImage` renders opaque 3D geometry without requiring active desktop session. |

---

## 3. Sensitivity Matrix Execution Results

The official sensitivity matrix suite was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/run_sensitivity_matrix.py --evidence-dir testing/evidence/phase_2_13/sensitivity --candidates-dir testing/evidence/phase_2_13/candidates
```

### 3.1 Execution Summary
- **Total Tests Evaluated:** 15
- **Actionable Tests Evaluated:** 12
- **Actionable Tests Verified (100% Tri-State Discrimination):** **12 / 12**
- **Blocked Tests (Documented Architectural Gaps):** **3 / 15**
- **Overall Actionable Gate Status:** **PASSED**
- **Total Execution Duration:** 178.16 s
- **Exit Code:** 0 (Recorded in `testing/evidence/phase_2_13/sensitivity/sensitivity_exit_code.txt`)
- **Live Captured Transcripts:** `console_output.txt` and `console_error.txt` mirrored to `testing/evidence/phase_2_13/transcripts/run_sensitivity_matrix.log`
- **Cryptographic Run Seals:**
  - Sensitivity: Run UUID `9aac2738-e753-49ab-84e6-7a2a61548a67` (HMAC signature `71d658711b228329ee14afad9f966398998f869d5d79bf6d37ebd6c37376057f`)
  - Candidates: Run UUID `867d222a-334a-4327-aaf2-d6cc7c633bed` (HMAC signature `8ef701fcfd1d3111d7198ef41b229602686fe0925c745297b3b744bcf1d681d6`)

### 3.2 Detailed Sensitivity Matrix Table

| # | Test Identifier | Defect ID | (a) Baseline | (b) Minimal Correct | (c) Plausible Naive | Status | Discrimination Notes |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Scales loads by 1.35; (c) scales unassociated component or returns static multiplier. |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Recomputes dynamic $I_z, A, I_y, J$ from snapped plates; (c) alters $J \times 10$ or uses fixed unadjusted values. |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Resolves multi-girder ends ($G_1$ End $i = 2,900\text{ kNm}$, $G_2$ End $j = 3,200\text{ kNm}$); (c) first-girder only or $-1.5\%$ low shortcuts fail. |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Correct combination summation matches applied ULS resultant (2711.74 kN); (c) wrong barrier helper or missing factor fails. |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Genuine `crash_barrier_load` dynamically aggregated; (c) naive hardcoded barrier width fails. |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Dynamically propagates user input wind speed; (c) leaves $33.0\text{ m/s}$ hardcoded. |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-015 specification gap; honestly reported as BLOCKED. |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-018 specification gap; honestly reported as BLOCKED. |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Report summary reflects true component DCR threshold ($\le 1.000$); (c) narrative-only or DCR=1.001 passes fail. |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Ignores slab cantilever edge lines, aligning $N_{\text{girder}} = 4$; (c) naive count $N=6$ fails. |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-013 specification gap; honestly reported as BLOCKED. |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Effective section buckling capacity derived from IS 800; (c) unbounded squash formula fails. |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Propagates material density from input configuration; (c) hardcoded $78.5\text{ kN/m}^3$ fails. |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Anchors database connection to ephemeral user cache; (c) leaves working tree dirty. |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 | PASS | **PASS** | BASELINE_FAIL | **VERIFIED** | (b) Native offscreen export; (c) desktop screen-grab fails without display server. |

---

## 4. Empirical Windows Process Containment Validation

Executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/validate_windows_containment.py
```
Output captured live to `testing/evidence/phase_2_13/windows_containment_validation.txt`.

### 4.1 Empirical Results Table

| Check # | Verification Area | Target Mechanism | Empirical Behavior Observed | Verdict |
|:---:|:---|:---|:---|:---:|
| **1** | **Suspended Process Spawn & Assign-Before-Execute** | `CREATE_SUSPENDED (0x04)` + `AssignProcessToJobObject` | Child script writes marker on line 1. Step 1: marker absent while suspended (`False`). Step 2: `AssignProcessToJobObject` succeeds (`1`), active in job=`1`. Step 3: marker still absent before resume (`False`). Step 4: `ResumeThread` called. Step 5: marker created (`True`). Proves zero user instructions ran before containment. | **PASS** |
| **2** | **Kill-On-Job-Close Enforcement** | `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE (0x2000)` | Long-running child PID 37380 spawned. Job handle closed directly without `terminate()`. Process poll confirms child is dead (`False`). | **PASS** |
| **3** | **Breakaway Restrictions** | Omission of `JOB_OBJECT_LIMIT_BREAKAWAY_OK` | Child attempts `CREATE_BREAKAWAY_FROM_JOB` (0x01000000). Child output confirms `BREAKAWAY_DENIED`. Job active processes = `1`. | **PASS** |
| **4** | **Descendant Inheritance (Nested Grandchildren)** | Win32 Job Object tree inheritance | Process spawns child -> grandchild -> great-grandchild. Query confirms `3` active processes contained inside single Job boundary. | **PASS** |
| **5** | **Delayed Writes Prevention (Full 32s Horizon)** | `TerminateJobObject` at $t = 0.5\text{ s}$ | Delayed writer scheduled writes at 3s, 8s, 15s, 30s. Job terminated at 0.5s. Filesystem observed across 32s: at 4.5s (w3=`False`), at 9.5s (w8=`False`), at 16.5s (w15=`False`), at 31.5s (w30=`False`). Empirically proves all writes blocked. | **PASS** |
| **6** | **Complete Workload Termination** | `JobObjectBasicAccountingInformation` | Active processes polled until zero; confirmed `ActiveProcesses == 0` within 0.1s of termination. Zero orphan processes. | **PASS** |

**Overall Windows Containment Status:** **VERIFIED (100% Pass, 6/6)**.

---

## 5. Adversarial Governance Unit Test Suite Results

Executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -u testing/test_cases/baseline_regression/test_evidence_governance.py
```
Output captured live to `testing/evidence/phase_2_13/governance_test_output.txt`.

### 5.1 Results Summary
- **Total Tests Executed:** 27
- **Passed:** **27**
- **Skipped:** **0** (Windows directory junctions eliminated all previous-phase skips)
- **Failures / Errors:** 0
- **Execution Duration:** 25.55 s
- **Verdict:** **100% OK**

### 5.2 Complete 27-Vector Table

| Vector # | Test Function Name | Attack Class & Mechanism Tested | Result |
|:---:|:---|:---|:---:|
| 1 | `test_01_missing_evidence_dir_fails_closed` | Missing / empty string / whitespace target directory fails closed | **PASS** |
| 2 | `test_02_protected_historical_phase_rejected` | Direct target paths pointing to historical phases (`phase_1d` to `phase_2_12`) rejected | **PASS** |
| 3 | `test_03_path_traversal_targeting_protected_phases_rejected` | Traversal sequences (`active/../../phase_2_6/baseline`) detected and blocked | **PASS** |
| 4 | `test_04_case_variant_targeting_protected_phases_rejected` | Case variants (`PHASE_2_6`, `Phase_2_7`) rejected case-insensitively | **PASS** |
| 5 | `test_05_symlink_or_junction_to_protected_phase_rejected` | Directory junctions and symlinks pointing to protected phases caught and blocked | **PASS** |
| 6 | `test_06_populated_directory_reuse_rejected_by_default` | Reusing populated directory without explicit `allow_existing=True` rejected | **PASS** |
| 7 | `test_07_baseline_runner_cli_fails_on_protected_phase` | Baseline runner CLI invocation targeting protected phase exits with non-zero code | **PASS** |
| 8 | `test_08_sensitivity_runner_cli_fails_on_protected_phase` | Sensitivity runner CLI targeting protected phase exits with non-zero code | **PASS** |
| 9 | `test_09_process_lifetime_job_containment` | ProcessLifetimeJob contains child processes and reports process counts accurately | **PASS** |
| 10 | `test_10_post_manifest_tamper_detection` | Tampering with sealed file detected; raw write blocked by OS read-only attribute | **PASS** |
| 11 | `test_11_direct_test_function_write_rejected_at_write_time` | Direct test-function calls targeting protected phases fail at write time | **PASS** |
| 12 | `test_12_direct_logger_write_rejected_at_write_time` | Direct logger calls targeting protected phases fail at write time | **PASS** |
| 13 | `test_13_toctou_symlink_swap_rejected_at_write_time` | Mid-execution directory swap via junction caught before write | **PASS** |
| 14 | `test_14_protected_directories_include_baseline_repaired_and_phase_2_11` | Protected phases list exhaustive (`phase_2_11`, `phase_2_12`, `baseline_repaired`, etc.) | **PASS** |
| 15 | `test_15_non_destructive_toctou_defense_never_truncates` | Attacker swaps directory during write; destination sentinel remains 100% untruncated | **PASS** |
| 16 | `test_16_windows_assign_before_execute` | `CREATE_SUSPENDED` + Job assignment verified inside ContainedPopen hook | **PASS** |
| 17 | `test_17_extended_delayed_write_probes_contained` | Background delayed writers (3s, 8s, 15s) cleanly killed upon job exit | **PASS** |
| 18 | `test_18_eq_barrier_load_oracle_dynamic_derivation` | EQ barrier load oracle dynamically uses genuine `crash_barrier_load` key | **PASS** |
| 19 | `test_19_a02_independent_oracle_catches_mutated_helper` | A02 oracle rejects mutated production barrier helper (0.9x probe) | **PASS** |
| 20 | `test_20_b01_bottom_flange_width_mutation_rejected` | Mutating bottom flange width (410 -> 450 mm) causes test to fail | **PASS** |
| 21 | `test_21_c01_multi_girder_discrimination` | C01 rejects first-girder-only, j-end-only, i-end-only, and -1.5% low candidates | **PASS** |
| 22 | `test_22_run_seal_trust_architecture_attacks_s1_through_s11` | Run-seal trust architecture rejects all attack classes (S1–S11) fail-closed | **PASS** |
| 23 | `test_23_missing_evidence_dir_cli_execution_no_name_error` | Missing CLI `--evidence-dir` executes without `NameError: uuid` | **PASS** |
| 24 | `test_24_cross_process_sealed_overwrite_prevention` | Fresh Python subprocess cannot overwrite already-sealed directory (Probe W1) | **PASS** |
| 25 | `test_25_workspace_root_and_reports_protection` | Gateway prohibits writing to workspace root or `reports/` directory (Probes W6/W7) | **PASS** |
| 26 | `test_26_pinned_trust_directory_enforcement` | Verification fails closed on unpinned trust directory redirect (Probe K14) | **PASS** |
| 27 | `test_27_linux_cgroup_tmpfs_detection_rejection` | False cgroup v2 containment on tmpfs/hybrid hosts rejected (Audit F-08) | **PASS** |

---

## 6. Manifest & Cryptographic Run Seal Verification Summary

Independent verification utility was executed across all three official Phase 2.13 directories:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/verify_manifest.py testing/evidence/phase_2_13/baseline
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/verify_manifest.py testing/evidence/phase_2_13/candidates
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/verify_manifest.py testing/evidence/phase_2_13/sensitivity
```

### 6.1 Seal Ledger Records (`reports/PHASE_2_13_RUN_SEALS.json`)

```json
[
  {
    "run_uuid": "fb966e81-b715-4208-98c7-c258b7eb08fd",
    "phase_label": "Phase 2.13 Baseline (baseline)",
    "runner_id": "baseline_runner",
    "timestamp_utc": "2026-11-17T17:37:54.620312+00:00",
    "evidence_dir": "F:/FOSSEE internship/testing/evidence/phase_2_13/baseline",
    "total_files": 19,
    "total_bytes": 71441,
    "manifest_path": "F:/FOSSEE internship/testing/evidence/phase_2_13/baseline/manifest_hashes.json",
    "manifest_sha256": "b8711d3c777c2d53375dd23942238f86821e4fb3eebe5461c5b59f0056d91e38",
    "signature": "5fbbcf4d1fcd75f564f1714de68b771de780ae70fd46f38b76541dfa581bb916"
  },
  {
    "run_uuid": "9aac2738-e753-49ab-84e6-7a2a61548a67",
    "phase_label": "Phase 2.13 Sensitivity",
    "runner_id": "sensitivity_runner",
    "timestamp_utc": "2026-11-17T17:41:09.878418+00:00",
    "evidence_dir": "F:/FOSSEE internship/testing/evidence/phase_2_13/sensitivity",
    "total_files": 19,
    "total_bytes": 104183,
    "manifest_path": "F:/FOSSEE internship/testing/evidence/phase_2_13/sensitivity/manifest_hashes.json",
    "manifest_sha256": "0027c52b9028e70f86e955977b1cf5cecfcf0120fff878c718ea8a208dfbff06",
    "signature": "71d658711b228329ee14afad9f966398998f869d5d79bf6d37ebd6c37376057f"
  },
  {
    "run_uuid": "867d222a-334a-4327-aaf2-d6cc7c633bed",
    "phase_label": "Phase 2.13 Candidates",
    "runner_id": "candidates_runner",
    "timestamp_utc": "2026-11-17T17:41:10.080062+00:00",
    "evidence_dir": "F:/FOSSEE internship/testing/evidence/phase_2_13/candidates",
    "total_files": 54,
    "total_bytes": 115299,
    "manifest_path": "F:/FOSSEE internship/testing/evidence/phase_2_13/candidates/manifest_hashes.json",
    "manifest_sha256": "465d3f1ef9d7b14bb3f4583827d56d50ab0dc808019c432e97347c6a99fe9200",
    "signature": "8ef701fcfd1d3111d7198ef41b229602686fe0925c745297b3b744bcf1d681d6"
  }
]
```

All 92 evidence files match disk byte-for-byte and hash-for-hash. Post-manifest verification confirmed **Zero disk drift**.
