# PHASE 3 — Defect Traceability Matrix and Ground-Truth Source Analysis (Revision 3.0)

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Revision:** Revision 3.0 (Post-Re-Audit Re-Baseline)  
**Controlling Documents:**
- `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_REV2_REAUDIT.md` (by independent auditor Claude)
- `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md` (by independent auditor Claude)
**Historical Revision Archive:**
- `reports/phase_3/v1_original/PHASE_3_DEFECT_TRACEABILITY_MATRIX.md` (Revision 1.0)
- `reports/phase_3/PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV2.md` (Revision 2.0)
**Date:** 2026-11-18  

---

## 1. Master Defect Register Summary (18 Cataloged Defects & Sub-Defects)

Following independent auditor Claude's second audit ([`reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_REV2_REAUDIT.md`](file:///F:/FOSSEE%20internship/reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_REV2_REAUDIT.md)), the Defect Register has been comprehensively expanded to formally track **18 cataloged defects, sub-defects, and architectural gaps**, including the newly cataloged Wearing Course Transverse Extent defect (`DEF-20`), the decomposition of Live-Load Factor Composition into three distinct sub-defects (`DEF-19a`, `DEF-19b`, `DEF-19c`), and the separately scoped latent defect `DEF-LATENT-ZP`:

| Defect ID | Defect Title | Primary Source Module | Line Range | Severity | Baseline Status | Governing Standard |
|:---:|:---|:---|:---:|:---:|:---:|:---|
| **DEF-01** | Load Factor Scaling Omission in `ospgrillage` Load Combinations | `src/ospgrillage/osp_grillage.py`<br>`src/ospgrillage/load.py` | 1934–1960<br>1161–1168 | Critical | `BASELINE_FAIL` | IRC:6-2017 Table B.2 |
| **DEF-02** | Crash Barrier Superimposed Dead Load Omission in Combinations | `analyser.py`<br>`plategirderbridge.py` | 1532–1558<br>1336–1339 | Critical | `BASELINE_FAIL` | IRC:6-2017 Cl. 202 / Table B.2 |
| **DEF-03** | Section Property Desynchronization Between Snapped Plates and Grillage | `plategirderbridge.py`<br>`initial_sizing.py` | 1260–1277<br>Unverified | Critical | `BASELINE_FAIL` | IS 800:2007 Cl. 8 / Beam Theory |
| **DEF-05** | Wind Parameter Propagation Loss (Basic Wind Speed, Heights & Terrain) | `plategirderbridge.py`<br>`analyser.py` | 1380–1416<br>1310–1370 | High | `BASELINE_FAIL` | IRC:6-2017 Cl. 209 / Table 12 |
| **DEF-06** | Temperature Load Modeling Omission / Vertical Pressure Fallback | `plategirderbridge.py`<br>`analyser.py` | 1869–1877<br>905–938 | High | `BLOCKED` (DEC-015) | IRC:6-2017 Cl. 215 |
| **DEF-07** | Sectional Fatigue Stress Range End-Sign Doubling & Zero-Clamping | `designer.py` | 2976–2996 | Critical | `BASELINE_FAIL` | IRC:22-2015 Cl. 604.5 / 605.4 |
| **DEF-08** | Executive Summary Emits Hardcoded Static "Pass" Narrative | `executive_summary.py` | 233–236 | Medium | `BASELINE_FAIL` | Software Reliability / QA |
| **DEF-09** | Offscreen OpenCASCADE Viewport Image Export Verification | Test Environment Harness | 2950–2995 | Low | `PASS` (Harness) | OCC 3D Display Reliability |
| **DEF-10** | Reference Database Runtime Materialization & Package Tree Mutation | `database.py`<br>`ui_fields_project_location.py` | 12–30, 356<br>16–29 | Medium | `BASELINE_FAIL` | POSIX/Windows Packaging |
| **DEF-11** | Girder Count Geometry Misalignment (Edge Lines Counted in Config) | `designer.py`<br>`plategirderbridge.py` | 401, 413<br>1112–1115 | Medium | `BASELINE_FAIL` | Grillage Mesh Topology |
| **DEF-12** | Bearing Stiffener Web Buckling Capacity Formula Anomaly | `designer.py` | 1664–1672 | Critical | `BASELINE_FAIL` | IS 800:2007 Cl. 8.7.3.1 / IRC:24 |
| **DEF-13** | Hardcoded Structural Steel and Deck Concrete Density Propagation | `analyser.py`<br>`plategirderbridge.py` | 10, 416<br>1332–1333 | Medium | `BASELINE_FAIL` | IRC:6-2017 Cl. 202.1 |
| **DEF-14** | Transverse Concrete Deck Slab Assigned Steel Girder Properties | `plategirderbridge.py` | 1279–1291 | High | `BLOCKED` (DEC-013) | Grillage Structural Mechanics |
| **DEF-17** | Fatigue Vehicle Moving Load Analysis Pipeline Omission | `analyser.py`<br>`designer.py` | 1612–1660<br>2972–2985 | Critical | `BLOCKED` (DEC-018) | IRC:6-2017 Cl. 204.6 |
| **DEF-18** | Non-Conservation of Static Load Equilibrium & End-Bay Drop | `src/ospgrillage/osp_grillage.py` | 1576–1579<br>1674–1729, 1795–1858 | Critical | `BASELINE_FAIL` | Static Equilibrium ($\Sigma F_y = 0$) |
| **DEF-19** | Live-Load Factor Composition Omission (Lane Factors & DLA Dropped) | `analyser.py` | 1803, 1827–1841, 2025 | High | `BASELINE_FAIL` (Latent) | IRC:6-2017 Cl. 204.4 / Cl. 208 |
| ↳ **DEF-19a** | `cl_208_3` Truthy String Check Hardcoding 0.10 Impact for All Vehicles | `irc6_2017.py` | 534, 543 | High | `BASELINE_FAIL` (Latent) | IRC:6-2017 Cl. 208.3 |
| ↳ **DEF-19b** | Lane Reduction Factors Indexed Per-Vehicle Within Type, Not Per Lane | `analyser.py`<br>`keyfile.py` | 1827–1828<br>119 | Medium | `BASELINE_FAIL` (Latent) | IRC:6-2017 Cl. 205 / Table 6A |
| ↳ **DEF-19c** | Analysis Code (0.10) vs Report Chapter 3 (0.24) Impact Discrepancy | `analyser.py`<br>`chap3.py` | 1803<br>88–116 | Medium | `BASELINE_FAIL` (Latent) | Technical Documentation QA |
| **DEF-20** | Wearing Course Transverse Extent (Full Deck Width vs Carriageway Clear Width) | `plategirderbridge.py`<br>`load_placement.py` | 1334<br>133–139 | Medium | `BASELINE_FAIL` | IRC:5 Cl. 104 / IRC:6 Cl. 202 |
| **DEF-LATENT-ZP** | Transverse Coordinate Indexing in Line Load Intensity Interpolation (`zp = point_coordinate[0]`) | `src/ospgrillage/load.py` | 710 | Medium | `UNRESOLVED` (Latent) | Vector Calculus / Math QA |

---

## 2. Decoupled Structural Test Fixtures Specification

To resolve Claude's audit findings (§2.6, §7; Findings R2-01, R2-02, R2-03), Revision 3.0 rigorously separates the **Hand Calculation Test Fixture** from the **Sealed Bridge Pipeline Fixture**. Mixing these two geometries produced the arithmetic and oracle errors in Revision 2.0.

### 2.1 Fixture A: Hand Calculation Test Fixture (Pure Verification Geometry)
Used for standalone unit verification of cross-section integration, beam deflection, and closed-form load combinations:
- **Span Length:** $L = 24.000\text{ m}$ (simply supported, skew $0^\circ$).
- **Overall Deck Width:** $W_{\text{deck}} = 8.500\text{ m}$.
- **Carriageway Clear Width:** $W_{\text{cw}} = 7.500\text{ m}$ (centered between crash barriers).
- **Deck Slab Thickness:** $t_{\text{deck}} = 0.250\text{ m}$ ($250\text{ mm}$).
- **Wearing Course Thickness:** $t_{\text{wc}} = 0.050\text{ m}$ ($50\text{ mm}$).
- **Material Densities:**
  - Steel: $\rho_s = 78.50\text{ kN/m}^3$ (or user-injected custom $\rho_{s,\text{user}} = 70.00\text{ kN/m}^3$).
  - Concrete Deck Slab: $\rho_c = 24.50\text{ kN/m}^3$.
  - Asphalt Wearing Course: $\rho_{\text{wc}} = 24.00\text{ kN/m}^3$.
- **Girder Cross-Section (Fixed Plates):**
  - Web: $d_w = 1300\text{ mm}, t_w = 10\text{ mm}$.
  - Top Flange: $b_{ft} = 400\text{ mm}, t_{ft} = 16\text{ mm}$.
  - Bottom Flange: $b_{fb} = 500\text{ mm}, t_{fb} = 26\text{ mm}$.
  - Total Section Depth: $D = 1342\text{ mm}$.
- **Derived Closed-Form Bare-Steel Section Properties:**
  $$A = b_{ft} t_{ft} + b_{fb} t_{fb} + d_w t_w = 6400 + 13000 + 13000 = 32,400\text{ mm}^2 = \mathbf{0.032400\text{ m}^2}$$
  $$\bar{y}_{\text{bot}} = \frac{13000(13) + 13000(676) + 6400(1334)}{32400} = \mathbf{0.539957\text{ m}} \quad (539.957\text{ mm})$$
  $$I_z = \mathbf{0.0097174\text{ m}^4} \quad (9.7174 \times 10^9\text{ mm}^4), \quad I_y = \mathbf{0.0003563\text{ m}^4} \quad (3.5628 \times 10^8\text{ mm}^4)$$
- **Applied Static Dead Loads (Hand Fixture):**
  1. *Girder Self-Weight ($SW$):* $P_{SW} = 4 \times 24.0 \times 0.032400 \times 78.5 = \mathbf{244.166\text{ kN}}$ (or $217.728\text{ kN}$ at $\rho=70.0$).
  2. *Concrete Deck Slab ($DD$):* $P_{DD} = 24.0 \times 8.50 \times 0.25 \times 24.5 = \mathbf{1249.500\text{ kN}}$.
  3. *Wearing Course ($DW$ - Carriageway Clear Width $7.5\text{ m}$):* $P_{DW} = 24.0 \times 7.50 \times 0.05 \times 24.0 = \mathbf{216.000\text{ kN}}$.
  4. *Crash Barrier ($CB$):* $2 \times 24.0 \times 6.54 = \mathbf{313.920\text{ kN}}$.
  5. *Total Applied Physical Dead Load:*
     $$\sum P_{\text{applied}} = 244.166 + 1249.500 + 216.000 + 313.920 = \mathbf{2023.586\text{ kN}}$$
  6. *Authoritative Factored ULS Resultant (`BASIC_1` Reconciled - Finding R2-01):*
     $$P_{\text{ULS, B1}} = 1.35 \times (P_{SW} + P_{DD} + P_{CB}) + 1.75 \times P_{DW}$$
     $$P_{\text{ULS, B1}} = 1.35 \times (244.166 + 1249.500 + 313.920) + 1.75 \times (216.000) = 1.35 \times (1807.586) + 378.000 = \mathbf{2818.242\text{ kN}}$$
     *(Finding R2-01 Discrepancy Note: Revision 2.0 stated $2788.751\text{ kN}$, an arithmetic error of $-29.49\text{ kN}$ / $-1.05\%$. The exact closed-form value is $2818.242\text{ kN}$).*
  7. *Under Production Code DW ($8.5\text{ m}$ Full Deck Width - Finding R2-02):*
     $$P_{DW,\text{prod}} = 24.0 \times 8.50 \times 0.05 \times 24.0 = \mathbf{244.800\text{ kN}}$$
     $$P_{\text{ULS, B1, prod}} = 1.35 \times (1807.586) + 1.75 \times (244.800) = 2440.241 + 428.400 = \mathbf{2868.642\text{ kN}}$$

---

### 2.2 Fixture B: Sealed Bridge Pipeline Fixture (Production Regression Geometry)
Used for regression of the actual `PlateGirderBridge` pipeline execution, matching sealed evidence from Phase 2.12–2.13:
- **Span Length:** $L = 24.000\text{ m}$, Width $W = 8.500\text{ m}$, 4 girders at spacing $2.133\text{ m}$.
- **Preliminary Sizing Cross-Section:** $A = 0.022534\text{ m}^2 \implies P_{SW,\text{prelim}} = 4 \times 24.0 \times 0.022534 \times 78.5 = \mathbf{169.819\text{ kN}}$ (sealed EQ log line 15).
  *(Historical note on 165.28 kN: In A02 log line 21, SW is listed as $165.28\text{ kN}$, which corresponds to un-snapped sizing area $A = 0.021932\text{ m}^2$).*
- **Snapped Plate Girder Cross-Section (Sealed B01 Log):**
  - Web: $d_w = 1304\text{ mm}, t_w = 8\text{ mm}$.
  - Top Flange: $b_{ft} = 350\text{ mm}, t_{ft} = 14\text{ mm}$.
  - Bottom Flange: $b_{fb} = 450\text{ mm}, t_{fb} = 22\text{ mm}$.
  - Snapped Area: $A_{\text{snapped}} = \mathbf{0.025192\text{ m}^2}$ ($25,192\text{ mm}^2$).
  - Self-Weight at $\rho_s = 78.5\text{ kN/m}^3$: $P_{SW} = 4 \times 24.0 \times 0.025192 \times 78.5 = \mathbf{189.847\text{ kN}}$.
  - Self-Weight at $\rho_s = 70.0\text{ kN/m}^3$: $P_{SW} = 4 \times 24.0 \times 0.025192 \times 70.0 = \mathbf{169.290\text{ kN}}$.
- **Factored ULS Resultant on Sealed Snapped Bridge (at $\rho_s=78.5, \rho_c=24.5, DW=216.0\text{ kN}$):**
  $$P_{\text{ULS, B1, sealed}} = 1.35 \times (189.847 + 1249.500 + 313.920) + 1.75 \times (216.000) = 1.35 \times (1753.267) + 378.000 = \mathbf{2744.910\text{ kN}}$$
  *(With production DW $244.800\text{ kN}$: $P_{\text{ULS, B1, sealed, prod}} = 2366.910 + 428.400 = \mathbf{2795.310\text{ kN}}$).*

---

## 3. Exhaustive Technical Profiles for All Defects

---

### DEF-01: Load Factor Scaling Omission in `ospgrillage` Load Combinations
1. **Observation & Call Chain:** Force scaling factors passed to `LoadCase.add_load(load, load_factor=gamma)` had zero effect on OpenSees nodal loads.
   - Loop Location: `src/ospgrillage/osp_grillage.py:1934–1960` (in `_distribute_load_types_to_model`).
   - Storage Location: `src/ospgrillage/load.py:1166–1168` (`add_load` sets `load_dict.setdefault("factor", load_factor)`).
   - Downstream Copy Sites: `analyser.py:2344–2348` (`_copy_loads` in `create_uls_combinations`), `analyser.py:2539–2543` (in `create_sls_combinations`).
2. **Baseline Behavior:** `osp_grillage.py:1934` loops over `load_groups` and extracts `load_dict["load"]`, but ignores `load_dict["factor"]`. Force ratio remains $1.00000$ instead of $1.35000$.
3. **Proposed Fix Specification:** In `osp_grillage.py:1934`, retrieve `fac = load_dict.get("factor", 1.0)` and scale point, line, and patch load intensities prior to element distribution. In `analyser.py:2348`, compound factors: `factor = existing_factor * float(new_factor)`.

---

### DEF-02: Crash Barrier Superimposed Dead Load Omission in Combinations
1. **Observation & Call Chain:** Crash barrier line loads ($313.92\text{ kN}$) omitted from `BASIC_1`.
   - Omission Site: `plategirderbridge.py:1336–1339` (`create_crash_barrier_load()` called, but `create_sidl_combination()` is never invoked).
   - Combination Assembly: `analyser.py:1532–1558` (`create_dead_load_combination` queries `self.sidl_combination`, which is `None`).
2. **Baseline Behavior:** Observed barrier contribution in baseline combination is **$-708.74\text{ kN}$** (sealed log `tc_reg_a02_uls_combination_sum.log`).
3. **Proposed Fix Specification:** In `plategirderbridge.py:1338`, insert call to `model.create_sidl_combination(partial_safety_factor=1.0)` immediately following barrier, railing, and median load creation.

---

### DEF-03: Section Property Desynchronization Between Snapped Plates and Grillage
1. **Observation & Call Chain:** Grillage solver uses preliminary un-snapped girder properties ($I_z = 0.0073409\text{ m}^4$) instead of final snapped plate dimensions ($I_z = 0.0097174\text{ m}^4$).
   - Sizing Return: `src/osdagbridge/core/bridge_types/plate_girder/initial_sizing.py:519–520`.
   - Model Assignment: `plategirderbridge.py:1260–1277` constructs `bcfg.girder_props` before final plate optimization.
2. **Baseline Behavior:** Deflection and stiffness calculations off by up to $24.5\%$ (sealed log `tc_reg_b01_section_property_sync.log`).
3. **Proposed Fix Specification:** Re-run section property derivation after final plate snapping and update solver beam elements with synchronized $A, I_z, I_y, J$.

---

### DEF-05: Wind Parameter Propagation Loss
1. **Observation & Call Chain:** Basic wind speed $V_b$, reference height $H$, and terrain type omitted or defaulted.
   - UI Fields: `ui_fields_project_location.py`.
   - Bridge Manager: `plategirderbridge.py:1380–1416` defaults $V_b = 33.0\text{ m/s}, H = 10.0\text{ m}$, terrain = Category 1.
2. **Baseline Behavior:** Sealed baseline evaluated $P_z = 463.7\text{ N/m}^2$ instead of $1039.6\text{ N/m}^2$ (sealed log `tc_reg_d01_wind_speed_propagation.log`).
3. **Proposed Fix Specification:** Propagate `KEY_WL_BASIC_WIND_SPEED`, `KEY_WL_AVG_EXPOSED_HEIGHT`, and `KEY_WL_TERRAIN_TYPE` through `plategirderbridge.py` to `analyser.py`.

---

### DEF-07: Sectional Fatigue Stress Range End-Sign Doubling & Zero-Clamping
1. **Observation & Call Chain:** Stress range extraction in `designer.py:2976–2996` doubles sagging moments and clamps negative values.
   - Mechanism 1 (End-sign doubling): $M_0 - (-M_0) = 2M_0 = 125.46\text{ MPa}$.
   - Mechanism 2 (Zero-clamping): $\max(M,0) - \min(M,0)$ converts static sagging into range ($62.73\text{ MPa}$).
2. **Baseline Behavior:** Static invariant produces fictitious stress range $62.73\text{ MPa}$ instead of $0.000\text{ MPa}$.
3. **Proposed Fix Specification:** Remove zero-clamp. Evaluate physical section moment range $\Delta M(x) = \max_{lc} M(lc, x) - \min_{lc} M(lc, x)$. Harmonize element end-j with next element end-i.

---

### DEF-08: Executive Summary Emits Hardcoded Static "Pass" Narrative
1. **Observation & Call Chain:** `executive_summary.py:233–236` emits hardcoded LaTeX "Pass" string regardless of component DCRs.
2. **Baseline Behavior:** Fails in 64 of 74 test scenarios (sealed log `tc_reg_rpt_exec_summary_status.log`).
3. **Proposed Fix Specification:** Dynamically evaluate $\max(\text{DCR}) \le 1.000$ across girders, bracing, diaphragms, and deck slab. Emit "Fail" if any component exceeds $1.000$, and "Not Evaluated" if dictionaries are missing.

---

### DEF-10: Reference Database Read-Only Packaging & Access Paths
1. **Observation & Call Chain:** `weather.sqlite` materialized into package directory or CWD on open; schema bootstrap executes writes; URI formatting fragile.
   - Access Paths:
     1. `ui_fields_project_location.py:24`
     2. `src/osdagbridge/core/reports/report_generator.py:666`
     3. `src/osdagbridge/desktop/ui/dialogs/project_location.py:932`
     4. `src/osdagbridge/core/data/project_location/zone_lookup.py:189`
     5. `src/osdagbridge/core/data/project_location/database.py:356`
2. **Baseline Behavior:** Connect creates `-journal` sidecars or mutates package directory (sealed log `tc_reg_fs_clean_working_tree.log`).
3. **Proposed Fix Specification:**
   - Use `Path(DB_PATH).resolve().as_uri() + "?mode=ro"` with `sqlite3.connect(..., uri=True)`.
   - Add explicit `Path.is_file()` pre-check so caller receives clean `FileNotFoundError`.
   - Run `PRAGMA quick_check` at open.
   - Guard against write operations (`run_schema` / `_bootstrap_stations_if_missing`) in read-only mode.
   - Define acceptance hash as logical SHA-256 of sorted `iterdump()`.

---

### DEF-11: Girder Count Geometry Misalignment in `BridgeConfig`
1. **Observation & Call Chain:** `designer.py:401, 413` counts grillage longitudinal lines (including edge lines), reporting $n_{\text{girders}} = 6$ for a 4-girder bridge.
2. **Baseline Behavior:** Sealed log `tc_reg_geo_girder_count_alignment.log` records 6 instead of 4.
3. **Proposed Fix Specification:** Bind `bcfg.geometry.n_girders` directly to `bridge._girder_count()`.

---

### DEF-12: Bearing Stiffener Web Buckling Capacity Formula Anomaly
1. **Observation & Call Chain:** `designer.py:1664–1672` evaluates web buckling capacity $F_{cdw}$ using stiffener plate inertia $I_{ys}$ instead of unstiffened web radius of gyration $r_y = t_w / \sqrt{12}$. Raw Euler stress $f_{cc} = 35,577\text{ MPa}$ calculated without capping at $f_y$ or applying column curve c reduction.
2. **Baseline Behavior:** Overpredicts capacity by **$3,384\times$** on sealed geometry 1 ($214,533\text{ kN}$ vs true $63.40\text{ kN}$). Hand calculation fixture true capacity is $118.79\text{ kN}$ ($\phi = 7.6130$).
3. **Consequence Analysis:** Row "Brg.Stiff: Web Buckling" runs in full-verification mode and emits a false "PASS = stiffener not needed", leading users to omit bearing stiffeners.
4. **Proposed Fix Specification:** Implement IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 curve c ($\alpha = 0.49$) using $r_y = t_w / \sqrt{12}$, $KL = 0.7d$, $A_{wb} = (b_1 + n_1)t_w$, and design compressive stress $f_{cd} = \chi f_y / \gamma_{m0}$.

---

### DEF-13: Hardcoded Structural Steel and Deck Concrete Density Propagation
1. **Observation & Call Chain:** `analyser.py:10, 416` and `plategirderbridge.py:1332–1333` hardcode $\rho_s = 78.5\text{ kN/m}^3$ and $\rho_c = 25.0\text{ kN/m}^3$, ignoring user material inputs.
2. **Baseline Behavior:** User-injected $\rho_s = 70.0\text{ kN/m}^3$ ignored; dead load evaluates to $169.819\text{ kN}$ instead of $151.431\text{ kN}$ (sealed log `tc_reg_mat_density_consistency.log`).
3. **Proposed Fix Specification:** Update `create_self_weight_load` and `create_deck_load` method signatures to accept `density_kN_m3: float | None = None`. Propagate inputs from `input_dict`.

---

### DEF-18: Non-Conservation of Static Load Equilibrium & End-Bay Drop
1. **Four Ground-Truth Sub-Defects Identified (Claude Re-Audit §3):**
   - **Sub-Defect 1 (Line load magnitude):** `osp_grillage.py:1717` assigns $W = (w_1 + w_2)/2$ instead of $W = ((w_1 + w_2)/2) \cdot L$. Omits segment length multiplier, assigning average intensity instead of total force.
   - **Sub-Defect 2 (First end-bay drop - Finding R2-06):** In bay 1 ($p_1=1.5, p_2=0$), `get_point_given_distance` subtracts $x_{\text{bar}}$ from $p_2$, placing equivalent point at $x = -0.75\text{ m}$ (outside mesh). `_assign_load_to_four_node` finds `grid_nodes is None` and **silently returns `[]`** (`osp_grillage.py:1577-1579`). Line 1676 `continue` never fires.
   - **Sub-Defect 3 (Interpolation axis swap):** `osp_grillage.py:1713–1714` passes $[p_1[0], 0, p_1[1]]$ (y elevation) instead of $[p_1[0], 0, p_1[2]]$ (z coordinate) to `interpolate_udl_magnitude`.
   - **Sub-Defect 4 (Patch over-integration - Finding R2-08):** 1) 4 corner cells intersected by two adjacent edges evaluated twice ($210\text{ m}^2$ vs $204\text{ m}^2$ on $7\times 17$ mesh); 2) `p_list.pop(count)` mutates list while enumerating; 3) Mean vertex pressure $\times$ area is approximate for non-uniform loading (order $|\nabla p| h^2$).
2. **Baseline Behavior:** Barrier line load assigned only $196.200\text{ kN}$ instead of $313.920\text{ kN}$ ($-37.5\%$ shortfall); centroid shifted to $12.750\text{ m}$ (sealed log `tc_reg_eq_load_conservation.log`).
3. **Proposed Fix Specification:**
   - Multiply segment line load by length: `W = ((w1 + w2) / 2) * L`.
   - Measure $x_{\text{bar}}$ from $p_1$ toward $p_2$, or use true segment centroid. Convert silent `return []` into a hard error.
   - Fix interpolation z-coordinate: $[p_1[0], 0, p_1[2]]$.
   - Deduplicate patch cells via grid number set; fix list mutation; enforce $\le 10^{-9}$ tolerance for uniform patches and document $h$-dependent analytical bound for non-uniform patches.

---

### DEF-19: Live-Load Factor Composition Omission
1. **Pipeline Trace & Latent Defects (Claude Re-Audit §4; Finding R2-05):**
   - **DEF-19a:** In `irc6_2017.py:534, 543`, `if KEY_VEHICLE[1]:` tests `'Class70R(T)'`, which is always truthy. Always returns hardcoded $0.10$ impact for spans 9–45m.
   - **DEF-19b:** In `analyser.py:1827`, `LANE_REDUCTION_FACTORS = [1.0, 0.8, 0.4]` indexed per vehicle within `coord_list`, not per loaded lanes.
   - **DEF-19c:** Analysis applies $0.10$ impact; report chapter 3 prints Class A steel formula $9/(13.5+L) = 0.24$.
   - **Factor Dropping:** `lc.add_load(vehicle, load_factor=lane_factor)` drops lane factor (DEF-01). Case added with `load_factor=dla`. Governing live-load selection (`analyser.py:2025–2027`) and combinations (`analyser.py:2348`) drop factors.
2. **Proposed Fix Specification:** Implement exact three-stage equality oracles:
   - Stage 1: Vehicle case ($DLA$ applied once).
   - Stage 2: Governing selection ($DLA \times \text{lane factor}$ preserved).
   - Stage 3: ULS combination ($\gamma_Q \times DLA \times \text{lane factor}$ compounded).
   - Raise **DEC-019** for owner ratification of the applicable Cl. 208 impact formula for composite superstructures.

---

### DEF-20: Wearing Course Transverse Extent (Full Deck Width vs Carriageway Clear Width)
1. **Observation & Call Chain (Finding R2-02):**
   - In `plategirderbridge.py:1334`, `create_wearing_course_load` is called with default `edge_clearance=0.0`.
   - In `load_placement.py:133–139`, `overlay_load` spans from $0.0$ to `bridge.width` ($8.500\text{ m}$).
   - Sealed EQ log line 17 recorded: "Expected 216.000 … Applied 244.800".
2. **Standards Analysis:** IRC:5 Clause 104 and IRC:6 Clause 202 specify wearing course across the carriageway width ($7.500\text{ m}$ between kerbs/barriers), not extending under the crash barriers.
3. **Proposed Fix Specification:**
   - Establish dual-oracle acceptance: production baseline behavior ($244.800\text{ kN}$) for regression verification, and intended carriageway behavior ($216.000\text{ kN}$, with `edge_clearance = 0.500\text{ m}`) governed by DEC-020 sign-off.

---

### DEF-LATENT-ZP: Transverse Coordinate Indexing in Line Load Intensity Interpolation
1. **Observation & Call Chain (Finding R2-03, Condition 1):**
   - In `src/ospgrillage/load.py:710`, within `interpolate_udl_magnitude`, the code sets `zp = point_coordinate[0]` instead of `point_coordinate[2]`.
   - When interpolating load intensity for vertical/transverse line loads where $x_1 = x_2$ and $z_1 \ne z_2$, the interpolation logic incorrectly evaluates coordinates along the longitudinal axis ($x$) instead of the transverse axis ($z$).
2. **Baseline Behavior & Latency:**
   - In standard longitudinal line loads ($x_1 \ne x_2, z_1 = z_2$), the interpolation branch `v[0] != 0` evaluates exclusively based on `point_coordinate[0]`, leaving line 710 unexercised.
   - For skew or transverse varying loads where vertical lines are tested, this causes incorrect intensity evaluation.
3. **Scoping & Governance Decision:**
   - Identified during Phase 3 Batch 2 reconnaissance as a latent defect in `load.py:710`.
   - Excluded from Phase 3 Batch 2 implementation commits (`34cd4bf` and `9e0b588`) to preserve strict atomic scope boundaries (as confirmed in independent audit `P3-IA-002`, finding R2-03).
   - Formally registered and tracked as an unresolved, separately scoped defect for future remediation authorization.

---

## 4. Phase 3 Engineering Remediation Defect Disposition & Closure Ledger

This section establishes the authoritative, cumulative defect disposition ledger for Phase 3 engineering remediation. While Section 1 preserves the permanent historical baseline condition (`BASELINE_FAIL`), this ledger tracks progressive remediation, independent audit verification, Git commit lineage, and formal closure decisions across all remediation batches approved by the Human Project Director.

### 4.1 Master Defect Disposition Table

| Defect ID | Defect Title | Baseline Status (Historical) | Remediation Batch | Commit SHA | Remediation Branch | Closure Record | Controlling Independent Audits | Current Disposition Status |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **DEF-12** | Bearing Stiffener Web Buckling Formula Anomaly | `BASELINE_FAIL` | Batch 1 | `418fd75` | `fix/phase-3-engineering-remediation` | `P3-CR-001` | `CLAUDE_BATCH_1_INDEPENDENT_AUDIT.md` (ACCEPTED) | **FORMALLY CLOSED (Batch 1)** |
| **DEF-08** | Executive Summary Emits Hardcoded Static "Pass" | `BASELINE_FAIL` | Batch 1 | `12493c9` | `fix/phase-3-engineering-remediation` | `P3-CR-001` | `CLAUDE_BATCH_1_INDEPENDENT_AUDIT.md` (ACCEPTED) | **FORMALLY CLOSED (Batch 1)** |
| **DEF-11** | Girder Count Geometry Misalignment in Config | `BASELINE_FAIL` | Batch 1 | `eaba076` | `fix/phase-3-engineering-remediation` | `P3-CR-001` | `CLAUDE_BATCH_1_INDEPENDENT_AUDIT.md` (ACCEPTED) | **FORMALLY CLOSED (Batch 1)** |
| **DEF-18** | Grillage Statics Non-Conservation (Line & Patch) | `BASELINE_FAIL` | Batch 2 | `34cd4bf`<br>`9e0b588` | `fix/phase-3-engineering-remediation` | `P3-CR-002` | `PHASE_3_BATCH_2_INDEPENDENT_AUDIT.md` (ACCEPTED WITH COND.) | **FORMALLY CLOSED (Batch 2)** |
| **DEF-01** | Component Load-Factor Scaling Omission | `BASELINE_FAIL` | Batch 3 | `f555075` | `fix/phase-3-engineering-remediation` | `P3-CR-003` | `CLAUDE_DEF_01_INDEPENDENT_CHALLENGE_AUDIT.md` (ACCEPTED)<br>`CLAUDE_BATCH_3_POST_COMMIT_AUDIT.md` (ACCEPTED) | **FORMALLY CLOSED (Batch 3)** |
| **DEF-02** | Crash Barrier SIDL Omission in Combinations | `BASELINE_FAIL` | — (Batch 4 Candidate) | — | — | — | — | **OPEN** |
| **DEF-03** | Section Property Desync (Snapped Plates vs Solver) | `BASELINE_FAIL` | — | — | — | — | — | **OPEN** |
| **DEF-05** | Wind Parameter Propagation Loss (Vb, H, Terrain) | `BASELINE_FAIL` | — | — | — | — | — | **OPEN** |
| **DEF-06** | Temperature Load Omission / Pressure Fallback | `BLOCKED` (DEC-015) | — | — | — | — | — | **BLOCKED** |
| **DEF-07** | Fatigue Stress Range Sign Flip & Zero Clamping | `BASELINE_FAIL` | — | — | — | — | — | **OPEN** |
| **DEF-09** | Offscreen OpenCASCADE Viewport Export | `PASS` (Harness) | Baseline | — | — | — | — | **PASS (Harness)** |
| **DEF-10** | Database Runtime Materialization & Tree Mutation | `BASELINE_FAIL` | — | — | — | — | — | **OPEN** |
| **DEF-13** | Hardcoded Steel/Deck Density Propagation | `BASELINE_FAIL` | — | — | — | — | — | **OPEN** |
| **DEF-14** | Transverse Slab Assigned Steel Properties | `BLOCKED` (DEC-013) | — | — | — | — | — | **BLOCKED** |
| **DEF-17** | Fatigue Vehicle Moving Load Pipeline Omission | `BLOCKED` (DEC-018) | — | — | — | — | — | **BLOCKED** |
| **DEF-19a** | Truthy String Check Hardcoding 0.10 Impact | `BASELINE_FAIL` (Latent) | — | — | — | — | — | **OPEN** |
| **DEF-19b** | Lane Reduction Factors Indexed Per-Vehicle | `BASELINE_FAIL` (Latent) | — | — | — | — | — | **OPEN** |
| **DEF-19c** | Analysis vs Report Chapter 3 Impact Discrepancy | `BASELINE_FAIL` (Latent) | — | — | — | — | — | **OPEN** |
| **DEF-20** | Wearing Course Width (Full Deck vs Carriageway) | `BASELINE_FAIL` | — | — | — | — | — | **OPEN** |
| **DEF-LATENT-ZP** | Transverse Coordinate Indexing in `load.py:710` | `UNRESOLVED` (Latent) | — | — | — | — | — | **UNRESOLVED (Latent)** |

### 4.2 Batch Closure Decisions Summary

| Batch ID | Scope / Target Defects | Closure Decision Record | Director Decision | Closure Approval Date | Branch & HEAD | Cumulative Commits |
|:---:|:---|:---:|:---:|:---:|:---|:---:|
| **Batch 1** | DEF-12, DEF-08, DEF-11 | `P3-CR-001` | APPROVED | 2026-11-19 | `fix/phase-3-engineering-remediation`<br>HEAD: `eaba076` | `418fd75`, `12493c9`, `eaba076` |
| **Batch 2** | DEF-18 (LINE & PATCH) | `P3-CR-002` | APPROVED | 2026-11-19 | `fix/phase-3-engineering-remediation`<br>HEAD: `9e0b588` | `34cd4bf`, `9e0b588` |
| **Batch 3** | DEF-01 | `P3-CR-003` | APPROVED | 2026-11-19 | `fix/phase-3-engineering-remediation`<br>HEAD: `f555075` | `f555075` |

### 4.3 Remediation Governance Invariants
1. **Preservation of Baseline Records:** All baseline failures (`BASELINE_FAIL`) documented in Section 1 remain immutable historical records reflecting the original unpatched system state at baseline anchor commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.
2. **Phase 3 Completion Status:** Phase 3 remediation is **NOT complete**. As of Batch 3 closure, 5 defects across Batches 1, 2, and 3 are formally closed (`DEF-12`, `DEF-08`, `DEF-11`, `DEF-18`, `DEF-01`). The remaining defects (`DEF-02`, `DEF-03`, `DEF-05`, `DEF-06`, `DEF-07`, `DEF-10`, `DEF-13`, `DEF-14`, `DEF-17`, `DEF-19a/b/c`, `DEF-20`, `DEF-LATENT-ZP`) remain open, blocked, or latent, awaiting subsequent authorized batch remediation.
3. **Local Remediation Isolation:** All remediation commits (`418fd75` through `f555075`) reside exclusively on the local branch `fix/phase-3-engineering-remediation`. Zero remote pushes, zero pull requests, and zero merges to `dev` or `main` have occurred. Upstream baseline `origin/dev` remains untouched at `d74f56d`.

