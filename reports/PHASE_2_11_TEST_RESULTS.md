# PHASE 2.11 — Regression Test Suite Results

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_11\`  

---

## 1. Baseline Test Execution Results

The official baseline regression suite was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline --evidence-dir testing/evidence/phase_2_11/baseline
```

### Execution Summary
- **Total Tests Executed:** 15
- **Baseline Failures (Defects Confirmed):** 11
- **Passing Checks (Environment / Tooling):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
- **Blocked (Architectural Specifications Pending):** 3 (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Errors / Harness Exceptions:** 0
- **Manifest Alignment:** 15 / 15 (100% Exact Match)
- **Execution Duration:** 27.81 s
- **Post-Manifest Verification:** SUCCESS (Zero disk drift)
- **Exit Code:** 0
- **Cryptographic Run Seal:** Recorded in `reports/PHASE_2_11_RUN_SEALS.json` (Run UUID: `0d1ffe3c-f574-48e3-b41b-c949104d35f0`)

| # | Test Identifier | Defect ID | Expected Status | Observed Status | Alignment | Duration (s) |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.82 |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 4.31 |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.14 |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 6.85 |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 4.31 |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.52 |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.21 |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.07 |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | MATCH | 0.00 |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.11 |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 3.89 |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | BASELINE_FAIL | MATCH | 0.45 |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | MATCH | 0.12 |

---

## 2. Sensitivity Matrix Execution Results

The official sensitivity matrix harness was executed via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" testing/test_cases/baseline_regression/run_sensitivity_matrix.py --evidence-dir testing/evidence/phase_2_11/sensitivity --candidates-dir testing/evidence/phase_2_11/candidates
```

### Execution Summary
- **Total Tests Evaluated:** 15
- **Actionable Tests Verified:** 12 / 12 (100% Verified)
- **Blocked Tests:** 3 / 15 (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Execution Duration:** 65.75 s
- **Post-Manifest Verification:** SUCCESS (Zero disk drift across both sensitivity and candidates directories)
- **Overall Gate Status:** PASSED
- **Exit Code:** 0
- **Sensitivity Run Seal:** Run UUID `3f53ab9b-6a86-4c7a-92fd-1336651b399c` (17 files, SHA-256 `494886219d43ebd7d0d3bec395d86bf88f1bb3e2d4f8ea27b5ce7eeb254a2ad7`)
- **Candidates Run Seal:** Run UUID `b8e24ed7-768b-4d62-95dd-b783f1c68a8d` (54 files, SHA-256 `a60e85dfe3f55439addaf77115e2fc92b14fe1b593e1c6790334bdacd8af9914`)

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

- **`evidence_guard.py` SHA-256:** `2929e746401614f17ee0362ff2a4a753ce311aeeec23d8c3f7b233fec656b825`
- **`run_all_baseline_tests.py` SHA-256:** `acb9cf8d266e7466cfcf904ebfd16172551a37a91599553f1066750337b51b43`
- **`run_sensitivity_matrix.py` SHA-256:** `91278ff56eb2c6fa4d5885e345e5d3264c5ae1ee60064971c265e31505d933ca`
- **`verify_manifest.py` SHA-256:** `a5dfbe5ef8b939fa982a5c48bbfb2670e3eb999c06d88cf50daffbbecaa15555`
- **Baseline Manifest:** `testing/evidence/phase_2_11/baseline/phase_2_11_baseline_summary.json`
- **Sensitivity Manifest:** `testing/evidence/phase_2_11/sensitivity/phase_2_11_sensitivity_matrix_summary.json`
- **External Run Seals:** `reports/PHASE_2_11_RUN_SEALS.json`
