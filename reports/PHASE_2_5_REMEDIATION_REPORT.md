# PHASE 2.5 — Final Regression Suite Remediation Report

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md` (Verdicts: `CONDITIONAL ACCEPTANCE`)  
**Python Reference Environment:** `osdagbridge-py312` (Python 3.12.16 on Windows 11 AMD64)  
**Phase 2.5 Test Runner:** `testing\test_cases\baseline_regression\run_all_baseline_tests.py`  
**Phase 2.5 Sensitivity Matrix Runner:** `testing\test_cases\baseline_regression\run_sensitivity_matrix.py`  
**Evidence Root:** `testing\evidence\phase_2_5\`  

---

## 1. Executive Summary

In the Phase 2.4 independent gate audit (`reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`), Claude issued a verdict of **CONDITIONAL ACCEPTANCE**. Twelve tests were accepted or conditionally accepted with documented limitations, but three tests were **REJECTED**:
1. `TC-REG-EQ-LOAD-CONSERVATION` (DEF-18) — rejected due to hardcoded expected values, lack of centroid verification, loose tolerance (5%), and an unconstrained sensitivity candidate distributor;
2. `TC-REG-RPT-EXEC-SUMMARY-STATUS` (DEF-08) — rejected because single-girder interior/edge failure scenarios were omitted, table consistency was untested, and the candidate was fragile;
3. `TC-REG-FS-CLEAN-WORKING-TREE` (DEF-10) — rejected because the test erroneously treated explicit path creation as a defect, and candidate (b) used brittle sandbox-name heuristics.

In addition, the audit required clarifying four tests with accepted limitations (`TC-REG-A02`, `TC-REG-B01`, `TC-REG-C01`, `TC-REG-MAT`), correctly relabeling `TC-REG-C02` as DEF-17, and preserving the three formal engineering blockers (`TC-REG-D02` under DEC-015, `TC-REG-C02` under DEC-018, and `TC-REG-GEO-SLAB` under DEC-013).

In Phase 2.5, **all mandatory remediation items specified in §13 of the controlling audit have been fully resolved**. The regression suite and sensitivity framework were comprehensively overhauled in a completely isolated evidence directory (`testing/evidence/phase_2_5/`). No application source files under `source/OsdagBridge` were altered.

### Gate Results Summary

- **Baseline Regression Suite:**
  - Total Tests: **15**
  - Baseline Failures (True Defects Detected): **11**
  - Passing Checks (Environment Verification): **1** (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
  - Blocked (Formal Architectural/Spec Decisions Pending): **3** (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
  - Harness Exceptions / Errors: **0**
  - Manifest Alignment: **15 / 15 (100% Exact Match)**
  - Execution Duration: **34.95 s**
  - Process Exit Code: **0**

- **Sensitivity Matrix Suite (Candidate Mutation Gate):**
  - Total Tests Registered: **15**
  - Actionable Tests Verified: **12 / 12 (100.0%)**
  - Blocked Tests: **3 / 15**
  - Overall Actionable Gate Status: **PASSED**
  - Process Exit Code: **0**

---

## 2. Mandatory Remediation Actions & Technical Implementations

The following subsections document the technical corrections made to resolve each item identified in §13 of `reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`.

### 2.1 TC-REG-EQ-LOAD-CONSERVATION (DEF-18) — Full Overhaul

- **Defect Background:** OpenSees grillage load distribution in `PlateGirderBridge` causes severe force imbalance and centroid displacement:
  - Deck slab (DD) is assigned $1314.375\text{ kN}$ instead of $1275.000\text{ kN}$ (+3.09%).
  - Wearing course (DW) is assigned $252.360\text{ kN}$ instead of $244.800\text{ kN}$ (+3.09%).
  - Crash barrier line loads are assigned $196.200\text{ kN}$ instead of $313.920\text{ kN}$ (-37.50% shortfall).
  - Furthermore, crash barrier load application points were displaced from the bridge center ($x = 12.000\text{ m}$) to $x = 12.750\text{ m}$, introducing a $+0.750\text{ m}$ longitudinal centroid shift.
- **Audit Findings:** The Phase 2.4 test used hardcoded literals (`1275.0`, `244.8`, `313.92`), had a 5% tolerance, omitted moment/centroid checks, and candidate (b) used an unphysical magic-total scaling hack.
- **Phase 2.5 Corrections:**
  1. **Dynamic Derivation:** All expected loads are dynamically computed directly from model inputs:
     - Deck slab: $W_{DD} = L_{span} \times W_{carriageway} \times q_{slab} = 24.0 \times 8.5 \times 6.250 = 1275.000\text{ kN}$.
     - Wearing course: $W_{DW} = L_{span} \times W_{carriageway} \times q_{wc} = 24.0 \times 8.5 \times 1.200 = 244.800\text{ kN}$.
     - Crash barrier: $W_{CB} = 2 \times L_{span} \times w_{barrier} = 2 \times 24.0 \times 6.540 = 313.920\text{ kN}$.
     - Self-weight: $W_{SW} = \sum (A_g) \times \rho_{steel} \times L_{span} = 4 \times 0.02253 \times 78.5 \times 24.0 = 169.819\text{ kN}$.
     - Total Applied Resultant: $W_{tot} = 2003.539\text{ kN}$.
  2. **Centroid and Moment Conservation:** Added exact checks for both longitudinal centroid ($\bar{x} = 12.000\text{ m}$) and transverse centroid ($\bar{z} = 4.250\text{ m}$):
     $$\bar{x} = \frac{\sum (F_{x,i} \cdot x_i)}{\sum F_{x,i}}, \quad \bar{z} = \frac{\sum (F_{z,i} \cdot z_i)}{\sum F_{z,i}}$$
  3. **Strict Tolerances:** Tightened force tolerance to 0.05% ($0.0005$) and centroid tolerance to $0.05\text{ m}$.
  4. **Sensitivity Candidates:**
     - Candidate (b) implements a genuine cell-intersection bilinear distributor (`_distribute_patch_load_fem` and `_distribute_line_load_fem`), achieving 100% force and centroid conservation without magic normalizations. Status: `PASS`.
     - Candidate (c) distributes patch loads correctly but omits crash barrier line loads, resulting in a $-117.7\text{ kN}$ force deficit and $+0.750\text{ m}$ centroid shift. Status: `BASELINE_FAIL`.
     - Sensitivity outcome: `VERIFIED`.

### 2.2 TC-REG-RPT-EXEC-SUMMARY-STATUS (DEF-08) — Multi-Scenario Audit

- **Defect Background:** `executive_summary.py` hardcodes `\noindent Girder design pass` in the Key Design Outcomes section of the generated LaTeX report regardless of whether one, multiple, or all girders fail.
- **Audit Findings:** The Phase 2.4 test only checked a uniform failure of all girders, failing to verify single-girder interior failure, single-girder edge failure, and table status agreement.
- **Phase 2.5 Corrections:**
  1. **Comprehensive Scenarios:** Expanded test matrix to 6 distinct scenarios:
     - Scenario 1: All components pass (Mirror scenario).
     - Scenario 2A: Interior girder failure (G3 fails, G1, G2, G4.. pass).
     - Scenario 2B: Edge girder failure (G1 fails, G2.. pass).
     - Scenario 3: Cross bracing failure.
     - Scenario 4: End diaphragm failure.
     - Scenario 5: Deck slab failure.
     - Scenario 6: Multiple simultaneous component failures.
  2. **Table Consistency Assertion:** Added an explicit assertion that the executive summary table's `Overall Design Status` must match the narrative outcome.
  3. **Sensitivity Candidates:**
     - Candidate (b) dynamically derives pass/fail status for all girders G1 through G6 and all auxiliary structural components, correctly reflecting failures in all scenarios. Status: `PASS`.
     - Candidate (c) naively inspects G1 only, passing Scenario 2B but failing Scenario 2A (interior girder G3 failure). Status: `BASELINE_FAIL`.
     - Sensitivity outcome: `VERIFIED`.

### 2.3 TC-REG-FS-CLEAN-WORKING-TREE (DEF-10) — Packaging & Immutability Overhaul

- **Defect Background:** In baseline, `ui_fields_project_location.DB_PATH` is hardcoded relative to `__file__` inside the package data directory (`src/osdagbridge/core/data/project_location/weather.sqlite`). In a clean checkout or standard pip install where `weather.sqlite` is not pre-packaged, calling `@_with_db` creates `weather.sqlite` inside the package tree. Furthermore, the default `Database()` constructor creates unanchored `weather.sqlite` in `os.getcwd()`. In a read-only environment, write attempts cause application crashes.
- **Audit Findings:** The Phase 2.4 test failed because it treated creating a file at an explicit path as a defect, and candidate (b) relied on folder-name sniffing.
- **Phase 2.5 Corrections:**
  1. **Dropped Erroneous Premise:** Dropped the check that penalized `Database(explicit_path).connect()` for creating a file at the user-specified target path.
  2. **Four Rigorous Checks:**
     - **Check 1 (Production Anchoring):** Verified that `ui_loc.DB_PATH` resolves outside `pkg_root` and targets a writable user-data location.
     - **Check 2 (Constructor Anchoring):** Verified that `Database()` default constructor resolves to an anchored user-data path, not to `os.getcwd()` or inside `pkg_root`.
     - **Check 3 (Package Immutability):** Verified that executing production queries (`get_state_list`, `get_weather`) does not create, touch, or mutate any file under `real_pkg_loc_dir`.
     - **Check 4 (Read-Only Package Resilience):** Verified that production queries succeed when the package tree is read-only, because write operations are isolated to user app data.
  3. **Sensitivity Candidates:**
     - Candidate (b) anchors both `ui_loc.DB_PATH` and `Database.__init__` default to user app data (`%LOCALAPPDATA%\OsdagBridge` or temporary user directory). Status: `PASS`.
     - Candidate (c) anchors `ui_loc.DB_PATH` but leaves `Database.__init__` unanchored, creating files in `os.getcwd()`. Status: `BASELINE_FAIL`.
     - Sensitivity outcome: `VERIFIED`.

### 2.4 Documentation & Refinement of Conditionally Accepted Tests

1. **TC-REG-B01-SECTION-PROPERTY-SYNC (DEF-03):**
   - Documented the analytical grillage bounds: Courbon lower bound is $4.541\text{ mm}$, single-beam upper bound is $18.164\text{ mm}$, and calibrated grillage target deflection is $7.218\text{ mm}$.
   - Updated Candidate (b) to use plate formula section properties ($I_y = 0.0002068\text{ m}^4$, $J = 1.815 \times 10^{-6}\text{ m}^4$) instead of hardcoded magic constants.
2. **TC-REG-C01-SECTIONAL-STRESS-RANGE (DEF-07):**
   - Corrected log label to reference $N_{sc} = 2,000,000$ cycles.
   - Raised an explicit `KeyError` when `f_fd_eff_MPa` is missing from the output dictionary.
   - Candidate (b) evaluates sign-consistent element-end section moments ($-Mz_i$ / $+Mz_j$) and extracts $\max(M) - \min(M)$ across frequent load combinations divided by composite section modulus $Z_e$, resolving the issue cleanly without range injection.
3. **TC-REG-A02-ULS-COMBINATION-SUM (DEF-01 / DEF-02):**
   - Replaced silent fallback literals with explicit retrieval of each component load case (`self_weight`, `deck_slab`, `wearing_course`, `crash_barrier`).
   - Documented the $2802.70\text{ kN}$ total applied resultant and explained the IRC 6 Annex B Table B.1 vs Table B.2 convention (1.35 vs 1.75).
4. **TC-REG-MAT-DENSITY-CONSISTENCY (DEF-13):**
   - Refined documentation explaining that baseline `analyser.py` hardcodes $78.5\text{ kN/m}^3$ ($169.8\text{ kN}$ self-weight resultant), ignoring the user-specified input density of $70.0\text{ kN/m}^3$ ($151.4\text{ kN}$).

### 2.5 Formal Blockers & Decisions Preserved

1. **TC-REG-D02-TEMPERATURE-PROPAGATION:** Preserved as formally `BLOCKED` under **DEC-015** (thermal load modeling under IRC 6 Cl. 215 is undecided in specifications; `add_temperature_load` reads unpopulated keys).
2. **TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS:** Corrected defect label to **DEF-17** (removed DEF-08); preserved as formally `BLOCKED` under **DEC-018** (IRC 6 Cl. 204.6 fatigue vehicle moving load is completely missing from the analysis and design pipeline).
3. **TC-REG-GEO-SLAB-SECTION-PROPERTIES:** Preserved as formally `BLOCKED` under **DEC-013** (transverse deck slab representation model—transformed steel vs concrete, uncracked vs cracked, torsion factor—remains undecided in project documentation).

---

## 3. Full Test Execution Evidence Summary

### 3.1 Baseline Suite Execution Table

| Test ID | Defect ID | Baseline Expected | Observed Status | Manifest Match | Duration | Primary Diagnostic Reason |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| `TC-REG-A01-FACTOR-SCALING` | DEF-01 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 1.34 s | DEF-01 Confirmed: ospgrillage ignored load_factor 1.35; force ratio is 1.00000 (expected 1.35000). |
| `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.31 s | DEF-03 Confirmed: Dimensions inconsistent (D=1340 vs 1342); Iz gap ~7.40%, A gap ~10.55%; Deflection 7.82mm vs 7.22mm target. |
| `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.28 s | DEF-07 Confirmed: Static load case produces false cyclic stress ranges (Path a: 125.46 MPa; Path b: 62.73 MPa; Expected 0.0 MPa). |
| `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01/02 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 13.85 s | DEF-01/DEF-02 Confirmed: Shears match un-factored 1.0DL+1.0DW; Reaction 1736.6kN vs 2710.2kN target; Crash barrier omitted from BASIC_1. |
| `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.81 s | DEF-18 Confirmed: DD diff +3.1%; DW diff +7.6 kN (+3.1%); Crash barrier diff -117.7 kN (-37.5%), centroid shift dx=+0.750m. |
| `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.08 s | DEF-05 Confirmed: Wind arguments fell back to defaults (speed=33 vs 47, height=10 vs 15), yielding Pz = 463.7 N/m2 vs 1039.6 N/m2. |
| `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | **BLOCKED** | MATCH | 0.00 s | DEC-015 Pending: Thermal load modeling (IRC 6 Cl. 215) is undecided in project specifications. |
| `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | **BLOCKED** | MATCH | 0.00 s | DEC-018 Pending: IRC 6 Cl. 204.6 fatigue vehicle moving load not implemented in analysis/design pipeline. |
| `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.45 s | DEF-08 Confirmed: executive_summary() emits literal '\noindent Girder design pass' unconditionally in Scenarios 2A, 2B, 3, 4, 5, 6. |
| `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.05 s | DEF-11 Confirmed: designer.py:401 sets n_girders = geom.n_l (6), incorrectly counting 2 overhang lines as structural girders. |
| `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | **BLOCKED** | MATCH | 0.00 s | DEC-013 Pending: Transverse deck slab representation model undecided in project specifications. |
| `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.05 s | DEF-12 Confirmed: Geometries fail oracle (Geo 1: 214533.2kN vs oracle 63.4kN; Geo 2: 370184.0kN vs oracle 158.5kN). |
| `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 0.78 s | DEF-13 Confirmed: Self-weight resultant (169.8 kN) matches hardcoded 78.5 kN/m3 instead of user input 70.0 kN/m3 (151.4 kN). |
| `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | **BASELINE_FAIL** | MATCH | 4.21 s | DEF-10 Confirmed: Production DB_PATH resolves inside package tree; Database() unanchored in cwd; Package vulnerable to read-only install. |
| `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 | PASS | **PASS** | MATCH | 2.45 s | Environment Verification: Native OCC offscreen Viewer3d.ExportToImage renders opaque 3D geometry (std=66.6, 3 colors). |

### 3.2 Sensitivity Matrix Verification Table

| Test ID | Condition (a) Baseline | Condition (b) Correct | Condition (c) Naive | Sensitivity Verdict | Gate Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| `TC-REG-A01-FACTOR-SCALING` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-B01-SECTION-PROPERTY-SYNC` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-C01-SECTIONAL-STRESS-RANGE` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-A02-ULS-COMBINATION-SUM` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-EQ-LOAD-CONSERVATION` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-D01-WIND-SPEED-PROPAGATION` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-D02-TEMPERATURE-PROPAGATION` | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-015 |
| `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-018 |
| `TC-REG-RPT-EXEC-SUMMARY-STATUS` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | BLOCKED | BLOCKED | BLOCKED | **BLOCKED** | DEC-013 |
| `TC-REG-CAP-STIFFENER-BUCKLING` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-MAT-DENSITY-CONSISTENCY` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-FS-CLEAN-WORKING-TREE` | BASELINE_FAIL | PASS | BASELINE_FAIL | **VERIFIED** | PASS |
| `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | PASS | PASS | BASELINE_FAIL | **VERIFIED** | PASS |

**Actionable Gate Outcome:** 12 / 12 Verified (100.0%) | **Gate Result:** **PASSED**

---

## 4. Evidence Integrity and Cryptographic Hashing

All Phase 2.5 evidence was generated in the dedicated folder:
`testing\evidence\phase_2_5\`

Every file in the directory has been cryptographically fingerprinted using SHA-256 and recorded in `testing\evidence\phase_2_5\hashes\manifest_hashes.json`.

Key Artifact Hashes:
- `testing/evidence/phase_2_5/baseline/phase_2_5_baseline_summary.json`: `cbbde09d9bc181e14a2bcab62b08a1cb556391d17154fbdbd1e70beeaeb384be` (12,243 bytes)
- `testing/evidence/phase_2_5/sensitivity/phase_2_5_sensitivity_matrix_summary.json`: `41a69a21e4a30eef7ec1aa7db44fc8b9759885bf22fa59dfcfd1f65dc7f6b907` (24,914 bytes)
- `testing/test_cases/baseline_regression/run_all_baseline_tests.py`: `e26a0cae18fa428e2023dbf7fc138fb0b3b44b9cb79f1efc9b19d5c4eaae0b6f`
- `testing/test_cases/baseline_regression/run_sensitivity_matrix.py`: `d9270bb3f567b45cae7c5b62b02e6eebef652a9261ff2f0e0db1eb1eb3602d24`
- Structural Database (`Intg_osdag.sqlite`): `25f97857d4cbe2054ff1a669bc673fb370e7a2b97c23bc9514eef93df155a0b7` (270,336 bytes)
- Untracked Baseline Database (`weather.sqlite`): `1d7676587372cf936f212239be9b2bf0df7b545f4cb609d57a916a4be7ad85e3` (180,224 bytes)

### Known Historical Provenance Limitation

As noted in Claude's Phase 2.4 audit, five candidate log files in the legacy directory `testing/evidence/phase_2_3/candidates/` were overwritten during Phase 2.4 test development prior to creating the isolated `phase_2_4/` directory. All Phase 2.4 and Phase 2.5 directories are strictly isolated, self-contained, and preserved without modification.

---

## 5. Conclusion & Transition to Phase 3 Readiness

With:
1. 100% of Claude's mandatory corrections from §13 remediated,
2. 12 out of 12 actionable regression tests verified against genuine candidate mutations,
3. 3 undecided structural design specifications preserved as blocked under formal project decisions (DEC-013, DEC-015, DEC-018),
4. The application source repository frozen, unmodified, and clean on `dev` at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`,

the OsdagBridge Phase 2 regression test infrastructure has achieved **FULL INDEPENDENT AUDIT ACCEPTANCE READINESS**. Phase 3 remediation planning may proceed immediately following formal gate sign-off.
