# PHASE 2.11 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_11\`  

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

### Summary Statistics
- **Total Registered Regression Tests:** **15**
- **Actionable Tests Verified:** **12 / 12 (100.0%)**
- **Actionable Tests Unverified:** **0 / 12 (0.0%)**
- **Formally Blocked Specifications:** **3 / 15** (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Manifest Alignment Accuracy:** **15 / 15 (100.0% Exact Match)**
- **Baseline Duration:** **27.81 s**
- **Sensitivity Matrix Duration:** **65.75 s**
- **Post-Manifest Verification:** **SUCCESS (0 file drift across all directories)**
- **Overall Actionable Sensitivity Gate:** **PASSED**

---

## 2. Detailed Technical Profiles for All 15 Tests

### 1. TC-REG-A01-FACTOR-SCALING
- **Defect Identifier:** DEF-01 (Upstream `ospgrillage` Library)
- **Defect Mechanism:** Upstream `ospgrillage` ignores `load_factor` in `LoadCase.add_load`, resulting in un-factored force ratios ($1.00000$ observed vs $1.35000$ expected).
- **Condition (a) Baseline:** `BASELINE_FAIL` (force ratio = 1.00000).
- **Condition (b) Minimal Correct:** Deepcopies and scales load magnitudes by load factor in `og.load.LoadCase.add_load`. `PASS` (force ratio = 1.35000).
- **Condition (c) Naive / Wrong:** Hardcodes arbitrary 1.15x factor. `BASELINE_FAIL` (force ratio = 1.09174 vs expected 1.35000).
- **Sensitivity Verdict:** **VERIFIED**.

### 2. TC-REG-B01-SECTION-PROPERTY-SYNC
- **Defect Identifier:** DEF-03
- **Defect Mechanism:** Section depth inconsistent with plate components ($D=1340\text{ mm} \ne 1342\text{ mm}$); solver girder section retains preliminary preliminary sizing ($I_z$ gap ~7.40%, $A$ gap ~10.55%).
- **Phase 2.11 Hardening:** Added verification of bottom flange width against configured dimensions ($b_{fb} = 410.0\text{ mm}$), discriminating bottom flange mutations (e.g. 410 -> 450 mm). Implemented general asymmetric I-section formulation (`_calc_asymmetric_i_section`) calculating exact $A$, $I_z$, $I_y$, $J$, and neutral axis $\bar{y}$ for arbitrary top and bottom flange dimensions.
- **Condition (a) Baseline:** `BASELINE_FAIL` (dimensions inconsistent: $D=1340\text{ mm} \ne 1342\text{ mm}$; solver girder sections deviate from snapped plate properties and fixed hand oracle).
- **Condition (b) Minimal Correct:** Dynamically derives snapped plate properties taking into account both top and bottom flange dimensions, updating `_girder_section` and web depth in `input_dict`. `PASS`.
- **Condition (c) Naive / Wrong:** Swaps `bgm.girder_props` metadata post-setup only, leaving solver elements and OpenSees stiffness preliminary. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect Identifier:** DEF-07
- **Defect Mechanism:** Evaluates static load case as a false cyclic stress range ($\Delta \sigma = 62.73\text{ MPa}$ instead of $0.00\text{ MPa}$) due to end-sign divergence ($+M_{z,j}$ and $-M_{z,i}$).
- **Phase 2.11 Hardening:** Replaced single-governing element fixture with a balanced multi-girder fixture: Girder G1 governing at Element 1 End $i$ ($2900\text{ kNm} \rightarrow 181.914\text{ MPa}$), Girder G2 governing at Element 5 End $j$ ($2700\text{ kNm} \rightarrow 169.358\text{ MPa}$). Evaluates sign consistency and eliminates j-end-only (C10) and i-end-only (C11) candidate escapes.
- **Condition (a) Baseline:** `BASELINE_FAIL` (static load case evaluates to false cyclic range on envelope and per-LC paths).
- **Condition (b) Minimal Correct:** Evaluates section bending moments with consistent sign convention across both ends ($i$ and $j$) for all frequent load cases, elements, and girders. `PASS`.
- **Condition (c) Naive / Wrong:** Inspects only first two load cases. `BASELINE_FAIL` (evaluates range as 1000 kNm / 62.73 MPa instead of governing 2900 kNm / 181.914 MPa).
- **Sensitivity Verdict:** **VERIFIED**.

### 4. TC-REG-A02-ULS-COMBINATION-SUM
- **Defect Identifier:** DEF-01 / DEF-02
- **Defect Mechanism:** FE solver ignores ULS combination factors in BASIC_1; crash barrier load omitted from combination.
- **Phase 2.11 Hardening:** Expected barrier resultant is derived directly from raw input keys (`loading.crash_barrier_load`, `geometry.carriageway_width`, `geometry.span`) without relying on production helper functions `crash_barrier_load_from_inputs` or `crash_barrier_dead_load_kN_m`.
- **Condition (a) Baseline:** `BASELINE_FAIL` (shears un-factored; barrier omitted; component reactions deviate; total reaction 1736.55 kN != 2710.16 kN).
- **Condition (b) Minimal Correct:** Scaled load magnitudes in `LoadCase.add_load`, creates SIDL before DL combination, sets carriageway width and densities, and applies FEM distribution. `PASS`.
- **Condition (c) Naive / Wrong:** Factors SW and DW, but omits crash barrier and FEM patch fix. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 5. TC-REG-EQ-LOAD-CONSERVATION
- **Defect Identifier:** DEF-18
- **Defect Mechanism:** Static equilibrium and transverse spatial load distribution violated in FE grillage (barrier force shortfall -37.5%, centroid shift +0.75m).
- **Phase 2.11 Hardening:** Dynamic derivation of barrier load from `input_dict.get("loading.crash_barrier_load", 6.54)` and barrier centroid offset from `typical_section.barrier_width / 2.0`. Reconciled with A02 inputs.
- **Condition (a) Baseline:** `BASELINE_FAIL` (barrier force diff -117.7 kN (-37.5%), centroid shift dx=+0.750m; DD and DW line shares deviate).
- **Condition (b) Minimal Correct:** Bilinear shape function distribution over finite element grid for patch loads and non-collinear line loads, combined with input-derived dead loads. `PASS`.
- **Condition (c) Naive / Wrong:** Distributes patch loads via FEM but leaves crash barrier line loads un-fixed. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect Identifier:** DEF-05
- **Defect Mechanism:** Baseline hardcodes basic wind speed = 33 m/s, exposed height = 10 m, barrier height = 0 m, railing height = 0 m, ignoring user inputs.
- **Condition (a) Baseline:** `BASELINE_FAIL` (wind speed 47.0 m/s ignored, defaults to 33.0 m/s; transverse wind force = 3.65 kN/m vs expected 7.42 kN/m).
- **Condition (b) Minimal Correct:** Propagates user wind speed, exposed height, crash barrier height, and railing height to `create_wind_load()`. `PASS`.
- **Condition (c) Naive / Wrong:** Reads `basic_wind_speed` only, leaves height/barrier as defaults. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 7. TC-REG-D02-TEMPERATURE-PROPAGATION
- **Defect Identifier:** DEF-06
- **Status:** **BLOCKED** under DEC-015 pending client architectural decision on IRC 6 Cl. 215 non-linear temperature gradient modeling.

### 8. TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Defect Identifier:** DEF-17
- **Status:** **BLOCKED** under DEC-018 pending client architectural decision on IRC 6 Cl. 204.6 fatigue vehicle moving load implementation.

### 9. TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect Identifier:** DEF-08
- **Defect Mechanism:** Executive summary LaTeX report hardcodes "Pass" regardless of component design results.
- **Phase 2.11 Hardening:** Strict 0.999 / 1.000 / 1.001 boundary checks across girders, deck, cross-bracing, and end diaphragms, with independent evaluation of summary text vs table overall design status.
- **Condition (a) Baseline:** `BASELINE_FAIL` (hardcoded "Pass" across all fail scenarios).
- **Condition (b) Minimal Correct:** Dynamically derives component statuses and overall design status from actual component output dictionaries. `PASS`.
- **Condition (c) Naive / Wrong:** Inspects G1 only, passes all-pass scenario but fails multi-girder fail scenario. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 10. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect Identifier:** DEF-11
- **Defect Mechanism:** `designer.py:401` sets `bcfg.geometry.n_girders = geom.n_l` (6), incorrectly counting 2 slab overhang edge lines as structural girders for a 4-girder bridge.
- **Condition (a) Baseline:** `BASELINE_FAIL` (reports 6 girders for 4-girder bridge).
- **Condition (b) Minimal Correct:** Sets `bcfg.geometry.n_girders = bridge._girder_count()` (4). `PASS`.
- **Condition (c) Naive / Wrong:** Sets `n_girders = 0`. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 11. TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Defect Identifier:** DEF-14
- **Status:** **BLOCKED** under DEC-013 pending client architectural decision on transverse slab strip representation model.

### 12. TC-REG-CAP-STIFFENER-BUCKLING
- **Defect Identifier:** DEF-12
- **Defect Mechanism:** Evaluates stiffener buckling using stiffener plate properties ($I_{ys} = 2.07\times 10^7\text{ mm}^4$) instead of web strip radius of gyration ($r_{wb} = t_w / \sqrt{12} = 2.309\text{ mm}$), overestimating buckling capacity by 3300x.
- **Condition (a) Baseline:** `BASELINE_FAIL` (capacity = 214,533 kN vs oracle 63.4 kN).
- **Condition (b) Minimal Correct:** Evaluates web strip buckling per IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 using $r_{wb} = t_w / \sqrt{12}$. `PASS`.
- **Condition (c) Naive / Wrong:** Squash load formula $(f_y / \gamma_{m0}) \times A_{wb} / 1000$, ignoring buckling entirely. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 13. TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect Identifier:** DEF-13
- **Defect Mechanism:** Dead load creation hardcodes steel unit weight to 78.5 kN/m3 from database, ignoring user input.
- **Condition (a) Baseline:** `BASELINE_FAIL` (resultant 169.8 kN matches 78.5 kN/m3 instead of configured 70.0 kN/m3 -> 151.4 kN).
- **Condition (b) Minimal Correct:** Dynamically reads `material.girder.density` and applies to self-weight line loads. `PASS`.
- **Condition (c) Naive / Wrong:** Ignores user density, retaining 78.5 kN/m3. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 14. TC-REG-FS-CLEAN-WORKING-TREE
- **Defect Identifier:** DEF-10
- **Defect Mechanism:** `ui_loc.DB_PATH` resolves inside package tree; `Database()` default constructor creates unanchored `weather.sqlite` in cwd; causes OperationalError on read-only package installations.
- **Condition (a) Baseline:** `BASELINE_FAIL` (creates `weather.sqlite` in package tree and cwd).
- **Condition (b) Minimal Correct:** Anchors database paths to User AppData directory. `PASS`.
- **Condition (c) Naive / Wrong:** Anchors UI module `DB_PATH`, but leaves `Database.__init__` unanchored, failing cwd check. `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.

### 15. TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Defect Identifier:** DEF-09 (Harness Verification)
- **Defect Mechanism:** Verifies offscreen native OpenCASCADE 3D CAD export without relying on desktop GUI screenshots.
- **Condition (a) Baseline:** `PASS` (renders opaque 3D CAD geometry with std = 66.6, 3 distinct colors).
- **Condition (b) Minimal Correct:** Standard CAD export passes. `PASS`.
- **Condition (c) Naive / Wrong:** Generates uniform blank image (std = 0.0). `BASELINE_FAIL`.
- **Sensitivity Verdict:** **VERIFIED**.
