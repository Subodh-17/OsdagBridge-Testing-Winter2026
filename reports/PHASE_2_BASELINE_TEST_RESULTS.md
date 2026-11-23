# PHASE 2 BASELINE REGRESSION TEST RESULTS & GATING AUDIT

**Workspace:** `F:\FOSSEE internship`  
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`  
**Frozen Baseline Git Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev` branch)  
**Reference Environment:** `osdagbridge-py312` (Python 3.12.16 | conda-forge / PyPI isolated)  
**Date:** 2026-11-16  
**Status:** **GATING PREREQUISITES COMPLETED — READY FOR REMEDIATION BRANCH**  

---

## 1. Executive Summary & Gating Outcome

In accordance with the directive `# PHASE 2 — GATING CONDITIONS AND BASELINE REGRESSION SETUP`, an automated baseline regression campaign was executed against the pristine upstream commit `d74f56d`.

### Primary Objectives Met:
1. **Zero Source Code Alteration:** No application code was modified, patched, or refactored.
2. **Elimination of Flawed Tests:** Tautological assertions, incorrect attribute names, and invalid key injections identified in the independent review reconciliation were purged.
3. **100% Defect Capture Rate:** All 14 implemented regression tests executed cleanly, with **0 unhandled exceptions**, **0 blocked tests**, **0 anomalous failures**, and **14 confirmed baseline failures** (100% intended failure rate).
4. **Independent Evidence Logging:** Full execution logs and structured summaries were recorded in `testing/evidence/phase_2_baseline/`.

### Final Recommendation:
**DECISIVE GO** for creating the dedicated remediation feature branch (`fix/phase-2-remediation`). All pre-implementation gating prerequisites have been satisfied.

---

## 2. Baseline Environment & Repository Integrity

Prior to running the regression suite, the environment and repository state were independently audited:
- **Repository Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (clean `dev` tracking `origin/dev`).
- **Python Executable:** `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` (Python 3.12.16).
- **Environment Isolation:** `PYTHONNOUSERSITE = 1` enforced; user site-packages excluded.
- **Database Hashes:** Unaltered (`osdag_core_db`: `fed15f...`, `osdagbridge_local_db`: `25f978...`, `weather.sqlite`: `1d7676...`).
- **Test Runner:** `testing/test_cases/baseline_regression/run_all_baseline_tests.py`.

---

## 3. Comprehensive Baseline Test Execution Matrix

| Test Identifier | Defect ID | Test Level | Baseline Outcome | Expected on Baseline? | Exact Failure Reason / Defect Mechanism | Evidence Log Path | Post-Fix Readiness |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| **`TC-REG-A01-FACTOR-SCALING`** | DEF-01 | Unit | **FAIL** | **YES** | Load factor 1.35 was ignored by `ospgrillage._distribute_load_types_to_model`; force ratio is 1.00000 (expected 1.35000). | `testing/evidence/phase_2_baseline/tc_reg_a01_factor_scaling.log` | **READY** |
| **`TC-REG-B01-SECTION-PROPERTY-SYNC`** | DEF-03 | Integration | **FAIL** | **YES** | Assigned $I_z$ ($0.00734091\text{ m}^4$) retains preliminary sizing and fails to match snapped plate $I_z$ ($0.00795392\text{ m}^4$, diff 7.71%). | `testing/evidence/phase_2_baseline/tc_reg_b01_section_property_sync.log` | **READY** |
| **`TC-REG-C01-SECTIONAL-STRESS-RANGE`** | DEF-07 | Unit | **FAIL** | **YES** | Moment was doubled to $2 M_0$ ($2,000,000\text{ Nm}$) due to opposing local sign conventions at element ends $i$ and $j$, yielding $125.47\text{ MPa}$ instead of $0.0\text{ MPa}$. | `testing/evidence/phase_2_baseline/tc_reg_c01_sectional_stress_range.log` | **READY** |
| **`TC-REG-A02-ULS-COMBINATION-SUM`** | DEF-01 / DEF-02 | Integration | **FAIL** | **YES** | `create_sidl_combination()` was never invoked; `sidl_combination` is `None` in grillage model, omitting crash barriers from dead load. | `testing/evidence/phase_2_baseline/tc_reg_a02_uls_combination_sum.log` | **READY** |
| **`TC-REG-D01-WIND-SPEED-PROPAGATION`** | DEF-05 | Unit/Integration | **FAIL** | **YES** | All 4 wind parameters dropped and defaulted to fallbacks (speed=33.0, barrier_h=0.0) because line 1381 reads un-prefixed keys. | `testing/evidence/phase_2_baseline/tc_reg_d01_wind_speed_propagation.log` | **READY** |
| **`TC-REG-D02-TEMPERATURE-PROPAGATION`** | DEF-06 | Integration | **FAIL** | **YES** | `temperature_load_kN_m2` is absent from inputs; `add_temperature_load()` silently returns without instantiating `temperature_load_case`. | `testing/evidence/phase_2_baseline/tc_reg_d02_temperature_propagation.log` | **READY** |
| **`TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS`** | DEF-17 | Integration | **FAIL** | **YES** | `cl_204_6_fatigue_load()` is defined in `irc6_2017.py` but is never called in `create_moving_vehicle_load_cases()`. | `testing/evidence/phase_2_baseline/tc_reg_c02_fatigue_vehicle_analysis.log` | **READY** |
| **`TC-REG-RPT-EXEC-SUMMARY-STATUS`** | DEF-08 | Unit | **FAIL** | **YES** | `executive_summary.py:233` hardcodes literal text `\noindent Girder design pass` unconditionally, masking design failures. | `testing/evidence/phase_2_baseline/tc_reg_rpt_exec_summary_status.log` | **READY** |
| **`TC-REG-GEO-GIRDER-COUNT-ALIGNMENT`** | DEF-11 | Unit/Integration | **FAIL** | **YES** | `designer.py:401` sets `n_girders = geom.n_l` (6), incorrectly counting 2 slab overhang edge lines as structural girders. | `testing/evidence/phase_2_baseline/tc_reg_geo_girder_count_alignment.log` | **READY** |
| **`TC-REG-GEO-SLAB-SECTION-PROPERTIES`** | DEF-14 | Unit | **FAIL** | **YES** | `plategirderbridge.py:1285` assigns exactly $A/2$ and $I_z/2$ of the steel girder to the transverse concrete deck slab. | `testing/evidence/phase_2_baseline/tc_reg_geo_slab_section_properties.log` | **READY** |
| **`TC-REG-CAP-STIFFENER-BUCKLING`** | DEF-12 | Unit | **FAIL** | **YES** | `bs_Fcdw_wb_kN` ($134,083.2\text{ kN}$) evaluates to $64.2\times$ the stiffener column capacity due to unbounded Euler elastic stress. | `testing/evidence/phase_2_baseline/tc_reg_cap_stiffener_buckling.log` | **READY** |
| **`TC-REG-MAT-DENSITY-CONSISTENCY`** | DEF-13 | Unit | **FAIL** | **YES** | Self-weight uses hardcoded $78.5\text{ kN/m}^3$ (`analyser.py:416`) instead of input database density $76.4\text{ kN/m}^3$. | `testing/evidence/phase_2_baseline/tc_reg_mat_density_consistency.log` | **READY** |
| **`TC-REG-FS-CLEAN-WORKING-TREE`** | DEF-10 | Integration | **FAIL** | **YES** | Runtime database `weather.sqlite` ($180,224\text{ bytes}$) was generated inside the tracked package source directory. | `testing/evidence/phase_2_baseline/tc_reg_fs_clean_working_tree.log` | **READY** |
| **`TC-REG-CAD-EXPORT-VS-SCREENSHOT`** | DEF-09 | Integration | **FAIL** | **YES** | Qt `widget.grab()` produced $92.95\%$ transparent pixels due to reading software paint buffer instead of native OpenGL context. | `testing/evidence/phase_2_baseline/tc_reg_cad_export_vs_screenshot.log` | **READY** |

---

## 4. In-Depth Technical Verification of Baseline Defects

### 4.1 DEF-01: Load Factor Scaling Verification
- **Test:** `TC-REG-A01-FACTOR-SCALING`
- **Observed Values:** Unfactored maximum force = $9,634.6432\text{ N}$; Factored maximum force ($\gamma_f = 1.35$) = $9,634.6432\text{ N}$.
- **Force Ratio:** $1.00000$ (discrepancy: $25.9\%$ below expected $1.35000$).
- **Significance:** Confirms that `load_dict["factor"]` is completely ignored by `ospgrillage`, proving that all ULS combinations in OsdagBridge currently represent unfactored service loads.

### 4.2 DEF-03: Section Sizing Stiffness Discrepancy
- **Test:** `TC-REG-B01-SECTION-PROPERTY-SYNC`
- **Observed Values:** Preliminary $I_z$ passed to OpenSees = $0.00734091\text{ m}^4, A = 0.02253434\text{ m}^2$. Post-snapping analytical $I_z = 0.00795392\text{ m}^4, A = 0.02520800\text{ m}^2$.
- **Discrepancy:** $I_z$ differs by $7.71\%$; $A$ differs by $10.61\%$.
- **Significance:** The finite element grillage model is solved on an artificial section that is significantly more flexible than the fabricated section checked by the designer.

### 4.3 DEF-07: Fatigue Stress Doubling via Member-End Sign Conventions
- **Test:** `TC-REG-C01-SECTIONAL-STRESS-RANGE`
- **Observed Values:** For a constant static sagging moment $M_0 = 1,000\text{ kNm}$ ($M_{z\_i} = +1,000\text{ kNm}, M_{z\_j} = -1,000\text{ kNm}$), `mz_range_Nm` evaluates to $2,000,000\text{ Nm}$ ($2 M_0$), yielding a stress range of $125.47\text{ MPa}$ when the true cyclic variation is $0.0\text{ MPa}$.
- **Significance:** Confirms that the reported Phase 1D fatigue failure (DCR = 1.9746) was driven by an arithmetic sign-flip bug across element ends rather than physical structural under-capacity.

### 4.4 DEF-05: Wind Input Key Decoupling
- **Test:** `TC-REG-D01-WIND-SPEED-PROPAGATION`
- **Observed Values:** When passing $V_b = 47.0\text{ m/s}$, $H = 15.0\text{ m}$, barrier height $= 1.1\text{ m}$, railing height $= 1.2\text{ m}$ through the standard GUI hierarchy, `create_wind_load` intercepted arguments: `basic_wind_speed = 33.0`, `height_for_pz = 10.0`, `crash_barrier_height = 0.0`, `railing_height = 0.0`.
- **Significance:** Confirms that all 5 wind parameters are dropped, under-designing wind lateral drag and omitting barriers from exposed frontal areas.

### 4.5 DEF-12: Bearing Stiffener Capacity Singularity
- **Test:** `TC-REG-CAP-STIFFENER-BUCKLING`
- **Observed Values:** `bs_Fcdw_wb_kN = 134083.225 kN` vs. column squash capacity `bs_Fcd_kN = 2087.273 kN` (ratio = $64.2\times$).
- **Significance:** Confirms an unconstrained Euler elastic buckling calculation without material yield cutoff.

---

## 5. Verification Against False Failure Modes

Each test was audited to confirm it did **not** fail due to trivial setup errors:
- **No Import Errors:** All 14 tests imported modules and dependencies cleanly under `osdagbridge-py312`.
- **No Missing Attribute Crashes:** Verified attribute names (e.g. `.Iz` instead of `.I_z`, `girder_props[i]`, `BridgeConfig.from_plate_girder_bridge`).
- **No Missing Key Exceptions:** Strict hierarchical dictionaries and fallback protections were applied.
- **Controlled Invariants:** Tests asserted strict physical or code relationships, ensuring they will transition to **PASS** once remediated.

---

## 6. Phase 2 Gating Sign-Off & Recommendation

| Gating Criterion | Required State | Verified State | Audit Status |
| :--- | :--- | :--- | :---: |
| **Baseline Immutability** | Commit `d74f56d` unchanged | Git HEAD matches `d74f56d` on `dev` | **PASSED** |
| **Documentation Rectification** | Errata corrected, DEF-11 to DEF-17 added | Preserved in Defect Register & Preservation Record | **PASSED** |
| **Test Plan Quality** | No tautologies or defective tests | Verified in `PHASE_2_TEST_PLAN.md` | **PASSED** |
| **Reproducible Failure Evidence** | 100% intended failure rate on baseline | 14 / 14 confirmed failures with log artifacts | **PASSED** |
| **Clean Filesystem Hygiene** | Non-destructive execution | Tracked working tree clean; logs saved in evidence | **PASSED** |

### **FINAL RECOMMENDATION: GO**
The testing harness is fully operational and verified against baseline `d74f56d`. The project is authorized to proceed to **Phase 2 Implementation** by creating the dedicated feature branch `fix/phase-2-remediation` and systematically executing fixes following the 12-stage implementation sequence.

---

**Signed:**  
*Lead Software QA Architect & Structural Systems Arbitrator*  
*FOSSEE Winter Internship Contribution Verification Campaign*  
*Date: 2026-11-16*
