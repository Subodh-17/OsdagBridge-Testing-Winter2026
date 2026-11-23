# PHASE 2 REGRESSION TEST PLAN & QUALITY SPECIFICATION

**Workspace:** `F:\FOSSEE internship`  
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`  
**Reference Baseline:** Commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev` branch)  
**Environment:** `osdagbridge-py312` (Python 3.12.16 | conda-forge / PyPI isolated)  
**Date:** 2026-11-16  
**Status:** **ACTIVE SPECIFICATION — BASELINE REGRESSION HARNESS**  

---

## 1. Scope, Architecture & Testing Strategy

This test plan defines the official Phase 2 regression test harness for OsdagBridge. Following the independent review reconciliation (`PHASE_2_REVIEW_RECONCILIATION.md`), all previously identified flawed test assertions (tautologies, incorrect API attributes, unmapped key injections) have been eliminated and replaced with mathematically sound, code-verified specifications.

### Core Testing Mandates
1. **Verified API Invariants:** Every attribute name, method signature, and data structure has been verified against the physical codebase (e.g. `girder_props[i].Iz`, `_copy_loads`, `cl_204_6_fatigue_load`).
2. **Intentional Baseline Failure:** A regression test is valid only if it fails against baseline commit `d74f56d` for the specific defect mechanism, and passes after a correct fix. Tests that fail due to unhandled `AttributeError`, `ImportError`, or test-setup flaws are strictly rejected.
3. **No Arbitrary Numbers:** All assertions use mathematical identities (linear superposition, equilibrium $\sum M = w L^2 / 8$, subset invariance) or application-derived relationships rather than invented engineering constants.
4. **Side-Effect-Free Execution:** Tests must not write files into tracked or ignored directories within `source/OsdagBridge/`.

---

## 2. Primary Regression Test Specifications (Priority A to D)

### TC-REG-A01-FACTOR-SCALING
- **Defect Identifier:** DEF-01 (`ospgrillage` load factor omission in `add_load`)
- **Test Type:** Unit Regression Test (isolated `ospgrillage`)
- **Preconditions:** Fresh OpenSees domain (`ops.wipe()`), vendored `ospgrillage` importable.
- **Exact Controlled Input:** 
  Minimal 2-girder grillage ($L = 10.0\text{ m}$, spacing $= 2.0\text{ m}$). Define a static `LineLoading` $w = 10.0\text{ kN/m}$.
  - Case U (Unfactored): `lc_u.add_load(line_load)` ($\gamma_f = 1.0$)
  - Case F (Factored): `lc_f.add_load(line_load, load_factor=1.35)`
- **Expected Behavior:** OpenSees linear static analysis requires all member forces and nodal displacements to scale by exactly $1.35\times$: $\mathbf{F}_F = 1.35 \cdot \mathbf{F}_U$.
- **Observable Output:** Member force arrays ($M_z, V_y$) extracted via `model.get_results()`.
- **Assertion Strategy:**
  1. Pre-assertion: `assert np.max(np.abs(F_U)) > 0` (guards against vacuous pass).
  2. Scaling assertion: `np.testing.assert_allclose(F_F, 1.35 * F_U, rtol=1e-7, atol=1e-7)`.
- **Baseline Failure Expectation:** Fails: $F_F == F_U$ (ratio = 1.00000) because `_distribute_load_types_to_model` reads only `load_dict["load"]` and ignores `load_dict["factor"]`.
- **Potential False Positives:** Calling `ospgrillage.add_load_combination()` instead of testing the `add_load(..., load_factor=...)` path used by OsdagBridge's `_copy_loads`.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_a01.log`

---

### TC-REG-B01-SECTION-PROPERTY-SYNC
- **Defect Identifier:** DEF-03 (preliminary vs. snapped plate sizing mismatch)
- **Test Type:** Integration Regression Test (`plategirderbridge.py` Stage 1 to 3, no solver execution)
- **Preconditions:** Bridge sizing initialized in `Optimized` mode with flange/web thicknesses set to `"All"`.
- **Exact Controlled Input:** Canonical Phase 1D input dict ($L = 24.0\text{ m}, W_{cw} = 7.5\text{ m}$, E 350A steel).
- **Expected Behavior:** After `_resolve_optimized_bounds_to_mm` snaps plate dimensions to commercial SAIL thicknesses ($t_f = 18\text{ mm}, t_w = 8\text{ mm}$), the section properties assigned to OpenSees (`grillage_model.girder_props[i]`) must equal the analytical properties of the snapped cross-section.
- **Observable Output:** `bridge.grillage_model.girder_props[i].Iz`, `.Iy`, `.A`, `.J`.
- **Assertion Strategy:**
  Extract snapped plate dimensions from `bridge.input_dict` (`B_top`, `t_f_top`, `d_web`, `t_w`, `B_bot`, `t_f_bot`). Compute analytical properties using `BridgeConfigurationSolver.compute_section_properties()`.
  Assert relative difference:
  $$\left| \frac{\text{assigned } I_z}{\text{analytical } I_z} - 1.0 \right| < 10^{-6}, \quad \left| \frac{\text{assigned } A}{\text{analytical } A} - 1.0 \right| < 10^{-6}$$
- **Baseline Failure Expectation:** Fails: Assigned $I_z = 0.0073409\text{ m}^4$ vs. analytical snapped $I_z = 0.0079276\text{ m}^4$ (7.4% discrepancy; $A$ has 10.6% discrepancy).
- **Potential False Positives:** Querying non-existent attribute `.I_z` instead of verified attribute `.Iz`.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_b01.log`

---

### TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect Identifier:** DEF-07 (fatigue stress range doubled via member-end sign flip)
- **Test Type:** Unit Regression Test (`PlateGirderDesigner.check_fatigue` isolated mathematical evaluation)
- **Preconditions:** Isolated evaluation harness with known elastic section modulus $Z_e$.
- **Exact Controlled Input:** 
  Synthetic xarray dataset matching `analysis_results.ds` schema with member end components `Mz_i` and `Mz_j`.
  - Case 1 (Static constant moment): Constant sagging moment $M_0 = 1000\text{ kNm}$ on element 1 across all SLS Frequent combinations (opposite local signs: $M_{z\_i} = +1000, M_{z\_j} = -1000$). No live load variation.
  - Case 2 (Cyclic variation): Constant $M_0$ plus cyclic range $\pm \Delta M = \pm 200\text{ kNm}$.
- **Expected Behavior:** 
  Fatigue evaluates cyclic stress range $\Delta \sigma$ at a discrete cross-section under live load variation.
  - Case 1: Zero variation $\implies \Delta \sigma == 0.0\text{ MPa}$.
  - Case 2: $\Delta \sigma == 2 \Delta M / Z_e == 400\text{ kNm} / Z_e$.
  - Invariance: $\Delta \sigma$ must not change if static dead load $M_0$ is doubled.
- **Observable Output:** Computed `stress_range_MPa` from fatigue check.
- **Assertion Strategy:**
  - Case 1: `assert stress_range_case1 == 0.0` (abs tol $10^{-9}$).
  - Invariance: `assert stress_range(2 * M_0) == stress_range(M_0)`.
- **Baseline Failure Expectation:** Fails: Case 1 returns $2 M_0 / Z_e \approx 182.63\text{ MPa}$ because `max(mz_all) - min(mz_all)` conflates $+M_{z\_i}$ with $-M_{z\_j}$.
- **Potential False Positives:** Asserting $\Delta M(x) \le \Delta M_{global}$ (mathematical tautology that always passes).
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_c01.log`

---

### TC-REG-A02-ULS-COMBINATION-SUM
- **Defect Identifier:** DEF-01 (factors) & DEF-02 (SIDL omission)
- **Test Type:** Integration Regression Test (Combination assembly pipeline)
- **Preconditions:** Grillage model built with static dead load ($DL$), crash barrier SIDL ($SIDL$), and live load ($LL$).
- **Exact Controlled Input:** Phase 1D benchmark configuration.
- **Expected Behavior:** Member force vector for ULS Basic Combination 1 must equal the linear combination of constituent cases using application partial safety factors:
  $$\mathbf{F}_{ULS1} = \gamma_{DL} \mathbf{F}_{DL} + \gamma_{SIDL} \mathbf{F}_{SIDL} + \gamma_{LL} \mathbf{F}_{LL}$$
- **Observable Output:** Member force arrays across all elements.
- **Assertion Strategy:**
  1. Sub-test A02a (Superposition): `np.testing.assert_allclose(F_ULS1, sum(gamma_j * F_j), rtol=1e-5)` where $\gamma_j$ are read dynamically from combination metadata.
  2. Sub-test A02b (SIDL Completeness): Assert that `F_SIDL` is non-zero and included in the combination's component list.
  3. Sub-test A02c (Distinctness): Assert that combinations with distinct factor vectors produce distinct force arrays (fails on baseline where 18 combinations return identical forces).
- **Baseline Failure Expectation:** A02a fails (factors ignored); A02b fails (`sidl_combination` is None); A02c fails (18 combinations identical).
- **Potential False Positives:** Hardcoding factors ($1.35, 1.75, 1.50$) rather than dynamically querying the application's $\gamma$ table.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_a02.log`

---

### TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect Identifier:** DEF-05 (wind parameters ignored across 5 unmapped keys)
- **Test Type:** Unit/Integration Regression Test (`PlateGirderBridge.add_wind_load`)
- **Preconditions:** Initialized `PlateGirderBridge` instance.
- **Exact Controlled Input:** 
  Input dictionary structured strictly through GUI hierarchy:
  - `project.location.weather_data.wind_speed = 47.0`
  - `loading.wind_load.avg_exposed_height = 15.0`
  - `loading.wind_load.terrain_type = "Obstacle Terrain"`
  - `typical_section.railing.height = 1.2`
  - `typical_section.crash_barrier.height = 1.1`
  - **No bare un-prefixed keys** (`basic_wind_speed`, `avg_exposed_height`, etc.).
- **Expected Behavior:** `add_wind_load()` must map the hierarchical input keys and pass non-default arguments to `grillage_model.create_wind_load()`.
- **Observable Output:** Call arguments intercepted via mock spy on `grillage_model.create_wind_load`.
- **Assertion Strategy:**
  Assert spy was called with:
  - `basic_wind_speed == 47.0` (not 33.0)
  - `height_for_pz == 15.0` (not 10.0)
  - `terrain == "obstructed"` (not "plain")
  - `railing_height == 1.2` (not 0.0)
  - `crash_barrier_height == 1.1` (not 0.0)
- **Baseline Failure Expectation:** Fails: All 5 arguments receive hardcoded fallbacks ($33.0, 10.0, \text{"plain"}, 0.0, 0.0$) because line 1381 queries un-prefixed keys.
- **Potential False Positives:** Injecting `ai["basic_wind_speed"] = 47.0` in the test input, which erroneously masks the defect.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_d01.log`

---

## 3. Additional Regression Test Specifications (Stage 3 Coverage)

### TC-REG-D02-TEMPERATURE-PROPAGATION
- **Defect Identifier:** DEF-06 (temperature load unmapped)
- **Test Type:** Integration Regression Test (`PlateGirderBridge.add_temperature_load`)
- **Preconditions:** Bridge instance initialized with project location temperature range ($T_{max} = 45^\circ\text{C}, T_{min} = -5^\circ\text{C}$).
- **Controlled Input:** Canonical input dictionary with valid location weather data.
- **Expected Behavior:** `add_temperature_load()` must compute effective temperature range per IRC:6 Cl. 215, create non-empty temperature load cases (`TEMP_FALL`, `TEMP_RISE`), and factor them into temperature-inclusive combinations without emitting warnings.
- **Assertion Strategy:**
  1. `assert bridge.grillage_model.load_cases.get("TEMP_FALL") is not None`.
  2. Assert non-zero element load intensities in `TEMP_FALL`.
- **Baseline Failure Expectation:** Fails: `temperature_load_kN_m2` is absent, and the function silently returns without creating any load case.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_d02.log`

---

### TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Defect Identifier:** DEF-17 (fatigue vehicle defined but omitted from moving load analysis)
- **Test Type:** Integration Regression Test (`PlateGirderBridge.run_moving_load_analysis`)
- **Preconditions:** Grillage model with moving load analyzer initialized.
- **Controlled Input:** Bridge configuration with fatigue design enabled.
- **Expected Behavior:** Moving load analysis must include the IRC:6 Cl. 204.6 40-tonne 3-axle fatigue vehicle ($12\text{t} + 14\text{t} + 14\text{t}$ at $4.5\text{ m}, 1.4\text{ m}$) as a discrete moving load case, storing its response history.
- **Assertion Strategy:**
  `assert "FATIGUE_VEHICLE" in bridge.grillage_model.moving_load_cases`.
- **Baseline Failure Expectation:** Fails: Moving load analysis only iterates over Class A and Class 70R vehicles; fatigue truck is never analyzed.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_c02.log`

---

### TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect Identifier:** DEF-08 (hardcoded outcome text in report generator)
- **Test Type:** Unit Regression Test (`src/osdagbridge/core/reports/executive_summary.py`)
- **Preconditions:** Report generator payload populated with an overall status of `"FAIL"` (e.g. fatigue DCR = 1.9746).
- **Controlled Input:** Payload where `overall_design_status = "FAIL"`, `fatigue_status = "FAIL"`.
- **Expected Behavior:** The executive summary section must not output literal text claiming "Girder design pass" or "pass" for failed components.
- **Assertion Strategy:**
  Render LaTeX via `generate_executive_summary(payload)`.
  Assert `"Girder design pass"` is NOT present in the generated LaTeX when girder fatigue fails.
- **Baseline Failure Expectation:** Fails: `executive_summary.py:233` contains hardcoded literal `\noindent Girder design pass \\ ...`.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_rpt_status.log`

---

### TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect Identifier:** DEF-11 (grillage edge lines counted as main girders in designer)
- **Test Type:** Unit/Integration Regression Test (`PlateGirderDesigner.from_plate_girder_bridge`)
- **Preconditions:** Bridge instance with 4 physical main girders and 2 slab overhang edge lines (`geom.n_l = 6`).
- **Controlled Input:** Canonical 4-girder bridge configuration.
- **Expected Behavior:** `designer.n_girders` and `design_results.n_girders` must equal the number of fabricated steel plate girders (4), NOT the total number of grillage lines (6).
- **Assertion Strategy:**
  `designer = PlateGirderDesigner.from_plate_girder_bridge(bridge)`  
  `assert designer.n_girders == 4` (fails on baseline where `designer.n_girders == 6`).
- **Baseline Failure Expectation:** Fails: Line 401 sets `n_girders = geom.n_l`, returning 6.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_geo_count.log`

---

### TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Defect Identifier:** DEF-14 (transverse slab takes steel plate girder properties)
- **Test Type:** Unit Regression Test (`plategirderbridge.py:_transverse_section`)
- **Preconditions:** Initialized `PlateGirderBridge` instance with defined deck slab thickness ($t_{slab} = 250\text{ mm}$).
- **Controlled Input:** Canonical bridge configuration.
- **Expected Behavior:** Transverse grillage members represent concrete slab strips; their moment of inertia $I_z$ must reflect transformed concrete slab properties ($b t_{slab}^3 / 12m$), NOT half of the steel plate girder's moment of inertia.
- **Assertion Strategy:**
  `transverse = bridge._transverse_section()`  
  `assert transverse.Iz != bridge._girder_section().Iz / 2.0`
- **Baseline Failure Expectation:** Fails: Line 1287 assigns `Iz = g(KEY_MP_GIRDER_SECTIONAL_IZ) / 2`.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_geo_slab.log`

---

### TC-REG-CAP-STIFFENER-BUCKLING
- **Defect Identifier:** DEF-12 (bearing stiffener web buckling capacity anomaly)
- **Test Type:** Unit Regression Test (`PlateGirderDesigner.compute_bearing_stiffener`)
- **Preconditions:** Designer instance with support reaction $R = 304.97\text{ kN}$.
- **Controlled Input:** Sized plate girder section ($1340 \times 410 \times 18\text{ mm}$, E 350A steel).
- **Expected Behavior:** Stiffener web buckling capacity $F_{cdw, wb}$ must be bounded by the steel yield strength ($f_y / \gamma_{m0}$) and must not exceed the stiffener's column squash capacity $F_{cd}$.
- **Assertion Strategy:**
  `res = designer.compute_bearing_stiffener()`  
  `assert res["Fcdw_wb_kN"] <= res["Fcd_kN"] * 1.5` (or bounded by yield).
- **Baseline Failure Expectation:** Fails: `res["Fcdw_wb_kN"]` evaluates to $134,083.2\text{ kN}$ due to unbounded Euler elastic stress calculation.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_cap_stiffener.log`

---

### TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect Identifier:** DEF-13 (hardcoded densities vs. database values)
- **Test Type:** Unit Regression Test (`BridgeGrillageModel.create_model`)
- **Preconditions:** `BridgeGrillageModel` instance initialized with material properties.
- **Controlled Input:** Material properties with steel density $76.4\text{ kN/m}^3$ and concrete density $24.5\text{ kN/m}^3$.
- **Expected Behavior:** Applied self-weight line loads must use the density specified in the material properties, not hardcoded constants ($78.5\text{ kN/m}^3$ and $25.0\text{ kN/m}^3$).
- **Assertion Strategy:**
  Inspect self-weight load magnitude:
  `assert model.load_cases["SELF_WEIGHT"].magnitude == pytest.approx(A_steel * 76.4, rel=1e-3)`
- **Baseline Failure Expectation:** Fails: `analyser.py:374` multiplies area by literal `78.5`.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_mat_density.log`

---

### TC-REG-FS-CLEAN-WORKING-TREE
- **Defect Identifier:** DEF-10 (`weather.sqlite` creation in source tree)
- **Test Type:** Integration Regression Test (Clean tree invariant)
- **Preconditions:** Snapshot of repository working tree.
- **Controlled Input:** Invoke project location lookup (`zone_lookup.py`) and full bridge initialization.
- **Expected Behavior:** Application runtime must not create, modify, or delete any files inside `source/OsdagBridge/`.
- **Assertion Strategy:**
  Compare before/after filesystem state across all files (including git-ignored files).
  `assert new_files_in_source_tree == []`
- **Baseline Failure Expectation:** Fails: Generates `src/osdagbridge/core/data/project_location/weather.sqlite` (180,224 bytes).
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_fs_clean.log`

---

### TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Defect Identifier:** DEF-09 (CAD capture transparency)
- **Test Type:** Integration Regression Test (Headless CAD export)
- **Preconditions:** Initialized `PlateGirderCADGenerator` with generated solid shapes.
- **Controlled Input:** Canonical 24m plate girder bridge CAD model.
- **Expected Behavior:** CAD rendering export via OpenCASCADE native `ExportToImage()` or `View.Dump()` must produce an image with $\ge 20\%$ non-background, non-transparent pixels.
- **Assertion Strategy:**
  Export image to PNG and analyze alpha/RGB channels:
  `assert non_transparent_pixel_ratio >= 0.20`
- **Baseline Failure Expectation:** Fails when using Qt `widget.grab()` (92.95% transparent pixels); passes when using native OpenCASCADE dump.
- **Evidence Location:** `testing/evidence/phase_2_baseline/tc_reg_cad_export.log`

---

## 4. Test Execution Framework & Directory Layout

All regression tests are organized under:
```
testing/
├── test_cases/
│   └── baseline_regression/
│       ├── test_tc_reg_a01_factor_scaling.py
│       ├── test_tc_reg_b01_section_sync.py
│       ├── test_tc_reg_c01_stress_range.py
│       ├── test_tc_reg_a02_combination_sum.py
│       ├── test_tc_reg_d01_wind_propagation.py
│       ├── test_tc_reg_d02_temperature.py
│       ├── test_tc_reg_c02_fatigue_truck.py
│       ├── test_tc_reg_rpt_status.py
│       ├── test_tc_reg_geo_count.py
│       ├── test_tc_reg_geo_slab.py
│       ├── test_tc_reg_cap_stiffener.py
│       ├── test_tc_reg_mat_density.py
│       ├── test_tc_reg_fs_clean.py
│       └── test_tc_reg_cad_export.py
└── evidence/
    └── phase_2_baseline/
        └── *.log
```
