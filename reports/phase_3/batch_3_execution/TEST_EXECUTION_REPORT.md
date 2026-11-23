# PHASE 3 BATCH 3 — TEST EXECUTION REPORT

**Document ID:** P3-B3-TST-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation  
**Batch:** Phase 3 Batch 3 — DEF-01 (Component Load-Factor Scaling)  
**Directive Reference:** P3-B3-AUTH-003  
**Date:** 19 November 2026  
**Status:** ALL TESTS EXECUTED & PASSED  
**Python Environment:** `C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe` (Python 3.11.18)

---

## 1. Test Execution Architecture

Testing for Batch 3 was conducted across four distinct test suites to guarantee mathematical accuracy, non-regression, and governance enforcement:

1. **Batch 3 Comprehensive Verification Suite:** `testing/test_cases/phase_3/test_batch_3_factor_scaling.py` (15/15 passed).
2. **Official Baseline Regression Harness:** `testing/test_cases/baseline_regression/run_all_baseline_tests.py` — `test_tc_reg_a01` (flipped from `BASELINE_FAIL` to `PASS`).
3. **Batch 2 Comprehensive Verification Suite:** `testing/test_cases/phase_3/test_batch_2_comprehensive.py` (17/17 passed).
4. **Adversarial Evidence Governance Suite:** `testing/test_cases/baseline_regression/test_evidence_governance.py` (27/27 passed).

---

## 2. Test Suite 1: Batch 3 Comprehensive Verification (`test_batch_3_factor_scaling.py`)

Execution command:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe" "testing\test_cases\phase_3\test_batch_3_factor_scaling.py"
```

```text
...............
----------------------------------------------------------------------
Ran 15 tests in 16.396s

OK
```

### Individual Test Case Results:

| Test Identifier | Description & Load Type | Nominal Load | Factor | Target Reaction | Observed Reaction | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `test_or_b3_01_point_load_scaling` | Point load on 4-node mesh | $100.0\text{ kN}$ | $1.35$ | $135.000000\text{ kN}$ | $135.000000\text{ kN}$ | **PASS** |
| `test_or_b3_02_uniform_line_load_scaling` | Uniform line load on 4-node mesh | $200.0\text{ kN}$ | $1.35$ | $270.000000\text{ kN}$ | $270.000000\text{ kN}$ | **PASS** |
| `test_or_b3_03_uniform_patch_load_scaling` | Uniform patch load on 4-node mesh | $400.0\text{ kN}$ | $1.35$ | $540.000000\text{ kN}$ | $540.000000\text{ kN}$ | **PASS** |
| `test_or_b3_04_compound_multi_load_superposition` | Multi-load superposition ($P_1 + P_2$) | $60 + 100\text{ kN}$ | $1.35, 1.75$ | $256.000000\text{ kN}$ | $256.000000\text{ kN}$ | **PASS** |
| `test_or_b3_05_compound_load_vehicle_scaling` | Multi-axle vehicle CompoundLoad | $100.0\text{ kN}$ | $0.80$ | $80.000000\text{ kN}$ | $80.000000\text{ kN}$ | **PASS** |
| `test_or_b3_06_beam_element_line_load_scaling` | Direct beam-element line load | $160.0\text{ kN}$ | $1.35$ | $216.000000\text{ kN}$ | $216.000000\text{ kN}$ | **PASS** |
| `test_or_b3_07_zero_factor_relief_scaling` | Zero-factor relief ($P_1 + P_2$) | $150 + 80\text{ kN}$ | $1.35, 0.00$ | $202.500000\text{ kN}$ | $202.500000\text{ kN}$ | **PASS** |
| `test_or_b3_08_negative_reversible_factor_scaling` | Negative / reversible factor ($P$) | $120.0\text{ kN}$ | $-1.20$ | $-144.000000\text{ kN}$ | $-144.000000\text{ kN}$ | **PASS** |
| `test_or_b3_09_compounded_dual_scaling` | Dual compounding ($\gamma_{\text{load}} \times \gamma_{\text{case}}$) | $50.0\text{ kN}$ | $0.80 \times 1.10$ | $44.000000\text{ kN}$ | $44.000000\text{ kN}$ | **PASS** |
| `test_invariance_unfactored_loads` | Unfactored load equivalence ($\gamma=1.0$) | $100.0\text{ kN}$ | $1.00$ | $\Delta R_y < 10^{-12}$ | $|\Delta R_y| = 0.00$ | **PASS** |
| `test_invariance_load_object_immutability` | Load object immutability | $1.0\text{ kN}$ | $1.50$ | $P_{\text{obj}} \equiv 1.0\text{ kN}$ | $P_{\text{obj}} = 1.0\text{ kN}$ | **PASS** |
| `test_invariance_batch_1_def12` | Batch 1 DEF-12 stiffener capacity | Sizing | N/A | $63.4\text{ kN}$ | $63.4\text{ kN}$ | **PASS** |
| `test_invariance_batch_1_def11` | Batch 1 DEF-11 girder count | Layout | N/A | $4\text{ girders}$ | $4\text{ girders}$ | **PASS** |
| `test_invariance_batch_1_def08` | Batch 1 DEF-08 executive summary | Full pipeline | N/A | Dynamic `PASS` | `PASS` | **PASS** |
| `test_invariance_batch_2_statics` | Batch 2 DEF-18 statics conservation | Line load | N/A | $\Delta R_y < 10^{-9}$ | $|\Delta R_y| < 10^{-12}$ | **PASS** |

---

## 3. Test Suite 2: Baseline Regression Harness (`TC-REG-A01-FACTOR-SCALING`)

Execution log extracted from `testing/evidence/phase_3/batch_3/post_check/tc_reg_a01_factor_scaling.log`:

```text
================================================================================
TEST IDENTIFIER:        TC-REG-A01-FACTOR-SCALING
DEFECT IDENTIFIER:      DEF-01 (Upstream ospgrillage)
RESULT STATUS:          PASS
EXPECTED ON BASELINE:   BASELINE_FAIL
EXECUTION DURATION:     0.322 s
TIMESTAMP UTC:          2026-11-19T15:22:07.207703+00:00
BASELINE COMMIT:        9e0b5883a247c8c0fb74b0890915600c7ab4a896
PYTHON EXECUTABLE:      C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe
CONCRETE MODULE:        F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\core\bridge_types\plate_girder\plategirderbridge.py
================================================================================
OUTCOME SUMMARY:        Load factor 1.35 correctly scaled linear grillage forces across line and patch loads.

EXECUTION DETAILS & TRACE:
Unfactored Load Case (Line + Patch) max force: 26331.9016 N
Factored Load Case (Line + Patch) max force:   35548.0672 N (Target ratio: 1.35000)
Observed Force Ratio:                         1.35000
```

Transition from `BASELINE_FAIL` to `PASS` confirmed.

---

## 4. Test Suite 3: Batch 2 Comprehensive Verification (`test_batch_2_comprehensive.py`)

Execution command:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe" "testing\test_cases\phase_3\test_batch_2_comprehensive.py"
```

```text
Ran 17 tests in 19.541s

OK
```

All 17 Batch 2 statics and centroid tests pass with zero regression:
- TC-B2-01 through TC-B2-09 (line load mesh invariance, skew, partial, boundary) -> **100% PASS**
- TC-B2-10 through TC-B2-16 (patch load full/partial/skew/non-aligned grids) -> **100% PASS**
- TC-B2-17 (zero-crossing line load partitioning & moment conservation) -> **100% PASS**

---

## 5. Test Suite 4: Adversarial Evidence Governance (`test_evidence_governance.py`)

Execution command:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe" "testing\test_cases\baseline_regression\test_evidence_governance.py"
```

```text
Ran 27 tests in 23.058s

OK
```

All 27 vectors pass:
- Fail-closed behavior on missing evidence dir.
- Complete refusal of historical directories (`phase_1d` through `phase_2_15`).
- Directory traversal, case variance, symlink attacks blocked.
- Windows Job Object process containment active.
- Non-destructive write refusal verified.
- External run seal trust verified.
