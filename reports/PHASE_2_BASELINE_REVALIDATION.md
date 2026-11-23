# PHASE 2 BASELINE REVALIDATION REPORT

**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `source\OsdagBridge` at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`)  
**Reference Environment:** `osdagbridge-py312` (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | Python 3.12.16)  
**Controlling Audit Document:** `PHASE_2_REGRESSION_INDEPENDENT_AUDIT.md`  
**Date:** 2026-11-16  
**Final Status:** **BASELINE REVALIDATED — READY FOR REMEDIATION**  

---

## 1. Executive Summary

Following the full repair of the regression test suite, the entire 14-test suite was re-executed against the pristine, untouched upstream commit `d74f56d`.

### Revalidation Summary:
- **Total Tests Executed:** 14
- **Passed (Clean Application Behavior):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`, confirming that the application's native `Viewer3d.ExportToImage` functions properly and that the Phase 1D 92.95% transparent PNG was an artifact of Qt `widget.grab()`).
- **Failed (Confirmed Genuine Baseline Defects):** 13
- **Blocked (Setup / Runtime Errors):** 0
- **Process Exit Code:** `1` (Non-zero exit code correctly triggered by failed baseline tests).
- **Application Source Modifications:** 0 lines changed (`git status` clean).

---

## 2. Test-by-Test Execution Results

| Test Identifier | Target Defect | Application Entry Point | Inputs & Preconditions | Expected Engineering Behavior | Actual Baseline Result | Status | Evidence Log | Genuine Defect Demonstrated? |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **`TC-REG-A01-FACTOR-SCALING`** | DEF-01 | `og.create_load_case`, `lc.add_load(line_load, load_factor=1.35)`, `model.analyze()` | Standard 24m grillage; identical line loads added with factor 1.0 vs 1.35. | Max force ratio $F_{f} / F_{u} == 1.35000$. | Force ratio is $1.00000$ ($9634.64\text{ N}$ both cases). Factor dropped in `ospgrillage`. | **FAIL** | [`tc_reg_a01_factor_scaling.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_a01_factor_scaling.log) | **YES** (Upstream `ospgrillage`) |
| **`TC-REG-B01-SECTION-PROPERTY-SYNC`** | DEF-03 | `PlateGirderBridge.set_input()`, `_resolve_optimized_bounds_to_mm()`, `_stage_grillage_setup()` | `BASE_CFG` with snapped plates $D=1.34\text{ m}$, $t_f=0.018\text{ m}$, $b_f=0.41\text{ m}$, $t_w=0.008\text{ m}$. | Assigned $I_z, A$ for all girders match snapped section ($I_z=0.00792758\text{ m}^4$, $A=0.025192\text{ m}^2$, $d_w=1.304\text{ m}$). | Assigned preliminary $I_z=0.00734091\text{ m}^4$ (diff 7.40%), $A=0.022534\text{ m}^2$ (diff 10.55%), input dict $d_w=1.306\text{ m}$ (stale). | **FAIL** | [`tc_reg_b01_section_property_sync.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_b01_section_property_sync.log) | **YES** |
| **`TC-REG-C01-SECTIONAL-STRESS-RANGE`** | DEF-07 | `_extract_demands_from_analysis_results(analysis_res, bcfg)` | Controlled frequent load case with constant sagging moment $M_0 = 1000\text{ kNm}$ ($M_{z\_i} = +M_0, M_{z\_j} = -M_0$). | Cyclic stress range under static loading MUST be $0.0\text{ MPa}$ ($\Delta \sigma \le 1.0\text{ MPa}$). | Opposite element ends $[+M_0, -M_0]$ flattened across girders, doubling moment to $2000\text{ kNm}$, yielding $\sigma_{range} = 125.46\text{ MPa}$. | **FAIL** | [`tc_reg_c01_sectional_stress_range.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_c01_sectional_stress_range.log) | **YES** |
| **`TC-REG-A02-ULS-COMBINATION-SUM`** | DEF-01 / DEF-02 | `BridgeGrillageModel.create_uls_combinations()`, `_load_case_resultant_kN()` | `BASE_CFG` dead loads + surfacing; invoke combination generation. | ULS combination includes SIDL and applies factors: $R_{ULS} == \sum \gamma_i R_i$. | `create_sidl_combination()` never called (`sidl_combination is None`), and load factors dropped in `_copy_loads`. | **FAIL** | [`tc_reg_a02_uls_combination_sum.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_a02_uls_combination_sum.log) | **YES** |
| **`TC-REG-D01-WIND-SPEED-PROPAGATION`** | DEF-05 | `PlateGirderBridge.add_wind_loads()`, intercepting `create_wind_load` | Authentic UI keys: `loading.wind_load.basic_wind_speed = 47.0`, `height = 15.0`, `barrier = 1.1`, `railing = 1.2`. | All 4 arguments propagate to `create_wind_load`; $P_z = 945.7\text{ N/m}^2$ (IRC 6 Table 12). | Reads bare un-prefixed keys; drops all 4 to fallbacks (speed=33.0, height=10.0, barrier=0.0, railing=0.0); $P_z = 463.7\text{ N/m}^2$. | **FAIL** | [`tc_reg_d01_wind_speed_propagation.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_d01_wind_speed_propagation.log) | **YES** |
| **`TC-REG-D02-TEMPERATURE-PROPAGATION`** | DEF-06 | `PlateGirderBridge.add_temperature_load()` | Authentic UI temperature keys: `max_temp = 45.0`, `min_temp = 5.0`, $\alpha_{steel}, \alpha_{conc}$. | Temperature load case created on grillage model with non-zero resultant force. | Looks for `temperature_load_kN_m2`; silently returns None without creating `temperature_load_case`. | **FAIL** | [`tc_reg_d02_temperature_propagation.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_d02_temperature_propagation.log) | **YES** |
| **`TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS`** | DEF-17 | `PlateGirderBridge.add_vehicle_load_cases_from_combinations()` | `BASE_CFG` with `loading.live_load.fatigue = True`. | Moving vehicle cases include IRC 6 Cl. 204.6 fatigue vehicle load case. | Only Class A and Class 70R vehicle cases generated; fatigue vehicle completely omitted. | **FAIL** | [`tc_reg_c02_fatigue_vehicle_analysis.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_c02_fatigue_vehicle_analysis.log) | **YES** |
| **`TC-REG-RPT-EXEC-SUMMARY-STATUS`** | DEF-08 | `executive_summary(input_dict, output_dict, fig_paths)` | Output dictionary containing failing design check (`fatigue_check = False`, DCR = 1.9746). | Executive summary must NOT state unconditional `Girder design pass` when a design check fails. | Generates literal LaTeX `\noindent Girder design pass` unconditionally, masking design failure. | **FAIL** | [`tc_reg_rpt_exec_summary_status.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_rpt_exec_summary_status.log) | **YES** |
| **`TC-REG-GEO-GIRDER-COUNT-ALIGNMENT`** | DEF-11 | `BridgeConfig.from_plate_girder_bridge(bridge)` | Standard 4-girder bridge configuration. | `bcfg.geometry.n_girders == bridge._girder_count() == 4`. | `designer.py:401` sets `n_girders = geom.n_l` (6), counting 2 overhang edge lines as main girders. | **FAIL** | [`tc_reg_geo_girder_count_alignment.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_geo_girder_count_alignment.log) | **YES** |
| **`TC-REG-GEO-SLAB-SECTION-PROPERTIES`** | DEF-14 | `PlateGirderBridge._transverse_section()` | Standard bridge configuration ($t_s = 0.25\text{ m}$). | Transverse properties derived from concrete slab strip model ($I_{slab} \approx 0.001302\text{ m}^4$) and $\ne \text{girder}/2$. | `_transverse_section()` assigns preliminary steel girder $I_z/2 = 0.00367046\text{ m}^4$ and $A/2 = 0.01126717\text{ m}^2$. | **FAIL** | [`tc_reg_geo_slab_section_properties.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_geo_slab_section_properties.log) | **YES** |
| **`TC-REG-CAP-STIFFENER-BUCKLING`** | DEF-12 | `IRC22CapacityCalculator.compute_bearing_stiffener()` | Support reaction $R = 305\text{ kN}$, $t_q = 10\text{ mm}$, $H = 200\text{ mm}$. | Web buckling capacity $F_{cdw,wb} \le \frac{f_y}{\gamma_{m0}} A_{wb} = 1918.8\text{ kN}$ (material squash yield bound). | Evaluates to $134,083.2\text{ kN}$ ($69.9\times$ maximum yield capacity) due to unreduced Euler elastic stress. | **FAIL** | [`tc_reg_cap_stiffener_buckling.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_cap_stiffener_buckling.log) | **YES** |
| **`TC-REG-MAT-DENSITY-CONSISTENCY`** | DEF-13 | `BridgeGrillageModel.create_self_weight_load()` | Distinct user input density: `material.girder.density = 70.0\text{ kN/m}^3`. | Total resultant self-weight load matches user input density ($151.4\text{ kN}$). | Calculates self weight using hardcoded constant $78.5\text{ kN/m}^3$, producing $169.8\text{ kN}$ (12.15% error). | **FAIL** | [`tc_reg_mat_density_consistency.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_mat_density_consistency.log) | **YES** |
| **`TC-REG-FS-CLEAN-WORKING-TREE`** | DEF-10 | `Database.connect()` in isolated temporary directory | Run database connection in clean temp workspace. | Database connection must not create unanchored SQLite files in local execution directory. | Creates $180,224\text{ byte}$ `weather.sqlite` in current working directory due to unanchored relative path. | **FAIL** | [`tc_reg_fs_clean_working_tree.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_fs_clean_working_tree.log) | **YES** |
| **`TC-REG-CAD-EXPORT-VS-SCREENSHOT`** | DEF-09 | `OCC.Display.OCCViewer.Viewer3d.ExportToImage()` | Create 3D BRep box geometry in offscreen Viewer3d and export image. | Native CAD export API produces non-empty, opaque, valid RGB image file. | `Viewer3d.ExportToImage()` successfully produces $656 \times 519$ 100% opaque RGB PNG ($4324\text{ bytes}$). | **PASS** | [`tc_reg_cad_export_vs_screenshot.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_repaired/tc_reg_cad_export_vs_screenshot.log) | **NO** (Harness Flaw Verified) |

---

## 3. Unresolved Engineering Decisions for Phase 3 Remediation

The audit and revalidation campaign have isolated three engineering decisions that must be explicitly established during remediation:

1. **Steel Density Standard Convention (DEF-13):**
   - The SQLite database (`Steel_Grade_Properties`) specifies $78,500\text{ N/m}^3 = 78.5\text{ kN/m}^3$.
   - The UI input layer defaults to $76.4\text{ kN/m}^3$ ($7.8\text{ t/m}^3 \times 9.8\text{ m/s}^2$).
   - *Remediation Rule:* The solver must respect the user's explicit input density (`material.girder.density`). If the user specifies $76.4$ or $78.5$, that exact value must propagate to `create_self_weight_load()`.

2. **Temperature Load Mechanical Formulation (DEF-06):**
   - The application's analyser implements temperature as a transverse patch pressure `temperature_load_kN_m2` over the deck quad.
   - IRC:6-2017 Cl. 215 defines temperature as uniform overall range $\Delta T$ and temperature gradient through the deck depth.
   - *Remediation Rule:* To preserve compatibility with the grillage solver, `PlateGirderBridge.add_temperature_load()` must compute the equivalent load intensity from $\Delta T = T_{max} - T_{min}$ and thermal expansion coefficient $\alpha$, populating `temperature_load_case`.

3. **Transverse Deck Slab Modeling (DEF-14):**
   - Currently, transverse members are assigned $A/2$ and $I_z/2$ of the steel girder.
   - *Remediation Rule:* In accordance with Hambly (Chapter 5), transverse members must represent the concrete deck slab: flexural inertia $I = \frac{s_t t_{slab}^3}{12}$ (using transverse spacing $s_t$ and deck thickness $t_{slab}$), transformed to steel equivalent using modular ratio $m = E_s / E_c \approx 6.06$ to $7.14$, or assigned concrete material properties directly.

---

## 4. Changed-Files Inventory

No application source files were altered. All changes were strictly confined to test specifications, test harness scripts, and audit documentation:

```
Modified:
  testing/test_cases/baseline_regression/run_all_baseline_tests.py  (Repaired test harness)
  PROGRESS.md                                                       (Phase 2 progress tracking)
  DECISIONS.md                                                      (Added DEC-010 and DEC-011)
  CHANGELOG.md                                                      (Recorded Phase 2 repair)

Created:
  reports/PHASE_2_REGRESSION_SUITE_REPAIR.md                        (Detailed reconciliation report)
  reports/PHASE_2_BASELINE_REVALIDATION.md                          (This baseline revalidation report)
  testing/evidence/phase_2_repaired/                                (14 logs + repaired_regression_summary.json)
```

---

## 5. Final Verdict

### **READY FOR REMEDIATION**

The Phase 2 regression suite is fully repaired, rigorous, and verified:
1. Every test invokes actual application code paths with genuine inputs and observable outputs.
2. Every expected value is grounded in traceable physical, code-based, or geometric principles.
3. Zero tests rely on source-code string grepping, formula copying, or static file artifacts.
4. The test runner uses workspace-relative paths, correctly isolates errors, and exits with code `1` on defective baseline.
5. All 13 genuine application and upstream defects fail cleanly for their documented root causes with 0 setup crashes.
6. The false-positive CAD transparency finding was definitively isolated to the Phase 1D test harness's `widget.grab()` method.

The suite is immediately ready to serve as the strict gating mechanism for the sequential 12-stage defect remediation branch (`fix/phase-2-remediation`).
