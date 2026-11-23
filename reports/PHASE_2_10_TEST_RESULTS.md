# PHASE 2.10 — Regression Test Suite Results

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_9_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_10\`  

---

## 1. Baseline Test Execution Results

The official baseline regression suite was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline --evidence-dir testing/evidence/phase_2_10/baseline
```

### Execution Summary
- **Total Tests Executed:** 15
- **Baseline Failures (Defects Confirmed):** 11
- **Passing Checks (Environment / Tooling):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
- **Blocked (Architectural Specifications Pending):** 3 (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Errors / Harness Exceptions:** 0
- **Manifest Alignment:** 15 / 15 (100% Exact Match)
- **Execution Duration:** 59.74 s
- **Post-Manifest Verification:** SUCCESS (Zero disk drift)
- **Exit Code:** 0

| # | Test Identifier | Defect ID | Expected Status | Observed Status | Alignment | Duration (s) |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.81 |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 4.34 |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.12 |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 15.42 |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 4.25 |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.56 |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 12.87 |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.08 |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.11 |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.98 |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 12.45 |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | MATCH | 1.75 |

---

## 2. Sensitivity Matrix Execution Results

The official sensitivity matrix harness was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/run_sensitivity_matrix.py --evidence-dir testing/evidence/phase_2_10/sensitivity --candidates-dir testing/evidence/phase_2_10/candidates
```

### Execution Summary
- **Total Tests Evaluated:** 15
- **Actionable Tests Verified:** 12 / 12 (100% Verified)
- **Blocked Tests:** 3 / 15 (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Execution Duration:** 73.26 s
- **Post-Manifest Verification:** SUCCESS (Zero disk drift)
- **Overall Gate Status:** PASSED
- **Exit Code:** 0

| # | Test Identifier | (a) Baseline | (b) Minimal Correct | (c) Naive Candidate | Sensitivity Status | Gate Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-015 |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-018 |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-013 |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | PASS | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |

---

## 3. Cryptographic Provenance

- **`evidence_guard.py` SHA-256:** `7823e2dc920155b9ffdfa3648a14ecb37f84a441e88e22700e12ea99d52528b7`
- **`run_all_baseline_tests.py` SHA-256:** `c830eb87e8e77a0c86807d4b4a1c52b2f6ef3f70624ce8c7a6e1df639c0fa370`
- **`run_sensitivity_matrix.py` SHA-256:** `ad121b6d91daecf89ae3298ecf0d959ca99be44c06e23ca6e8a4a58438b4d8ec`
- **Baseline Manifest:** `testing/evidence/phase_2_10/baseline/phase_2_10_baseline_summary.json`
- **Sensitivity Manifest:** `testing/evidence/phase_2_10/sensitivity/phase_2_10_sensitivity_matrix_summary.json`
- **Complete Cryptographic Inventory:** `reports/PHASE_2_10_EVIDENCE_MANIFEST.md` (96 artifacts cataloged).
