# PHASE 3 BATCH 3 — REGRESSION RESULTS REPORT

**Document ID:** P3-B3-REG-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation  
**Batch:** Phase 3 Batch 3 — DEF-01 (Component Load-Factor Scaling)  
**Directive Reference:** P3-B3-AUTH-003  
**Date:** 19 November 2026  
**Status:** ZERO REGRESSIONS DETECTED  

---

## 1. Executive Summary

This report evaluates non-regression across all historical remediation batches, un-factored load operations, and the official baseline regression harness following the implementation of DEF-01 in `src/ospgrillage/osp_grillage.py`.

Zero regressions were detected across all evaluated dimensions:
1. `TC-REG-A01-FACTOR-SCALING` flipped cleanly from `BASELINE_FAIL` to `PASS`.
2. Batch 1 remediations (`DEF-12`, `DEF-08`, `DEF-11`) remain 100% invariant.
3. Batch 2 remediations (`DEF-18-LINE`, `DEF-18-PATCH`, 17 tests) remain 100% invariant.
4. Nominal loads ($\gamma = 1.00$) produce bit-for-bit identical reactions before and after remediation.
5. Original load objects remain immutable in-place.

---

## 2. Regression Harness Manifest Comparison

| Test Identifier | Associated Defect | Phase 2 Baseline State | Phase 3 Batch 2 State | Phase 3 Batch 3 Observed State | Expected Remediation State | Regression Assessment |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **`TC-REG-A01-FACTOR-SCALING`** | **DEF-01** | `BASELINE_FAIL` | `BASELINE_FAIL` | **`PASS`** | `PASS` | **DEFECT RESOLVED** |
| `TC-REG-CAP-STIFFENER` | DEF-12 | `BASELINE_FAIL` | `PASS` | **`PASS`** | `PASS` | **INVARIANT** |
| `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT`| DEF-11 | `BASELINE_FAIL` | `PASS` | **`PASS`** | `PASS` | **INVARIANT** |
| `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | `BASELINE_FAIL` | `PASS` | **`PASS`** | `PASS` | **INVARIANT** |
| `TC-B2-01` to `TC-B2-17` | DEF-18 | N/A | `PASS` (17/17) | **`PASS` (17/17)** | `PASS` | **INVARIANT** |

---

## 3. Detailed Invariance Gate Evaluations

### 3.1 Unfactored Load Invariance Gate
- **Test Objective:** Verify that defining a load with `load_factor=1.0` or omitting `load_factor` entirely produces identical finite element reactions and member forces.
- **Fixture:** $20\text{ m} \times 10\text{ m}$ grillage with longitudinal line load $w = 5.0\text{ kN/m}$.
- **Unfactored Reaction (default factor 1.0):** $R_{y,1} = 100000.000000000\text{ N}$, $x_1 = 10.000000000\text{ m}$.
- **Explicit Factored Reaction (`load_factor=1.0`):** $R_{y,2} = 100000.000000000\text{ N}$, $x_2 = 10.000000000\text{ m}$.
- **Residual:** $|R_{y,1} - R_{y,2}| = 0.000000000\text{ N}$ ($< 10^{-12}$).
- **Verdict:** **PASS — STRICT INVARIANCE CONFIRMED.**

### 3.2 Load Object Immutability Gate
- **Test Objective:** Verify that applying a load factor during grillage load distribution does not alter the underlying attributes of the `Loads` object stored in `load_case.load_groups`.
- **Fixture:** PointLoad with nominal magnitude $P = 1000.0\text{ N}$ scaled by $\gamma = 1.50$.
- **Pre-Analysis Magnitude:** $1000.0\text{ N}$.
- **Post-Analysis Magnitude of Original Object:** $1000.0\text{ N}$.
- **Post-Analysis Magnitude inside `load_groups[0]["load"]`:** $1000.0\text{ N}$.
- **Verdict:** **PASS — ZERO IN-PLACE MUTATION.**

### 3.3 Batch 1 Remediation Invariance
- **DEF-12:** Bearing stiffener buckling capacity remains $63.4\text{ kN}$ (`status: PASS`).
- **DEF-11:** `BridgeConfig.girder_count` remains aligned with physical girders at $4$ girders (`status: PASS`).
- **DEF-08:** Executive summary dynamically evaluates limit states and reports `PASS` (`status: PASS`).
- **Verdict:** **PASS — BATCH 1 INTACT.**

### 3.4 Batch 2 Remediation Invariance
- All 17 comprehensive tests in `test_batch_2_comprehensive.py` passed in $19.541\text{ s}$.
- Line load force conservation error across varying mesh densities remains $< 10^{-12}\text{ N}$.
- Patch load area and force integration across non-aligned grids remain exact ($239.400\text{ kN}$).
- Zero-crossing line load partitioning preserves force neutrality ($\sum R_y = 0.0\text{ N}$) and moment conservation.
- **Verdict:** **PASS — BATCH 2 INTACT.**
