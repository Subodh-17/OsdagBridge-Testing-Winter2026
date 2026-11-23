# PHASE 2.5 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`)  
**Controlling Document:** `reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  

---

## 1. Master Validation Matrix (All 15 Tests)

| # | Test Identifier | Defect ID | Baseline Expected | Baseline Observed | Manifest Match | Cand. (b) Correct | Cand. (c) Naive | Sensitivity Verdict | Gate Status |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | MATCH | BLOCKED | BLOCKED | **BLOCKED** | DEC-015 |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | MATCH | BLOCKED | BLOCKED | **BLOCKED** | DEC-018 |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | MATCH | BLOCKED | BLOCKED | **BLOCKED** | DEC-013 |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |

**Actionable Verification Gate:** 12 / 12 Actionable Tests Verified (100.0%)  
**Blocked Specifications:** 3 / 15 Tests Formally Blocked Pending Design Decisions  
**Overall Phase 2.5 Gate Status:** **PASSED**  

---

## 2. Detailed Technical Test Profiles

### 1. TC-REG-A01-FACTOR-SCALING
- **Defect:** Upstream `ospgrillage` ignores `load_factor` in `CompoundLoad` / `PointLoad` creation, resulting in un-factored force ratios ($1.0000$ observed vs $1.3500$ expected).
- **Condition (a) Baseline:** `BASELINE_FAIL` (force ratio = 1.00000).
- **Condition (b) Minimal Correct:** Scaled load magnitude by 1.35x. `PASS` (force ratio = 1.35000).
- **Condition (c) Naive / Wrong:** Scale factor 1.00. `BASELINE_FAIL` (force ratio = 1.00000).
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_a01_factor_scaling.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_a01_factor_scaling_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_a01_factor_scaling_c_naive.log`

### 2. TC-REG-B01-SECTION-PROPERTY-SYNC
- **Defect:** Solver grillage section properties remain out-of-sync with designed plate girder sections ($I_z$ error $\sim 7.40\%$, $A$ error $\sim 10.55\%$, web/flange depth mismatch $1340\text{ mm}$ vs $1342\text{ mm}$, and deflection $7.82\text{ mm}$ vs calibrated grillage target $7.22\text{ mm}$).
- **Analytical Bounds:** Single-beam upper bound $= 18.164\text{ mm}$; Courbon lower bound $= 4.541\text{ mm}$; Grillage calibrated target $= 7.218\text{ mm}$.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Synced section properties with plate formula torsional and bending constants ($I_y = 0.0002068\text{ m}^4$, $J = 1.815 \times 10^{-6}\text{ m}^4$). `PASS` (deflection 7.22 mm, dimension check passes).
- **Condition (c) Naive / Wrong:** Preserves unsynced preliminary sections. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_b01_section_property_sync.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_b01_section_property_sync_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_b01_section_property_sync_c_naive.log`

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect:** Static load case produces false cyclic stress ranges ($125.46\text{ MPa}$ envelope due to element end $-Mz_i$ and $+Mz_j$ sign flipping; $62.73\text{ MPa}$ per-LC treating static moment as range, instead of $0.0\text{ MPa}$).
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Evaluates sign-consistent element-end section moments ($-Mz_i$ / $+Mz_j$) and extracts $\max(M) - \min(M)$ across frequent load combinations divided by composite section modulus $Z_e$. Static case yields $\Delta \sigma = 0.00\text{ MPa}$. `PASS`.
- **Condition (c) Naive / Wrong:** Zeroes static envelope only while keeping per-LC calculation uncorrected. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_c01_sectional_stress_range.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_c01_sectional_stress_range_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_c01_sectional_stress_range_c_naive.log`

### 4. TC-REG-A02-ULS-COMBINATION-SUM
- **Defect:** Analysis combination `BASIC_1` ignores ULS load factors (observed shears match $1.0\text{DL} + 1.0\text{DW}$ with error $1.60 \times 10^{-7}\text{ N}$; total reaction $1736.6\text{ kN}$ vs factored target $2710.2\text{ kN}$); crash barrier load is completely omitted from the combination.
- **Convention:** Total applied resultant $2802.70\text{ kN}$. Explains IRC 6 Annex B Table B.1 vs Table B.2 convention (1.35 vs 1.75).
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Properly assembles factored ULS combinations including crash barrier load. `PASS`.
- **Condition (c) Naive / Wrong:** Assembles combination without factoring. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_a02_uls_combination_sum.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_a02_uls_combination_sum_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_a02_uls_combination_sum_c_naive.log`

### 5. TC-REG-EQ-LOAD-CONSERVATION
- **Defect:** Static force equilibrium and moment/centroid conservation violated in FE grillage load distribution:
  - Deck slab (DD): $+39.4\text{ kN}$ (+3.1% error).
  - Wearing course (DW): $+7.6\text{ kN}$ (+3.1% error).
  - Crash barrier line load: $-117.7\text{ kN}$ (-37.5% shortfall), centroid shift $\Delta x = +0.750\text{ m}$.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Cell-intersection bilinear load distribution (`_distribute_patch_load_fem` and `_distribute_line_load_fem`). Conserves 100% force and centroids within $0.05\%$ and $0.05\text{ m}$. `PASS`.
- **Condition (c) Naive / Wrong:** Distributes patch loads correctly but omits crash barrier line loads, leaving barrier shortfall and longitudinal centroid error. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_eq_load_conservation.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_eq_load_conservation_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_eq_load_conservation_c_naive.log`

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect:** Wind calculation arguments fall back to module defaults (speed $33.0\text{ m/s}$ vs $47.0\text{ m/s}$, height $10.0\text{ m}$ vs $15.0\text{ m}$, barrier $0.0\text{ m}$ vs $1.1\text{ m}$, railing $0.0\text{ m}$ vs $1.2\text{ m}$), yielding $P_z = 463.7\text{ N/m}^2$ instead of authentic $1039.6\text{ N/m}^2$.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Full propagation of wind parameters to IRC 6 Table 12 calculator. `PASS` ($P_z = 1039.6\text{ N/m}^2$).
- **Condition (c) Naive / Wrong:** Propagates wind speed only, leaving height and barrier at defaults. `BASELINE_FAIL` ($P_z = 940.6\text{ N/m}^2$).
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_d01_wind_speed_propagation.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_d01_wind_speed_propagation_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_d01_wind_speed_propagation_c_naive.log`

### 7. TC-REG-D02-TEMPERATURE-PROPAGATION
- **Status:** **BLOCKED** under **DEC-015**.
- **Reason:** Thermal load modeling (IRC 6 Cl. 215) is undecided in project specifications. `add_temperature_load()` reads unpopulated `'temperature_load_kN_m2'` key and leaves `temperature_load_case` as `None`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_d02_temperature_propagation.log`

### 8. TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Status:** **BLOCKED** under **DEC-018**.
- **Defect Label:** DEF-17 (Architectural Gap / Feature Omission).
- **Reason:** OsdagBridge has no implementation linking the IRC 6 Cl. 204.6 fatigue vehicle moving load to grillage moving load analysis or `designer.py` fatigue demand/utilization extraction.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_c02_fatigue_vehicle_analysis.log`

### 9. TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect:** `executive_summary.py` hardcodes `\noindent Girder design pass` in the LaTeX output unconditionally, causing discrepancies when single girders or components fail.
- **Condition (a) Baseline:** `BASELINE_FAIL` (fails across Scenarios 2A, 2B, 3, 4, 5, 6).
- **Condition (b) Minimal Correct:** Dynamic status derivation across all girders G1-G6 and all components. `PASS` across all 6 scenarios.
- **Condition (c) Naive / Wrong:** Checks G1 only, passing Scenario 2B (edge girder failure) but failing Scenario 2A (interior girder G3 failure). `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_rpt_exec_summary_status.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_rpt_exec_summary_status_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_rpt_exec_summary_status_c_naive.log`

### 10. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect:** `designer.py:401` sets `n_girders = geom.n_l` (6), incorrectly counting 2 slab overhang edge lines as structural girders for a 4-girder bridge.
- **Condition (a) Baseline:** `BASELINE_FAIL` (`bcfg.geometry.n_girders = 6`, expected 4).
- **Condition (b) Minimal Correct:** Sets `n_girders` from `bridge.input_dict.get('number_of_girders')`. `PASS` (4 girders).
- **Condition (c) Naive / Wrong:** Sets `n_girders = 0`. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_geo_girder_count_alignment.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_geo_girder_count_alignment_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_geo_girder_count_alignment_c_naive.log`

### 11. TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Status:** **BLOCKED** under **DEC-013**.
- **Reason:** Transverse deck slab representation model is undecided in project documentation. Baseline assigns `girder/2` ($I_z = 0.00367\text{ m}^4$), which is mechanically invalid for concrete deck, but exact transformed vs concrete material and cracked/torsion model requires engineering sign-off.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_geo_slab_section_properties.log`

### 12. TC-REG-CAP-STIFFENER-BUCKLING
- **Defect:** Bearing stiffener capacity formula in `compute_bearing_stiffener` uses stiffener moment of inertia ($I_{ys}$) instead of web strip radius of gyration ($r_{wb} = t_w / \sqrt{12}$), yielding massive unphysical capacities ($214,533.2\text{ kN}$ on Geometry 1 vs oracle $63.4\text{ kN}$, squash load $1918.8\text{ kN}$).
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Genuine IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 web strip Perry-Robertson column buckling curve c. `PASS` (Geo 1: 63.4 kN; Geo 2: 158.5 kN).
- **Condition (c) Naive / Wrong:** Squash load formula $(f_y / \gamma_{m0}) \times A_{wb} / 1000$ (ignores column buckling). `BASELINE_FAIL` (1743.2 kN vs oracle 63.4 kN).
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_cap_stiffener_buckling.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_cap_stiffener_buckling_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_cap_stiffener_buckling_c_naive.log`

### 13. TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect:** Self-weight resultant ($169.8\text{ kN}$) matches hardcoded $78.5\text{ kN/m}^3$ ($169.8\text{ kN}$) instead of user-specified density $70.0\text{ kN/m}^3$ ($151.4\text{ kN}$).
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Reads user-specified density from input dict. `PASS` ($151.4\text{ kN}$).
- **Condition (c) Naive / Wrong:** Retains hardcoded $78.5\text{ kN/m}^3$. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_mat_density_consistency.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_mat_density_consistency_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_mat_density_consistency_c_naive.log`

### 14. TC-REG-FS-CLEAN-WORKING-TREE
- **Defect:** `ui_loc.DB_PATH` resolves inside package tree (`src/.../weather.sqlite`), `Database()` default constructor creates unanchored `weather.sqlite` in `os.getcwd()`, and package tree is vulnerable to read-only installation failures.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Anchors both `ui_loc.DB_PATH` and `Database.__init__` default constructor to user app data directory. `PASS`.
- **Condition (c) Naive / Wrong:** Anchors `ui_loc.DB_PATH` but leaves `Database.__init__` unanchored, creating files in `os.getcwd()`. `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_fs_clean_working_tree.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_fs_clean_working_tree_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_fs_clean_working_tree_c_naive.log`

### 15. TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Type:** Environment Verification Check.
- **Verification:** Offscreen OCC `Viewer3d.ExportToImage` generates genuine non-blank 3D CAD renders ($\text{std} = 66.6$, 3 distinct colors).
- **Condition (a) Baseline:** `PASS`.
- **Condition (b) Minimal Correct:** Baseline OCC export. `PASS`.
- **Condition (c) Naive / Wrong:** Blank uniform image ($\text{std} = 0.0$). `BASELINE_FAIL`.
- **Evidence Logs:**
  - `testing/evidence/phase_2_5/baseline/tc_reg_cad_export_vs_screenshot.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_cad_export_vs_screenshot_b_correct.log`
  - `testing/evidence/phase_2_5/candidates/tc_reg_cad_export_vs_screenshot_c_naive.log`

---

## 3. Summary of Verification Gates

| Gate Metric | Threshold Requirement | Observed Result | Status |
|:---|:---:|:---:|:---:|
| Total Test Cases Evaluated | 15 | 15 | MET |
| Baseline Manifest Alignment | 15 / 15 (100%) | 15 / 15 (100%) | **PASSED** |
| Actionable Tests Sensitivity Verified | 12 / 12 (100%) | 12 / 12 (100%) | **PASSED** |
| Formal Specifications Blocked | 3 | 3 (DEC-013, DEC-015, DEC-018) | **MET** |
| Application Source Tree State | Clean / Unmodified | Clean (`d74f56d` on `dev`) | **PASSED** |
| Baseline Suite Exit Code | 0 | 0 | **PASSED** |
| Sensitivity Runner Exit Code | 0 | 0 | **PASSED** |
