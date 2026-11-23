# PHASE 3 — Defect Traceability Matrix and Ground-Truth Source Analysis (Revision 2.0)

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Revision:** Revision 2.0 (Post-Audit Re-Baseline)  
**Controlling Audit:** `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md` (by independent auditor Claude)  
**Historical Revision Archive:** `reports/phase_3/v1_original/PHASE_3_DEFECT_TRACEABILITY_MATRIX.md`  
**Date:** 2026-11-18  

---

## 1. Master Defect Register Summary (16 Cataloged Defects)

Following the independent Phase 3 planning audit by Claude, the OsdagBridge Defect Register has been comprehensively updated. The register now formally tracks **16 distinct defects and architectural gaps**, including the newly cataloged latent live-load factor composition defect (`DEF-19`):

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
| **DEF-10** | Reference Database Runtime Materialization & Package Tree Mutation | `database.py`<br>`ui_fields_project_location.py` | 12–30<br>16–29 | Medium | `BASELINE_FAIL` | POSIX/Windows Packaging |
| **DEF-11** | Girder Count Geometry Misalignment (Edge Lines Counted in Config) | `designer.py`<br>`plategirderbridge.py` | 401, 413<br>1112–1115 | Medium | `BASELINE_FAIL` | Grillage Mesh Topology |
| **DEF-12** | Bearing Stiffener Web Buckling Capacity Formula Anomaly | `designer.py` | 1664–1672 | Critical | `BASELINE_FAIL` | IS 800:2007 Cl. 8.7.3.1 / IRC:24 |
| **DEF-13** | Hardcoded Structural Steel and Deck Concrete Density Propagation | `analyser.py`<br>`plategirderbridge.py` | 10, 416<br>1332–1333 | Medium | `BASELINE_FAIL` | IRC:6-2017 Cl. 202.1 |
| **DEF-14** | Transverse Concrete Deck Slab Assigned Steel Girder Properties | `plategirderbridge.py` | 1279–1291 | High | `BLOCKED` (DEC-013) | Grillage Structural Mechanics |
| **DEF-17** | Fatigue Vehicle Moving Load Analysis Pipeline Omission | `analyser.py`<br>`designer.py` | 1612–1660<br>2972–2985 | Critical | `BLOCKED` (DEC-018) | IRC:6-2017 Cl. 204.6 |
| **DEF-18** | Non-Conservation of Static Load Equilibrium & End-Bay Drop | `src/ospgrillage/osp_grillage.py` | 1674–1729<br>1795–1850 | Critical | `BASELINE_FAIL` | Static Equilibrium ($\Sigma F_y = 0$) |
| **DEF-19** | Live-Load Factor Composition Omission (Lane Factors & DLA Dropped) | `analyser.py` | 1836, 1841, 2025 | High | `BASELINE_FAIL` (Latent) | IRC:6-2017 Cl. 204.4 / Cl. 208 |

---

## 2. Authoritative Unified Test Fixture Specification

To eliminate the oracle discrepancies identified in Claude's audit (§3 DEF-18), all derived dead load, combination, section property, and deflection acceptance criteria are anchored to a **single authoritative structural test fixture**:

### Fixture Geometry & Material Definitions
- **Span Length:** $L = 24.000\text{ m}$ (simply supported, skew angle $0^\circ$).
- **Overall Deck Width:** $W_{\text{deck}} = 8.500\text{ m}$.
- **Carriageway Width:** $W_{\text{cw}} = 7.500\text{ m}$ (centered between crash barriers).
- **Deck Slab Thickness:** $t_{\text{deck}} = 0.250\text{ m}$ ($250\text{ mm}$).
- **Wearing Course Thickness:** $t_{\text{wc}} = 0.050\text{ m}$ ($50\text{ mm}$).
- **Material Densities:**
  - Structural Steel: $\rho_s = 78.50\text{ kN/m}^3$ (or user-injected custom $\rho_{s,\text{user}} = 70.00\text{ kN/m}^3$).
  - Concrete Deck Slab: $\rho_c = 24.50\text{ kN/m}^3$.
  - Asphalt Wearing Course: $\rho_{\text{wc}} = 24.00\text{ kN/m}^3$.
- **Girder Layout:** 4 longitudinal I-girders at center-to-center spacing $c = 2.133\text{ m}$; overhang $s_{\text{overhang}} = 1.050\text{ m}$.
- **Snapped Plate Dimensions:**
  - Web: $d_w = 1300\text{ mm}, t_w = 10\text{ mm}$.
  - Top Flange: $b_{ft} = 400\text{ mm}, t_{ft} = 16\text{ mm}$.
  - Bottom Flange: $b_{fb} = 500\text{ mm}, t_{fb} = 26\text{ mm}$.
  - Total Section Depth: $D = 1342\text{ mm}$.
- **Derived Snapped Section Properties (Bare Steel):**
  $$A = b_{ft} t_{ft} + b_{fb} t_{fb} + d_w t_w = 6400 + 13000 + 13000 = 32,400\text{ mm}^2 = \mathbf{0.032400\text{ m}^2}$$
  $$\bar{y}_{\text{bot}} = \frac{13000(13) + 13000(676) + 6400(1334)}{32400} = \mathbf{0.539957\text{ m}} \quad (539.957\text{ mm})$$
  $$I_z = I_{z,\text{web}} + I_{z,\text{bot}} + I_{z,\text{top}} = \mathbf{0.0097174\text{ m}^4} \quad (9.7174 \times 10^9\text{ mm}^4)$$
  $$I_y = I_{y,\text{web}} + I_{y,\text{bot}} + I_{y,\text{top}} = \mathbf{0.0003563\text{ m}^4} \quad (3.5628 \times 10^8\text{ mm}^4)$$
- **Applied Physical Dead Loads (Closed-Form):**
  1. *Girder Self-Weight ($SW$):* $P_{SW} = 4 \times 24.0 \times 0.032400 \times 78.5 = \mathbf{244.166\text{ kN}}$ (or $217.728\text{ kN}$ at $\rho=70.0$).
     *(Historical baseline note: preliminary sizing used $A = 0.022534\text{ m}^2 \implies P_{SW} = 169.819\text{ kN}$).*
  2. *Concrete Deck Slab ($DD$):* $P_{DD} = 24.0 \times 8.50 \times 0.25 \times 24.5 = \mathbf{1249.500\text{ kN}}$ (intensity $w_{DD} = 6.125\text{ kPa}$).
  3. *Wearing Course ($DW$):* $P_{DW} = 24.0 \times 7.50 \times 0.05 \times 24.0 = \mathbf{216.000\text{ kN}}$ (intensity $w_{DW} = 1.200\text{ kPa}$).
     *(Historical baseline note: baseline applied over full $8.5\text{ m}$ deck width $\implies 244.800\text{ kN}$).*
  4. *Crash Barrier ($CB$):* $2 \times 24.0 \times 6.54 = \mathbf{313.920\text{ kN}}$ ($156.960\text{ kN}$ per side at $z = 0.250\text{ m}$ and $z = 8.250\text{ m}$).
  5. *Total Applied Dead Load (Physical Reconciled):*
     $$\sum P_{\text{applied}} = 244.166 + 1249.500 + 216.000 + 313.920 = \mathbf{2023.586\text{ kN}}$$
  6. *Theoretical Factored ULS Resultant (`BASIC_1`):*
     $$P_{\text{ULS, B1}} = 1.35 \times (P_{SW} + P_{DD} + P_{CB}) + 1.75 \times P_{DW} = 1.35(244.166 + 1249.500 + 313.920) + 1.75(216.000) = \mathbf{2788.751\text{ kN}}$$
     *(Historical baseline sealed oracle used preliminary SW: $1.35(165.28 + 1249.50 + 313.92) + 1.75(216.00) = 2711.74\text{ kN}$).*

---

## 3. Exhaustive Technical Profiles for All 16 Defects

---

### DEF-01: Load Factor Scaling Omission in `ospgrillage` Load Combinations

1. **Original Observation:**  
   In ULS load combinations (`BASIC_1`), force scaling factors passed to `LoadCase.add_load(load, load_factor=gamma)` had zero effect on OpenSees command vectors. The reaction force ratio was $1.00000$ instead of $1.35000$.
2. **Current Source Location & Call Path:**  
   - Loop Location: `src/ospgrillage/osp_grillage.py:1934–1960` (in `_distribute_load_types_to_model`, not in `_assign_load_to_four_node`).
   - Storage Location: `src/ospgrillage/load.py:1166–1168` (`add_load` sets `load_dict.setdefault("factor", load_factor)`).
   - Downstream Copy Sites: `analyser.py:2344–2348` (`_copy_loads` in `create_uls_combinations`), `analyser.py:2539–2543` (in `create_sls_combinations`).
   - Mechanism: `osp_grillage.py:1934` loops over `load_groups` and extracts `load_dict["load"]`, but ignores `load_dict["factor"]`.
3. **Baseline Existence:**  
   **CONFIRMED (IV+IR+SE).** Baseline test `TC-REG-A01-FACTOR-SCALING` fails with force ratio $1.00000$ vs $1.35000$.
4. **Reproduction Procedure:**  
   In a standalone script, create a grillage model using vendored `ospgrillage`. Create a `LoadCase`, add a $100\text{ kN}$ point load with `load_factor=1.35`. Call `bridge.solve()`. Sum support reactions: $\Sigma R_y = 100.000\text{ kN}$ (ratio $1.00000$).
5. **Expected Engineering Behavior:**  
   OpenSees nodal load commands must reflect the compounded factor:
   $$\text{Effective Factor} = \text{Entry Factor} \times \text{Source Case Factor} \times \text{Combination Factor}$$
6. **Actual Behavior:**  
   All entry-level factors are ignored; combination cases registered with factor 1.0 execute un-factored.
7. **Relevant Standards:**  
   IRC:6-2017 Table B.2 ($\gamma_G = 1.35$, $\gamma_Q = 1.50$).
8. **Dependencies & Interacting Defects:**  
   Interacts with `DEF-19` (lane factors & DLA), `DEF-02` (combination sums), `DEF-18`.
9. **Potential Regression Risks:**  
   Must preserve unity when sub-cases already carry case-level factors to prevent double-factoring.
10. **Proposed Fix Specification:**  
    In `src/ospgrillage/osp_grillage.py:1934`, retrieve `fac = load_dict.get("factor", 1.0)` and scale point, line, and patch load intensities prior to element distribution. In `analyser.py:2348`, ensure `_copy_loads` compounds existing entry factors with combination factors (`factor = existing_factor * float(new_factor)`).

---

### DEF-02: Crash Barrier Superimposed Dead Load Omission in Combinations

1. **Original Observation:**  
   The crash barrier line load ($313.92\text{ kN}$) was omitted from the `BASIC_1` combination.
2. **Current Source Location & Call Path:**  
   - Omission Site: `plategirderbridge.py:1336–1339` (`model.create_crash_barrier_load()` called, but `create_sidl_combination()` is never called).
   - Combination Assembly: `analyser.py:1532–1558` (`create_dead_load_combination` queries `self.sidl_combination`, which is `None`).
   - ULS Map: `analyser.py:2319` (`dead_load` maps to `dead_load_combination`).
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Sealed log `tc_reg_a02_uls_combination_sum.log` records an observed barrier contribution of **−708.74 kN** (a compound artifact of DEF-01 unfactored combinations and DEF-18 distorted reactions).
4. **Reproduction Procedure:**  
   Execute `test_tc_reg_a02()`. Inspect `dead_load_combination.load_groups`. Confirm that crash barrier, railing, and median load objects are completely absent.
5. **Expected Engineering Behavior:**  
   `dead_load_combination` must contain all permanent structural and non-structural dead loads. Crash barrier loads must be present with un-factored resultant $313.92\text{ kN}$ at $\gamma = 1.0$, and factored contribution $1.35 \times 313.92 = 423.79\text{ kN}$ in `BASIC_1`.
6. **Actual Behavior:**  
   Barrier load is generated into an isolated sub-case that is discarded during combination assembly.
7. **Relevant Standards:**  
   IRC:6-2017 Clause 202 & Table B.2.
8. **Dependencies & Interacting Defects:**  
   Isolated presence check depends only on `plategirderbridge.py`; factored combination check requires `DEF-01` and `DEF-18`.
9. **Potential Regression Risks:**  
   Ensure railing and median loads are also absorbed into SIDL without duplicate counting.
10. **Proposed Fix Specification:**  
    In `plategirderbridge.py:1338`, insert `model.create_sidl_combination(partial_safety_factor=1.0)` immediately prior to `create_dead_load_combination()`.

---

### DEF-03: Section Property Desynchronization Between Snapped Plates and Grillage

1. **Original Observation:**  
   Grillage beam elements retained preliminary sizing properties ($A = 0.022534\text{ m}^2, I_z = 0.0073409\text{ m}^4$) rather than properties derived from snapped plates ($A = 0.032400\text{ m}^2, I_z = 0.0097174\text{ m}^4$).
2. **Current Source Location & Call Path:**  
   - Property Read: `plategirderbridge.py:1260–1277` (`_girder_section` queries `self.input_dict` via `_girder_value`).
   - Desynchronization Site: Snapped plate dimensions are stored, but derived sectional properties (`KEY_MP_GIRDER_SECTIONAL_IZ`, etc.) are not recomputed before grillage staging. *(Exact snapping site in `initial_sizing.py` unverified at baseline; line 519–520 is a return dict, not a snapping site).*
3. **Baseline Existence:**  
   **CONFIRMED (SE).** Sealed log `tc_reg_b01_section_property_sync.log` confirms solver elements retain preliminary sizing ($I_z = 0.0073409\text{ m}^4$).
4. **Reproduction Procedure:**  
   Run `test_tc_reg_b01()`. Extract properties from OpenSees element tags. Compare with parallel-axis derivation from snapped plate dimensions.
5. **Expected Engineering Behavior:**  
   Bare-steel longitudinal beam elements must carry section properties derived strictly from snapped plate dimensions ($d_w=1300, t_w=10$, top $400\times 16$, bot $500\times 26$):
   $$A = 0.032400\text{ m}^2, \quad \bar{y} = 0.539957\text{ m}, \quad I_z = 0.0097174\text{ m}^4, \quad I_y = 0.0003563\text{ m}^4$$
   Under a midspan point load $P = 100\text{ kN}$ on a simply supported bare beam ($L=24\text{ m}, E=200\text{ GPa}$), Euler-Bernoulli deflection is:
   $$\delta = \frac{P L^3}{48 E I_z} = \frac{100 \times 10^3 \times 24^3}{48 \times (200 \times 10^9) \times 0.0097174} = \mathbf{14.819\text{ mm}}$$
6. **Actual Behavior:**  
   Solver elements carry preliminary properties, producing ~8.3% deflection error.
7. **Relevant Standards:**  
   IS 800:2007 Section 8; Euler-Bernoulli beam theory (`elasticBeamColumn`).
8. **Dependencies & Interacting Defects:**  
   Scope strictly covers bare steel. Interaction with composite action is governed by DEC-013.
9. **Potential Regression Risks:**  
   Timoshenko beam elements would introduce ~4% shear deflection; acceptance oracle must pin `elasticBeamColumn`.
10. **Proposed Fix Specification:**  
    Implement `derive_snapped_section_properties()` in `plategirderbridge.py` to overwrite `KEY_MP_GIRDER_*` sectional keys with exact parallel-axis derivations prior to `_stage_grillage_setup()`.

---

### DEF-05: Wind Parameter Propagation Loss (Basic Wind Speed, Heights & Terrain)

1. **Original Observation:**  
   User-configured wind parameters ($V_b = 47\text{ m/s}, H = 15\text{ m}$) were ignored; analysis defaulted to $33\text{ m/s}$ and $10\text{ m}$.
2. **Current Source Location & Call Path:**  
   - Lookup Site: `plategirderbridge.py:1381–1393` queries bare unprefixed keys (`ai.get("basic_wind_speed")`, `ai.get("terrain_type")`).
   - Constant Definitions: `osdagbridge/core/utils/common.py` defines `KEY_WL_BASIC_WIND_SPEED`, `KEY_WL_AVG_EXPOSED_HEIGHT`, `KEY_WL_TERRAIN_TYPE`, `KEY_CB_HEIGHT`, `KEY_RL_HEIGHT`.
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Sealed log `tc_reg_d01_wind_speed_propagation.log` confirms captured arguments evaluate to $33.0\text{ m/s}$ and $10.0\text{ m}$.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_d01()`. Inject namespaced wind parameters into `cfg`. Spy on arguments passed to `bgm.create_wind_load()`.
5. **Expected Engineering Behavior:**  
   Input keys must resolve from namespaced constants. Per IRC:6-2017 Table 12, for plain terrain at $H = 15\text{ m}$, basic pressure is $512.5\text{ N/m}^2$ at $33\text{ m/s}$. Scaled for $V_b = 47\text{ m/s}$:
   $$P_z = 512.5 \times \left(\frac{47}{33}\right)^2 = \mathbf{1039.6\text{ N/m}^2}$$
6. **Actual Behavior:**  
   Unprefixed key lookups fail; wind pressure defaults to $463.7\text{ N/m}^2$ ($33\text{ m/s}, 10\text{ m}$).
7. **Relevant Standards:**  
   IRC:6-2017 Clause 209 & Table 12.
8. **Dependencies & Interacting Defects:**  
   None (independent input binding).
9. **Potential Regression Risks:**  
   Must support both namespaced and flat legacy project file keys.
10. **Proposed Fix Specification:**  
    In `plategirderbridge.py:1381–1393`, resolve keys hierarchically:
    ```python
    basic_wind_speed = float(self.input_dict.get(KEY_WL_BASIC_WIND_SPEED) or ai.get("basic_wind_speed") or 33.0)
    height_for_pz = float(self.input_dict.get(KEY_WL_AVG_EXPOSED_HEIGHT) or ai.get("avg_exposed_height") or 10.0)
    terrain_raw = str(self.input_dict.get(KEY_WL_TERRAIN_TYPE) or ai.get("terrain_type") or "Plain Terrain")
    crash_barrier_height = float(self.input_dict.get(KEY_CB_HEIGHT) or ai.get("crash_barrier_height") or 0.0)
    railing_height = float(self.input_dict.get(KEY_RL_HEIGHT) or ai.get("railing_height") or 0.0)
    ```

---

### DEF-06: Temperature Load Modeling Omission / Vertical Pressure Fallback (DEC-015)

1. **Original Observation:**  
   Temperature analysis was omitted or applied as an unphysical downward vertical patch load in $\text{kN/m}^2$.
2. **Current Source Location & Call Path:**  
   - Dispatch: `plategirderbridge.py:1869–1877` (`add_temperature_load`).
   - Implementation: `analyser.py:905–938` (`create_temperature_load` converts $\text{kN/m}^2$ to downward patch load).
3. **Baseline Existence:**  
   **CONFIRMED (BLOCKED under DEC-015).** Kept formally blocked.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_d02()`. Confirms `BLOCKED (DEC-015)`.
5. **Expected Engineering Behavior:**  
   Per IRC:6-2017 Clause 215, on a simply-supported determinate span with pinned–roller supports, uniform temperature change produces free axial expansion ($\Delta L = L \alpha \Delta T = 24.0 \times 1.17\times 10^{-5} \times 30 = 8.42\text{ mm}$) and zero internal axial restraint force. Temperature gradients produce self-equilibrating sectional residual stresses and free curvature, evaluated in cross-sectional post-processing.
6. **Actual Behavior:**  
   Attempts to apply vertical gravity-like pressure load to grillage deck.
7. **Relevant Standards:**  
   IRC:6-2017 Clause 215.
8. **Dependencies & Interacting Defects:**  
   DEC-015 architectural decision.
9. **Potential Regression Risks:**  
   Unphysical restraint forces must not be applied to determinate boundary nodes.
10. **Proposed Fix Specification:**  
    Retain blocked status until DEC-015 is formally ratified by the engineering owner. Remove vertical patch load from `analyser.py`.

---

### DEF-07: Sectional Fatigue Stress Range End-Sign Doubling & Zero-Clamping

1. **Original Observation:**  
   Under static load, cyclic fatigue stress range was evaluated as $62.73\text{ MPa}$ or $125.46\text{ MPa}$ instead of $0.00\text{ MPa}$.
2. **Current Source Location & Call Path:**  
   - Bending Stress Range: `designer.py:2976–2985`.
   - Shear Stress Range: `designer.py:2987–2994`.
   - Two Compounding Mechanisms:
     1. *Local End-Sign Concatenation:* Flattens `Mz_i` and `Mz_j` across elements and subtracts opposite sign conventions ($\Delta M = M_0 - (-M_0) = 2M_0 \implies 125.46\text{ MPa}$).
     2. *Zero-Clamping:* `max(max, 0) - min(min, 0)` turns constant sagging moment into a range equal to $M_0$ ($62.73\text{ MPa}$).
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Sealed log `tc_reg_c01_sectional_stress_range.log` confirms both failure paths.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_c01()`. Apply constant sagging moment $M_0 = 1000\text{ kNm}$. Verify `stress_range_MPa`. Baseline yields non-zero false ranges.
5. **Expected Engineering Behavior:**  
   Fatigue stress range must be evaluated cross-section by cross-section across load cases. Under static load, $\Delta \sigma \equiv 0.000\text{ MPa}$. Under the 5-case cyclic verification history with $Z_e = 0.015942\text{ m}^3$ and governing range $\Delta M = 2700\text{ kNm}$:
   $$\Delta \sigma = \frac{2700 \times 10^3}{0.015942 \times 10^6} = \mathbf{169.363\text{ MPa}}$$
6. **Actual Behavior:**  
   Evaluates spatial sign differences across beam ends as temporal fatigue variations.
7. **Relevant Standards:**  
   IRC:22-2015 Clause 604.5 & 605.4; IS 800:2007 Clause 13.
8. **Dependencies & Interacting Defects:**  
   Extraction logic is independent; fully coupled to `DEF-17` (DEC-018) for moving load inputs. Labelled as a surrogate extraction until DEC-018 is implemented.
9. **Potential Regression Risks:**  
   Removing zero-clamping must properly handle stress ranges across sign-reversing hogging/sagging regions.
10. **Proposed Fix Specification:**  
    In `designer.py:2970–2996`:
    1. Remove `max(..., 0) - min(..., 0)` zero-clamping.
    2. Harmonize member local coordinate sign conventions so end-j of element $e$ matches end-i of element $e+1$.
    3. Evaluate true peak-to-peak range section-by-section: $\Delta M(x) = \max_{lc} M(lc, x) - \min_{lc} M(lc, x)$.
    4. Apply identical section-wise logic to shear range $\Delta V_y(x)$.

---

### DEF-08: Executive Summary Emits Hardcoded Static "Pass" Narrative

1. **Original Observation:**  
   Executive Summary unconditionally printed "Girder design pass" even when members failed checks with $\text{DCR} > 1.0$.
2. **Current Source Location & Call Path:**  
   - Narrative Lines: `src/osdagbridge/core/reports/executive_summary.py:233–236`.
   - Table Status: `executive_summary.py:77–110`.
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Baseline test `TC-REG-RPT-EXEC-SUMMARY-STATUS` fails in 64 of 74 failure scenarios.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_rpt_status()`. Inject failing girder, bracing, or deck results. Verify generated LaTeX text.
5. **Expected Engineering Behavior:**  
   Narratives and overall table status must dynamically derive from component results:
   - "Pass" if $\text{DCR} \le 1.000$; "Fail" if $\text{DCR} > 1.000$.
   - Explicit "Not Evaluated" when component results are omitted.
   - Table overall status must reflect girders, cross-bracing, end-diaphragms, and deck slab.
6. **Actual Behavior:**  
   Emits literal strings regardless of calculation outputs.
7. **Relevant Standards:**  
   Software Reliability, ISO/IEC 25010.
8. **Dependencies & Interacting Defects:**  
   Independent reporting module. Prioritized in Batch 1 to make upstream defects visible.
9. **Potential Regression Risks:**  
   Dictionary key lookups must match production DTO keys (`crossbracing_design_results`, etc.).
10. **Proposed Fix Specification:**  
    Replace hardcoded LaTeX strings in `executive_summary.py:233–236` with dynamic helper functions querying `output_dict`, supporting PASS, FAIL, and NOT_EVALUATED states.

---

### DEF-09: Offscreen OpenCASCADE Viewport Image Export Verification

1. **Original Observation:**  
   Headless CI environments without physical display drivers could produce blank CAD images.
2. **Current Source Location & Call Path:**  
   `testing/test_cases/baseline_regression/run_all_baseline_tests.py:2950–2995` (`test_tc_reg_cad_export`).
3. **Baseline Existence:**  
   **PASSING (Environment Check).** Pixel std $= 66.6 > 5.0$, 3 unique colors.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_cad_export()`. Verifies native OCC `Viewer3d.ExportToImage()` offscreen rasterization.
5. **Expected Engineering Behavior:**  
   Offscreen rendering produces non-uniform opaque images.
6. **Actual Behavior:**  
   PASS on baseline.
7. **Relevant Standards:**  
   OCC Visualization Guidelines.
8. **Dependencies & Interacting Defects:** None.
9. **Potential Regression Risks:** None.
10. **Proposed Fix Specification:** No code fix required.

---

### DEF-10: Reference Database Runtime Materialization & Package Tree Mutation

1. **Original Observation:**  
   `Database.connect()` executed `executescript(schema.sql)` on first run, writing into the package directory, and created untracked `weather.sqlite` in CWD when called with defaults.
2. **Current Source Location & Call Path:**  
   - Creation Site: `src/osdagbridge/core/data/project_location/database.py:12–30`.
   - Caller: `src/osdagbridge/core/bridge_types/plate_girder/ui_fields_project_location.py:16–29`.
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Baseline test `TC-REG-FS-CLEAN-WORKING-TREE` fails on package tree mutation and unanchored CWD database creation.
4. **Reproduction Procedure:**  
   In a clean checkout, delete `weather.sqlite`. Call `Database().connect()`. Verify that `weather.sqlite` is created in `os.getcwd()` and package data is written.
5. **Expected Engineering Behavior:**  
   Reference data is static and immutable. `weather.sqlite` must be pre-built deterministically from `schema.sql` during packaging. Runtime access must be strictly read-only (`?mode=ro`). Zero files must be created or modified anywhere during runtime.
6. **Actual Behavior:**  
   Runtime side-effect file creation causes crashes on read-only filesystems.
7. **Relevant Standards:**  
   PEP 517 / FHS / Read-Only Packaging Standards.
8. **Dependencies & Interacting Defects:** Independent.
9. **Potential Regression Risks:**  
   Missing packaged database must fail with a descriptive `FileNotFoundError`, not an unhandled SQLite operational error.
10. **Proposed Fix Specification:**  
    1. Pre-build `weather.sqlite` deterministically as package data.
    2. Open SQLite connection strictly read-only: `sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)`.
    3. Remove `executescript` on connect at runtime.
    4. Remove default `db_name='weather.sqlite'`; require explicit anchored path.
    5. Disallow runtime writes; enforce zero filesystem pollution.

---

### DEF-11: Girder Count Geometry Misalignment (Edge Lines Counted in Config)

1. **Original Observation:**  
   `BridgeConfig.from_plate_girder_bridge` set `bcfg.geometry.n_girders = geom.n_l` (6 instead of 4).
2. **Current Source Location & Call Path:**  
   `src/osdagbridge/core/bridge_types/plate_girder/designer.py:401, 413, 430`.
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Baseline test `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` fails (`n_girders = 6`, expected 4).
4. **Reproduction Procedure:**  
   Run `test_tc_reg_geo_count()`. Check `bcfg.geometry.n_girders`. Evaluates to 6.
5. **Expected Engineering Behavior:**  
   `bcfg.geometry.n_girders` must represent the physical longitudinal plate girders ($N=4$). *(Severity is Medium reporting accuracy: per-girder design loops correctly use `_girder_count()`, so no index errors occur at baseline).*
6. **Actual Behavior:**  
   Reporting config reflects mesh grid line count ($6$) rather than girder count ($4$).
7. **Relevant Standards:**  
   Grillage Modeling Guidelines.
8. **Dependencies & Interacting Defects:** Independent reporting field; placed in Batch 1.
9. **Potential Regression Risks:** None.
10. **Proposed Fix Specification:**  
    In `designer.py:401`, change `n_girders = geom.n_l` to `n_girders = bridge._girder_count()`.

---

### DEF-12: Bearing Stiffener Web Buckling Capacity Formula Anomaly

1. **Original Observation:**  
   `compute_bearing_stiffener()` reported web buckling capacity as $214,533.2\text{ kN}$ instead of code-compliant capacity.
2. **Current Source Location & Call Path:**  
   `src/osdagbridge/core/bridge_types/plate_girder/designer.py:1664–1672`.
   Mechanism: Plugged stiffener plate inertia `Iys` into unstiffened web buckling slenderness `rys_wb = math.sqrt(Iys / A_wb)` and evaluated unreduced Euler stress.
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Baseline test `TC-REG-CAP-STIFFENER-BUCKLING` fails ($214,533.2\text{ kN}$ vs oracle).
4. **Reproduction Procedure:**  
   Run `test_tc_reg_cap_stiffener()`. Check `Fcdw_wb_kN`.
5. **Expected Engineering Behavior:**  
   Per IS 800:2007 Cl. 8.7.3.1 & Cl. 7.1.2.1 curve c ($\alpha = 0.49, \gamma_{m0} = 1.10, E = 2 \times 10^5\text{ MPa}$):
   - **For Unified Test Fixture Inputs ($t_w = 10\text{ mm}, d = 1300\text{ mm}, b_1 = 100\text{ mm}, f_y = 250\text{ MPa}$):**
     $$r_y = \frac{t_w}{\sqrt{12}} = \frac{10}{\sqrt{12}} = 2.8868\text{ mm}$$
     $$KL = 0.7 \times 1300 = 910\text{ mm} \implies \lambda = \frac{910}{2.8868} = 315.23$$
     $$f_{cc} = \frac{\pi^2 E}{\lambda^2} = 19.86\text{ MPa}, \quad \lambda_{\text{non-dim}} = \sqrt{\frac{250}{19.86}} = 3.548$$
     $$\phi = 0.5[1 + 0.49(3.548 - 0.2) + 3.548^2] = 7.114$$
     $$\chi = \frac{1}{\phi + \sqrt{\phi^2 - \lambda^2}} = 0.06969 \implies f_{cd} = \frac{0.06969 \times 250}{1.1} = \mathbf{15.839\text{ MPa}}$$
     $$A_{wb} = (b_1 + n_1) t_w = (100 + 650) \times 10 = 7500\text{ mm}^2$$
     $$F_{cdw} = \frac{15.839 \times 7500}{1000} = \mathbf{118.79\text{ kN}} \quad (\mathbf{118.8\text{ kN}})$$
   - *(Note on Sealed 63.4 kN Oracle: $63.4\text{ kN}$ corresponds to a separate fixture with $t_w = 8\text{ mm}, d = 1304\text{ mm}, b_1 = 101.81\text{ mm}, f_y = 350\text{ MPa}$, where $\lambda = 395.25 \implies f_{cd} = 10.51\text{ MPa}, A_{wb} = 6030.5\text{ mm}^2 \implies F_{cdw} = 63.40\text{ kN}$).*
6. **Actual Behavior:**  
   Uses stiffener `Iys` and Euler formula, overpredicting capacity by thousands of kilonewtons.
7. **Relevant Standards:**  
   IS 800:2007 Cl. 8.7.3.1 & Cl. 7.1.2.1; IRC 24:2010 Cl. 509.7.3.1.
8. **Dependencies & Interacting Defects:** Independent capacity formula; placed in Batch 1.
9. **Potential Regression Risks:**  
   Boundary conditions: $KL = 0.7d$ assumes restrained compression flange; for unrestrained flange $KL = 1.0d \implies F_{cdw} = 60.5\text{ kN}$. At girder end supports, $n_1$ dispersion and $20t_w$ web strip must be one-sided.
10. **Proposed Fix Specification:**  
    In `designer.py:1664–1672`, compute $r_y = t_w / \sqrt{12}$, evaluate $f_{cd}$ via `IS800_2007.cl_7_1_2_1_...` with curve c, account for end-support dispersion, and compute $F_{cdw} = f_{cd} A_{wb} / 1000$.

---

### DEF-13: Hardcoded Structural Steel and Deck Concrete Density Propagation

1. **Original Observation:**  
   User material densities were ignored; self-weight line loads always used hardcoded $78.5\text{ kN/m}^3$.
2. **Current Source Location & Call Path:**  
   `analyser.py:416` (`beam_mag = girder_self_weight_kN_m(A_girder_m2, STEEL_UNIT_WEIGHT_kN_m3)`).  
   `plategirderbridge.py:1332` (`model.create_self_weight_load()` has no density parameter).  
   Deck density: `plategirderbridge.py:1333` calls `create_deck_load()` with default $25.0\text{ kN/m}^3$, ignoring `material.deck.density`.
3. **Baseline Existence:**  
   **CONFIRMED (IV+SE).** Baseline test `TC-REG-MAT-DENSITY-CONSISTENCY` fails ($169.8\text{ kN}$ vs $151.4\text{ kN}$ target).
4. **Reproduction Procedure:**  
   Run `test_tc_reg_mat_density()`. Set custom steel density $70.0\text{ kN/m}^3$. Verify self-weight load.
5. **Expected Engineering Behavior:**  
   `create_self_weight_load` and `create_deck_load` must accept dynamic density arguments read from user input. For the unified fixture with derived area $A = 0.032400\text{ m}^2$ at $\rho_s = 70.0\text{ kN/m}^3$:
   $$P_{SW} = 4 \times 24.0 \times 0.032400 \times 70.0 = \mathbf{217.728\text{ kN}}$$
   *(At baseline unsynchronized area $0.022534\text{ m}^2 \implies 151.431\text{ kN}$).*
6. **Actual Behavior:**  
   Ignores user input; always uses hardcoded constants.
7. **Relevant Standards:**  
   IRC:6-2017 Clause 202.1 & Table 1.
8. **Dependencies & Interacting Defects:** Oracle sequenced after `DEF-03` derived area.
9. **Potential Regression Risks:**  
   Updating `create_self_weight_load` signature requires updating default parameter handling.
10. **Proposed Fix Specification:**  
    Update `create_self_weight_load` signature in `analyser.py:371` to accept `density_kN_m3: float | None = None`. In `plategirderbridge.py:1332–1333`, query `material.girder.density` and `material.deck.density` and pass to both methods.

---

### DEF-14: Transverse Concrete Deck Slab Assigned Steel Girder Properties (DEC-013)

1. **Original Observation:**  
   Transverse grillage members were assigned halved steel plate girder properties (`girder/2`, $I_z \approx 0.00367\text{ m}^4$).
2. **Current Source Location & Call Path:**  
   `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1279–1291` (`_transverse_section`).
3. **Baseline Existence:**  
   **CONFIRMED (BLOCKED under DEC-013).** Kept formally blocked.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_geo_slab()`. Confirms `BLOCKED (DEC-013)`.
5. **Expected Engineering Behavior:**  
   Transverse grillage members represent concrete deck slab strips ($b = s_{\text{node}} = 1.5\text{ m}, d_s = 0.25\text{ m}, m = E_s / E_c = 6.45$).
   $$I_{\text{trans, steel-equiv}} = \frac{b \cdot d_s^3}{12 \cdot m} = \frac{1.5 \times (0.25)^3}{12 \times 6.45} = \mathbf{3.028 \times 10^{-4}\text{ m}^4}$$
   Torsion constant $J \approx b d_s^3 / 6$ per Hambly.
6. **Actual Behavior:**  
   Halves longitudinal steel plate girder properties.
7. **Relevant Standards:**  
   IRC:112-2019; Hambly Bridge Deck Behaviour.
8. **Dependencies & Interacting Defects:** DEC-013.
9. **Potential Regression Risks:** Transverse distribution ratios change.
10. **Proposed Fix Specification:** Retain blocked status until DEC-013 is signed off by engineering owner.

---

### DEF-17: Fatigue Vehicle Moving Load Analysis Pipeline Omission (DEC-018)

1. **Original Observation:**  
   IRC 6:2017 Clause 204.6 fatigue vehicle moving load was never analyzed in grillage.
2. **Current Source Location & Call Path:**  
   `src/ospgrillage/load.py:1793–1847` defines the vehicle. `analyser.py:1612–1660` generates Class A and Class 70R only.
3. **Baseline Existence:**  
   **CONFIRMED (BLOCKED under DEC-018).** Kept formally blocked.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_c02()`. Confirms `BLOCKED (DEC-018)`.
5. **Expected Engineering Behavior:**  
   Per IRC 6:2017 Clause 204.6 and `ospgrillage/load.py:1793–1847`, the fatigue vehicle is a **40-tonne 3-axle truck**:
   - Axle 1: $12\text{ t} = 117.72\text{ kN}$
   - Axle 2: $14\text{ t} = 137.34\text{ kN}$ (at $4.500\text{ m}$ spacing)
   - Axle 3: $14\text{ t} = 137.34\text{ kN}$ (at $1.400\text{ m}$ spacing)
   - Total Load: $392.40\text{ kN}$ across $5.900\text{ m}$ wheelbase.
   - Simply Supported Moment Envelope on $24\text{ m}$ Span: **1996.42 kNm** (occurs under middle axle at $x = 12.43\text{ m}$ when front axle is at $x = 7.93\text{ m}$).
6. **Actual Behavior:**  
   Fatigue vehicle pass completely omitted from analysis.
7. **Relevant Standards:**  
   IRC:6-2017 Clause 204.6; IRC:22-2015 Clause 605.
8. **Dependencies & Interacting Defects:** DEC-018.
9. **Potential Regression Risks:** Analysis runtime increases by ~15s.
10. **Proposed Fix Specification:** Retain blocked status until DEC-018 is ratified. Implement dedicated single-vehicle moving load pass.

---

### DEF-18: Non-Conservation of Static Load Equilibrium & End-Bay Drop

1. **Original Observation:**  
   OpenSees grillage reactions lost $-37.5\%$ of barrier load and shifted longitudinal centroid by $+0.750\text{ m}$.
2. **Current Source Location & Call Path:**  
   `src/ospgrillage/osp_grillage.py:1674–1729` (`_assign_line_to_four_node`), `1795–1850` (`_assign_patch_load`).
   Four distinct source mechanisms:
   1. *Intensity instead of Force:* Line 1726 sets `mag = W` (intensity in N/m) instead of $W \times L$.
   2. *Dropped End-Bay:* Line 1676 `if "ends" not in points.keys(): continue` skips the first mesh bay entirely, causing the remaining 15 of 16 bays to shift the centroid to $(1.5 + 24)/2 = \mathbf{12.750\text{ m}}$.
   3. *Interpolation y/z Index Swap:* Lines 1713–1714 call `interpolate_udl_magnitude([p1[0], 0, p1[1]])`, passing y instead of z.
   4. *Patch Over-Integration:* Overlapping polygon boundary integration scales deck and wearing course patch areas upwards by $+2.9\%\text{–}+3.9\%$.
3. **Baseline Existence:**  
   **CONFIRMED (IV+IR+SE).** Sealed log `tc_reg_eq_load_conservation.log` confirms $-117.72\text{ kN}$ barrier shortfall, $\Delta x = +0.750\text{ m}$, and $+3.09\%$ patch inflation.
4. **Reproduction Procedure:**  
   Run `test_tc_reg_eq_load_conservation()`. Sum OpenSees nodal support reactions across load groups.
5. **Expected Engineering Behavior:**  
   Universal invariants 1, 2, and 3 must hold:
   - Total force conservation: $|\Sigma R_y - \Sigma P| \le 10^{-6} \cdot \Sigma P + 1\text{ N}$.
   - Centroid conservation: $|\bar{x}_R - \bar{x}_P| \le 10^{-6} \cdot L$.
   - Segment force and first-moment conservation: $\int w(x) dx$ and $\int w(x) x dx$ exact.
6. **Actual Behavior:**  
   Loses first bay of line loads and over-integrates patch loads.
7. **Relevant Standards:**  
   Fundamental Laws of Statics ($\Sigma F_y = 0, \Sigma M = 0$).
8. **Dependencies & Interacting Defects:** Independent of stiffness; placed in Batch 2.
9. **Potential Regression Risks:** Must be verified on asymmetric line loads, non-uniform loads, and skewed meshes.
10. **Proposed Fix Specification:**  
    In `osp_grillage.py`:
    1. Set `mag = W * L` in `_assign_line_to_four_node()`.
    2. Fix grid intersection logic to retain end bays without coordinate skipping.
    3. Correct interpolation index to pass z-coordinate: `[p1[0], 0, p1[2]]`.
    4. Replace patch polygon summation with exact numerical cell-integration.

---

### DEF-19: Live-Load Factor Composition Omission (Lane Factors & DLA Dropped)

1. **Original Observation (New Latent Defect identified in Claude Audit §3 DEF-01):**  
   Lane-reduction factors (IRC 6 Table 6A) and Dynamic Load Allowance / Impact Factor (IRC 6 Cl. 208) are silently lost from the governing live-load case and all load combinations.
2. **Current Source Location & Call Path:**  
   - Lane factors applied per entry in vehicle cases: `analyser.py:1836` (`lc.add_load(load=vehicle, load_factor=lane_factor)`).
   - DLA computed and applied only at case level to vehicle sub-cases: `analyser.py:1803, 1841`.
   - In `analyser.py:2025–2027` (`create_governing_ll_load_case`): Copies `LL.add_load(entry["load"])`, dropping `entry["factor"]`.
   - In `plategirderbridge.py:635`: `LL` is registered with `partial_safety_factor=1.0` only.
   - In `analyser.py:2348` (`create_uls_combinations`): Copies `LL` entries without lane factors or DLA.
3. **Baseline Existence:**  
   **CONFIRMED (IV).** Verified by code inspection of `analyser.py` call chain.
4. **Reproduction Procedure:**  
   Construct a bridge model with multi-lane Class A traffic. Inspect loads in `self.ll_load_case` and combination `BASIC_1`. Verify that lane reduction factors and DLA impact multiplier ($1 + \text{impact} \approx 1.15$) are absent.
5. **Expected Engineering Behavior:**  
   Governing live load and combinations must include both lane-reduction factors and DLA impact factor:
   $$\text{Live Load Factored Demand} = \gamma_Q \times \text{DLA} \times \sum (\text{Lane Factor}_i \times P_i)$$
   For a $24\text{ m}$ span under IRC 6 Cl. 208, impact factor is $\approx 15\%$, so dropping it is unconservative by ~15%.
6. **Actual Behavior:**  
   Copies raw unscaled vehicle loads, dropping lane reduction and impact factors.
7. **Relevant Standards:**  
   IRC:6-2017 Clause 204.4 (Table 6A Multi-Lane Reduction Factors) & Clause 208 (Dynamic Load Allowance).
8. **Dependencies & Interacting Defects:** Tightly coupled to `DEF-01` factor composition; remediated together in Batch 3.
9. **Potential Regression Risks:**  
   Changing live load scaling will alter the governing vehicle combination selection.
10. **Proposed Fix Specification:**  
    In `analyser.py`, ensure that when `create_governing_ll_load_case` aggregates loads from the governing vehicle case, each vehicle entry retains its lane reduction factor multiplied by DLA. In `_copy_loads`, compound all entry factors with the combination live-load factor $\gamma_Q = 1.50$.
