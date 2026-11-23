# PHASE 2.6 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`)  
**Controlling Document:** `reports/PHASE_2_5_FINAL_INDEPENDENT_GATE_AUDIT.md`  
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

**Summary Statistics:**
- **Actionable Tests Verified:** **12 / 12 (100.0%)**
- **Actionable Tests Unverified:** **0 / 12 (0.0%)**
- **Formally Blocked Specifications:** **3 / 15** (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Manifest Accuracy:** **15 / 15 (100.0% Exact Match)**
- **Overall Actionable Sensitivity Gate:** **PASSED**

---

## 2. Detailed Technical Test Profiles

### 1. TC-REG-A01-FACTOR-SCALING
- **Defect:** Upstream `ospgrillage` ignores `load_factor` in `CompoundLoad` / `PointLoad` creation, resulting in un-factored force ratios ($1.00000$ observed vs $1.35000$ expected).
- **Condition (a) Baseline:** `BASELINE_FAIL` (force ratio = 1.00000).
- **Condition (b) Minimal Correct:** Scaled load magnitude by 1.35x. `PASS` (force ratio = 1.35000).
- **Condition (c) Naive / Wrong:** Scale factor 1.00. `BASELINE_FAIL` (force ratio = 1.00000).
- **Sensitivity Status:** **VERIFIED**.

### 2. TC-REG-B01-SECTION-PROPERTY-SYNC
- **Defect:** Solver grillage section properties remain out-of-sync with designed plate girder sections ($I_z$ error $\sim 7.40\%$, $A$ error $\sim 10.55\%$, web/flange depth mismatch $1340\text{ mm}$ vs $1342\text{ mm}$).
- **Analytical & Model Bounds:**
  - Single-beam isolated upper bound: $18.164\text{ mm}$.
  - Courbon 4-girder central load lower bound: $4.541\text{ mm}$.
  - Courbon 4-girder eccentric load bound: $12.71\text{ mm}$.
  - Courbon 6-line rigid factor: $0.3977 \implies 7.22\text{ mm}$ at edge line, $0.3406 \implies 6.19\text{ mm}$ under load line.
  - Transformed concrete deck slab deflection (DEF-14 / DEC-013): $6.501\text{ mm}$.
  - Calibrated grillage model consistency target: $7.218\text{ mm}$.
- **Condition (a) Baseline:** `BASELINE_FAIL` (deflection $7.816\text{ mm}$ vs $7.218\text{ mm}$, dimensions out of sync).
- **Condition (b) Minimal Correct:** Synchronizes section properties with plate formula torsional and bending constants ($I_y = 0.0002068\text{ m}^4$, $J = 1.815 \times 10^{-6}\text{ m}^4$). `PASS` (deflection $7.218\text{ mm}$, dimensions synchronized).
- **Condition (c) Naive / Wrong:** Preserves unsynchronized preliminary sections. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect:** Static load case produces false cyclic stress ranges ($125.46\text{ MPa}$ envelope due to element end $-Mz_i$ and $+Mz_j$ sign flipping; $62.73\text{ MPa}$ per-LC treating static moment as range, instead of $0.00\text{ MPa}$).
- **Phase 2.6 Refinements:**
  - Added sign-reversal load case transition: hogging ($-500\text{ kNm}$) to sagging ($+1500\text{ kNm}$), producing a true stress range of $\Delta M = 2000\text{ kNm}$ and $\Delta \sigma = 125.45\text{ MPa}$.
  - Element-end sign consistency verified across both element ends ($-Mz_i$ at end $i$, $+Mz_j$ at end $j$).
  - Evaluated static zeroing ($\Delta \sigma = 0.00\text{ MPa}$) and genuine application fatigue capacity ($f_{fd,eff} = 92.491\text{ MPa}$, $\text{DCR} = 0.6782$).
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Evaluates sign-consistent element-end moments across frequent load combinations, zeroing static envelopes and correctly computing cyclic ranges. `PASS`.
- **Condition (c) Naive / Wrong:** Naively zeroes static envelope but fails sign-reversal transition. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 4. TC-REG-A02-ULS-COMBINATION-SUM
- **Defect:** Analysis combination `BASIC_1` ignores ULS load factors (observed shears match $1.0\text{DL} + 1.0\text{DW}$ with error $1.60 \times 10^{-7}\text{ N}$; total reaction $1736.6\text{ kN}$ vs factored target $2710.2\text{ kN}$); crash barrier load is completely omitted from the combination.
- **Convention:** Applied dead load resultant $2802.70\text{ kN} \pm 0.05\%$ derived dynamically from component models. Reaction superposition target $2710.16\text{ kN} \pm 0.5\%$.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Properly assembles factored ULS combinations including crash barrier load. `PASS`.
- **Condition (c) Naive / Wrong:** Assembles combination without factoring. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 5. TC-REG-EQ-LOAD-CONSERVATION
- **Defect:** OpenSees grillage load distribution violates static equilibrium, transverse tributary line distribution, and centroid conservation:
  - Deck slab (DD): $+39.4\text{ kN}$ (+3.088% excess).
  - Wearing course (DW): $+7.6\text{ kN}$ (+3.088% excess).
  - Crash barrier line loads: $-117.7\text{ kN}$ (-37.50% shortfall), longitudinal centroid shift $\Delta x = +0.750\text{ m}$.
- **Phase 2.6 Refinements:**
  - Individual barrier centroids asserted separately: Left at $z = 0.250\text{ m} \pm 0.05\text{ m}$, Right at $z = 8.250\text{ m} \pm 0.05\text{ m}$ ($156.960\text{ kN} \pm 0.05\%$ each).
  - Transverse tributary line shares asserted for patch loads ($[6.18\%, 18.73\%, 25.10\%, 25.10\%, 18.73\%, 6.18\%]$) and barrier line loads ($76.19\%$ to line 0 / $23.81\%$ to line 1 for left; $23.81\%$ to line 4 / $76.19\%$ to line 5 for right).
  - Declared self-weight derived from `material.girder.density`.
  - Support reactions summed algebraically without `abs()`: $R_y = \sum -ops.\text{nodeReaction}(\text{node}, 2)$.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Bilinear cell-intersection distributor and line distributor matching tributary coordinates. `PASS`.
- **Condition (c) Naive / Wrong:** Lumps barrier loads uniformly across lines or shifts barrier centroids to center, violating per-barrier centroid and tributary line share assertions. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect:** Wind calculation arguments fall back to module defaults (speed $33.0\text{ m/s}$ vs $47.0\text{ m/s}$, height $10.0\text{ m}$ vs $15.0\text{ m}$, barrier $0.0\text{ m}$ vs $1.1\text{ m}$, railing $0.0\text{ m}$ vs $1.2\text{ m}$), yielding $P_z = 463.7\text{ N/m}^2$ instead of authentic $1039.6\text{ N/m}^2$.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Full propagation of wind parameters to IRC 6 Table 12 calculator. `PASS` ($P_z = 1039.6\text{ N/m}^2$).
- **Condition (c) Naive / Wrong:** Propagates wind speed only, leaving height and barrier at defaults. `BASELINE_FAIL` ($P_z = 940.6\text{ N/m}^2$).
- **Sensitivity Status:** **VERIFIED**.

### 7. TC-REG-D02-TEMPERATURE-PROPAGATION
- **Defect:** `analyser.py:add_temperature_load` looks for nonexistent dictionary key `'temperature_load_kN_m2'`, leaving thermal analysis unexecuted.
- **Status:** **BLOCKED** under **DEC-015** (IRC 6 Cl. 215 thermal modeling undecided in specifications).
- **Sensitivity Status:** `BLOCKED / NOT DEMONSTRATED`.

### 8. TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Defect:** IRC 6 Cl. 204.6 fatigue vehicle moving load analysis pipeline is completely absent from `analyser.py`.
- **Status:** **BLOCKED** under **DEC-018** (fatigue vehicle pipeline integration undecided).
- **Sensitivity Status:** `BLOCKED / NOT DEMONSTRATED`.

### 9. TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect:** `executive_summary.py` hardcodes `\noindent Girder design pass` in the executive summary narrative regardless of component failures.
- **Phase 2.6 Refinements:**
  - Parameterized loop over all girders G1 through G6 independently.
  - DCR-only failure scenario (`status == "PASS"`, `dcr = 1.30`).
  - Auxiliary component failure scenarios: Cross Bracing (`CB`), End Diaphragm (`ED`), Deck Slab (`Deck`).
  - Multiple simultaneous failure scenario.
  - All-pass mirror scenario.
  - Tabular `Overall Design Status` asserted against Key Outcomes narrative in all scenarios.
  - Synchronized injected fixture state.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Dynamically evaluates all girders, auxiliary components, and DCR thresholds. `PASS`.
- **Condition (c) Naive / Wrong:** Checks only G1 and G3, failing when G2, G4, G5, or G6 fails. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 10. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect:** `plategirderbridge.py` hardcodes `num_girders = 4` in grillage generation even when user configures 6 girders.
- **Condition (a) Baseline:** `BASELINE_FAIL` (4 girders generated vs 6 configured).
- **Condition (b) Minimal Correct:** Generates grillage with user-configured 6 girders. `PASS`.
- **Condition (c) Naive / Wrong:** Generates 4 girders. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 11. TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Defect:** Transverse grillage members assigned half the steel girder section properties (`girder/2`, $I_z \approx 0.00367\text{ m}^4$) instead of transformed concrete deck slab properties.
- **Status:** **BLOCKED** under **DEC-013** (transverse concrete slab representation undecided in specifications).
- **Sensitivity Status:** `BLOCKED / NOT DEMONSTRATED`.

### 12. TC-REG-CAP-STIFFENER-BUCKLING
- **Defect:** Intermediate transverse stiffener design uses erroneous capacity formulations (tension field action without web buckling checks, yielding over-optimistic DCR).
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Evaluates authentic IS 800 Cl. 8.7 stiffener buckling capacity. `PASS`.
- **Condition (c) Naive / Wrong:** Uses uncorrected baseline formulation. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 13. TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect:** `analyser.py` hardcodes steel density as $78.5\text{ kN/m}^3$, ignoring user input density (e.g., $70.0\text{ kN/m}^3$), yielding $169.82\text{ kN}$ dead load instead of $151.43\text{ kN}$.
- **Phase 2.6 Refinement:** Retrieves span directly via production key `geometry.span`.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Uses input `material.girder.density` for dead load derivation. `PASS`.
- **Condition (c) Naive / Wrong:** Hardcodes $78.5\text{ kN/m}^3$. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 14. TC-REG-FS-CLEAN-WORKING-TREE
- **Defect:** Hardcoded relative paths in `ui_fields_project_location.DB_PATH` create `weather.sqlite` inside the package tree in clean installations, and default `Database()` constructor creates unanchored `weather.sqlite` in `os.getcwd()`. Fails in read-only environments.
- **Phase 2.6 Refinements:**
  - Sandboxed execution in temporary package copy, protecting `source/OsdagBridge`.
  - Recursive tree hashing with detector self-test on `shapefiles/` probe file.
  - Real OS write denial applied without elevation (`icacls /deny Everyone:(OI)(CI)W` or `chmod 0555`).
  - Asserts query results: `>= 30` states returned, valid weather dictionary (`max_temp`, `latitude`).
  - Removed redundant alias checks.
- **Condition (a) Baseline:** `BASELINE_FAIL`.
- **Condition (b) Minimal Correct:** Anchors database operations to user data directories, succeeding in read-only package copies. `PASS`.
- **Condition (c) Naive / Wrong:** Leaves default constructor unanchored, creating files in `os.getcwd()`. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

### 15. TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Purpose:** Verifies offscreen 3D CAD rendering and image export integrity without requiring desktop GUI invocation.
- **Condition (a) Baseline:** `PASS` (renders offscreen CAD geometry and exports valid image).
- **Condition (b) Minimal Correct:** Produces valid CAD export image. `PASS`.
- **Condition (c) Naive / Wrong:** Generates corrupted / blank image. `BASELINE_FAIL`.
- **Sensitivity Status:** **VERIFIED**.

---

## 3. Summary of Manifest Artifact Hashes

All test logs, summaries, and runner scripts have been cryptographically verified against `testing/evidence/phase_2_6/hashes/manifest_hashes.json`:

| File Path | SHA-256 Hash | Size (Bytes) |
|:---|:---|:---:|
| `testing/test_cases/baseline_regression/run_all_baseline_tests.py` | `ef5a8151feead5a0b104bc8ec058a1f0c46e6147b2590df280f51f93a140dbf1` | 109,078 |
| `testing/test_cases/baseline_regression/run_sensitivity_matrix.py` | `d24db269e7079f0097d823c3e4693cff395c0e612266b219042d7ee997c3da04` | 48,898 |
| `testing/evidence/phase_2_6/baseline/phase_2_6_baseline_summary.json` | `e2bd04069919b3ef826c0a766938fdb4ca9544d1b332f02707223aee41aae441` | 12,732 |
| `testing/evidence/phase_2_6/sensitivity/phase_2_6_sensitivity_matrix_summary.json` | `fbaf7f119ec749da76146def6c69442ac927789c6e12883f315af429a9f80d6c` | 25,929 |
| `testing/evidence/phase_2_6/hashes/manifest_hashes.json` | `7f20225cb604186f37120c2ee0e0ecff2409f33ab06b46f103528d51c2ad9dc6` | 16,047 |
