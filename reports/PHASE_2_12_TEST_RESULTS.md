# Phase 2.12 — Regression Test Suite Results

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_12\`  
**Authoritative Trust Store:** `~/.osdagbridge_trust` (`C:\Users\Subodh\.osdagbridge_trust`)  

---

## 1. Baseline Test Execution Results

The official baseline regression suite was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline --evidence-dir testing/evidence/phase_2_12/baseline
```

### 1.1 Execution Summary
- **Total Tests Executed:** 15
- **Baseline Failures (Defects Confirmed):** 11
- **Passing Checks (Environment / Tooling):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
- **Blocked (Architectural Specifications Pending):** 3 (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Errors / Harness Exceptions:** 0
- **Manifest Alignment:** 15 / 15 (100% Exact Match)
- **Total Execution Duration:** 25.59 s
- **Exit Code:** 0 (Recorded in `testing/evidence/phase_2_12/baseline/baseline_exit_code.txt`)
- **Live Captured Transcripts:** `console_output.txt` (12,511 B) and `console_error.txt` (10,673 B)
- **Post-Manifest Verification:** SUCCESS (Zero disk drift)
- **Cryptographic Run Seal:** Run UUID `efb61d9c-2986-4ecd-90cf-62fbd278f6a4` (HMAC-SHA256 signature `f14497a0daf33438bf64e7e44dbc0ca066ec97dff781aacfcb815152f87c3c8b`)

### 1.2 Detailed Baseline Test Results

| # | Test Identifier | Defect ID | Expected Status | Observed Status | Alignment | Duration (s) |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.81 |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 4.30 |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.14 |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 6.84 |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 4.32 |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.51 |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.20 |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.07 |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.11 |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.88 |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.44 |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | MATCH | 0.12 |

---

## 2. Sensitivity Matrix Execution Results

The official sensitivity matrix harness was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/run_sensitivity_matrix.py --evidence-dir testing/evidence/phase_2_12/sensitivity --candidates-dir testing/evidence/phase_2_12/candidates
```

### 2.1 Execution Summary
- **Total Tests Evaluated:** 15
- **Actionable Tests Evaluated:** 12
- **Actionable Tests Verified (100% Tri-State Discrimination):** **12 / 12**
- **Blocked Tests (Documented Architectural Gaps):** **3 / 15**
- **Overall Actionable Gate Status:** **PASSED**
- **Total Execution Duration:** 66.80 s
- **Exit Code:** 0 (Recorded in `testing/evidence/phase_2_12/sensitivity/sensitivity_exit_code.txt`)
- **Live Captured Transcripts:** `console_output.txt` (14,096 B) and `console_error.txt` (30,435 B)
- **Cryptographic Run Seals:**
  - Sensitivity: Run UUID `09dca119-7acd-450d-8b6b-11c63cf9b5a8` (HMAC signature `9dd1276cd4c0906b1fd48f213987a6ded6e61634334184a3632479bdf9a78c43`)
  - Candidates: Run UUID `c97ab96f-dccc-47f6-b4c9-b2fa7a973b45` (HMAC signature `ff51d6aa61c8c6ee8c285875d061f0fbd63aa1c0d75fe5d4134bacf988452995`)

### 2.2 Detailed Sensitivity Matrix Results

| # | Test Identifier | Defect ID | (a) Baseline | (b) Minimal Correct | (c) Plausible Wrong | Sensitivity Status | Verified |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | N/A |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | N/A |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | N/A |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | Yes |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | BASELINE_FAIL | **VERIFIED** | Yes |

---

## 3. Adversarial Governance Unit Test Suite

The 23-vector adversarial governance suite was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -m unittest testing.test_cases.baseline_regression.test_evidence_governance
```

### 3.1 Results Summary
- **Total Tests Executed:** 23
- **Passed:** 20
- **Skipped:** 3 (Vectors 6, 7, 10: non-admin Windows symlink privilege restrictions)
- **Failures / Errors:** 0
- **Execution Duration:** 20.87 s
- **Verdict:** **100% OK**

### 3.2 Coverage of Priority Security Vectors
- **Vectors 1–5:** Historical directory immutability (`phase_1d` through `phase_2_11`), case variations, and path traversal prevention.
- **Vectors 8, 11:** Write allowlisting (`_AUTHORIZED_DIRECTORIES`) rejecting writes to `source/OsdagBridge` and repo root.
- **Vectors 14, 15:** TOCTOU non-destructive staging and atomic replacement verification (zero target truncation on swap).
- **Vectors 16, 17:** Process containment: Kill-on-close and delayed-write background process termination.
- **Vectors 18, 19:** Barrier dynamic input propagation and independent oracle detection of mutated helpers.
- **Vectors 20, 21:** Engineering test mutation rejection (B01 bottom flange width, C01 multi-girder first-girder and i-end shortcuts).
- **Vectors 22, 23:** Run-seal trust architecture: HMAC-SHA256 digital signature validation, fail-closed rejection of missing seals, signature forgery, unlisted files (S8), missing files (S9), and directory swaps (S7).

---

## 4. Empirical Windows Containment Validation

Executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/validate_windows_containment.py
```

| Check # | Verification Area | Target Mechanism | Observed Behavior | Verdict |
|:---:|:---|:---|:---|:---:|
| 1 | Suspended Process Spawn | `CREATE_SUSPENDED (0x04)` | Initial thread suspended; 0 instructions executed | **PASS** |
| 2 | Pre-Execution Assignment | `AssignProcessToJobObject` | Handle assigned before thread resumed; zero uncontained instructions | **PASS** |
| 3 | Breakaway Prevention | `BREAKAWAY_DENIED` | Child attempt to spawn with `CREATE_BREAKAWAY_FROM_JOB` blocked by kernel | **PASS** |
| 4 | Kill-on-Close Boundary | `KILL_ON_JOB_CLOSE` | Closing Job handle instantly terminates all child processes | **PASS** |
| 5 | Multi-Generation Inheritance | Grandchildren trapped | 2 grandchildren and 1 child terminated simultaneously | **PASS** |
| 6 | Delayed-Write Matrix | 3s, 8s, 15s, 30s writes | Zero files written to disk; all background sleepers terminated | **PASS** |
