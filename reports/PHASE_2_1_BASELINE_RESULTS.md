# Phase 2.1 — Baseline Regression Test Results Report

**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Reference Environment:** `osdagbridge-py312`  
**Python Executable:** `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` (Python 3.12.16)  
**Baseline Git Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch: `dev`, Working Tree: Pristine Clean)  
**Execution Timestamp:** 2026-11-16T15:39:11+05:30  
**Total Run Duration:** 10.73 s  
**Process Exit Code:** `1` (Recorded in `testing/evidence/phase_2_1/exit_code.txt`)  
**Controlling Audit:** `reports/PHASE_2_FINAL_INDEPENDENT_GATE_AUDIT.md`  

---

## 1. Executive Summary & Gating Determination

This report documents the official baseline execution of the repaired Phase 2.1 regression test suite (`testing\test_cases\baseline_regression\run_all_baseline_tests.py`) against the frozen, untouched baseline commit `d74f56d`.

In accordance with the core mandate of the Final Independent Gate Audit, **no attempt was made to manufacture artificial passing results on defective baseline code**. True defects must fail; unresolved models must be marked blocked.

### Key Results Summary:
- **Total Tests Executed:** 14
- **Manifest Alignment:** **14 / 14 Matches (100%)**
- **Passed (Clean Environment / Harness Verification):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
- **Failed (Confirmed Genuine Baseline Defects):** 12 (DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, DEF-08, DEF-10, DEF-11, DEF-12, DEF-13, DEF-17)
- **Blocked (Pending Architectural / Engineering Decisions):** 1 (`TC-REG-GEO-SLAB-SECTION-PROPERTIES` pending DEC-013)
- **Harness Exit Code:** `1` (Properly non-zero, signaling failing baseline defects)

---

## 2. Environment & Repository Provenance

| Component | Provenance / Value | Cryptographic / Version Identifier |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 Enterprise (Build 26300, 64-bit) | Intel Core i9-14900HX, RTX 5070 Mobile |
| **Python Runtime** | Miniconda isolated environment | Python 3.12.16 (CPython, 64-bit) |
| **Git Repository** | `source\OsdagBridge` | Commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`origin/dev`) |
| **Git Status** | Working tree completely pristine | `nothing to commit, working tree clean` |
| **OpenCASCADE Kernel** | `pythonocc-core 8.0.1.2` / `occt 8.0.1` | OpenGL 4.6 (Hardware offscreen FBO) |
| **Qt Framework** | `PySide6 6.11.3` | Qt 6.11 runtime libraries |
| **FEA Solver** | `openseespy 3.8.0.0` / `openseespywin 3.8.0.0` | OpenSees finite-element engine |
| **Grillage Engine** | `ospgrillage 0.1.0` (vendored editable) | OsdagBridge integration layer |
| **Input Fixture SHA-256** | `testing/fixtures/pinned_input_fixture.json` | `31ae62dc62908f515d911cff721a7384725d2b7c62d0aa5c80dfaaee9f093a38` |
| **Output Fixture SHA-256** | `testing/fixtures/pinned_output_fixture.json` | `429a3198083b4b88ff6cf00bb2ba687353f86e336e885d519b78e472ce866a9a` |

---

## 3. Comprehensive Baseline Test Results Matrix

| Test Identifier | Associated Defect | Expected Baseline | Observed Status | Manifest Match | Duration | Mechanical Failure Reason / Baseline Behavior |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | FAIL | **FAIL** | MATCH | 0.387 s | `ospgrillage` ignored load_factor 1.35; force ratio is 1.00000 (expected 1.35000). |
| `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | FAIL | **FAIL** | MATCH | 0.045 s | Grillage retains preliminary sizing across all 4 girders (Iz gap ~7.40%, A gap ~10.55%); Post-snapping dimensions inconsistent: D=1340.0mm != dw(1306.0) + 2*tf(36.0) = 1342.0mm. |
| `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | FAIL | **FAIL** | MATCH | 0.052 s | Static load case produces false cyclic stress ranges: Path (a) envelope = 125.46 MPa (doubled from +M and -M end signs); Path (b) per-LC = 62.73 MPa (treats static moment Mz as range). Expected 0.0 MPa. |
| `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | FAIL | **FAIL** | MATCH | 6.270 s | Solver ignored ULS factors: BASIC_1 analyzed shears match un-factored 1.0DL + 1.0DW (discrepancy vs factored = 72392.5 N; error vs unfactored = 1.16e-07 N); create_sidl_combination() was not called (sidl_combination is None). |
| `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | FAIL | **FAIL** | MATCH | 0.083 s | Wind arguments fell back to defaults (speed=33.0 vs 47.0, height=10.0 vs 15.0, barrier=0.0 vs 1.1, railing=0.0 vs 1.2), yielding Pz = 463.7 N/m2 instead of authentic 1039.6 N/m2. |
| `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | FAIL | **FAIL** | MATCH | 0.046 s | add_temperature_load() reads 'temperature_load_kN_m2' which no UI field or standard inputs populate; authentic temperature keys are ignored and load case is None. |
| `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | FAIL | **FAIL** | MATCH | 0.084 s | add_vehicle_load_cases_from_combinations() generated 2 cases (Class A and 70R only); IRC 6 Cl. 204.6 fatigue vehicle case (12t/14t/14t) is completely missing. |
| `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | FAIL | **FAIL** | MATCH | 0.091 s | executive_summary() emits literal '\noindent Girder design pass' unconditionally under Key Design Outcomes Summary despite a failing fatigue check (DCR = 1.9746). |
| `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | FAIL | **FAIL** | MATCH | 0.046 s | designer.py:401 sets n_girders = geom.n_l (6), incorrectly counting 2 slab overhang edge lines as structural girders for a 4-girder bridge. |
| `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | **BLOCKED** | MATCH | 0.002 s | DEC-013 Pending: Transverse deck slab representation is undecided in project documentation. Baseline assigns girder/2 (Iz=0.00367 m4), which is mechanically invalid for concrete deck, but exact transformed vs concrete material and cracked/torsion model requires engineering sign-off. |
| `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | FAIL | **FAIL** | MATCH | 0.047 s | capacity 134083.2 kN exceeds squash bound 1918.8 kN (69.9x); elastic stress 22233.9 MPa exceeds yield bound 318.2 MPa; capacity 134083.2 kN fails positive IS 800 oracle 63.4 kN. |
| `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | FAIL | **FAIL** | MATCH | 0.779 s | Self-weight resultant (169.8 kN) matches hardcoded 78.5 kN/m3 (169.8 kN) instead of user-specified density 70.0 kN/m3 (151.4 kN). |
| `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | FAIL | **FAIL** | MATCH | 1.956 s | Database() defaults to relative path in cwd; Production DB_PATH targets installed package directory (F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\core\data\project_location\weather.sqlite). |
| `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | **PASS** | MATCH | 0.693 s | Environment CAD verification: Native OCC offscreen Viewer3d.ExportToImage renders opaque 3D geometry (pixel std=20.0, 3 unique colors). |

---

## 4. Key Engineering Discoveries & Empirical Insights

1. **FE Solver Load Combination Mechanics (DEF-01 / DEF-02):**
   The OpenSees grillage solver executes load combinations by summing load patterns. In `analyser.py:create_uls_combinations()`, combinations are created by cloning un-factored load cases via `og.create_load_case()`, but the partial safety factors (1.35 for DL, 1.75 for DW) are dropped by `ospgrillage`. The solver output for `BASIC_1` matches un-factored linear superposition to within $1.16 \times 10^{-7}\text{ N}$, but leaves factored design shears short by $72,392.5\text{ N}$.

2. **OpenSees Internal Force Sign Conventions in Fatigue (DEF-07):**
   In OpenSees, internal beam forces at a shared node between element $k$ (end j) and element $k+1$ (end i) have opposite signs due to coordinate transformations. For a simply supported beam under uniform sagging moment, element $k$ end j reports $+M$, while element $k+1$ end i reports $-M$. The global envelope calculation `max(mz) - min(mz)` evaluates $(+M) - (-M) = 2M$, doubling static moment and causing a false fatigue failure ($DCR = 1.9746$).

3. **Web Strip Buckling Singularity (DEF-12):**
   The baseline formula in `IRC22CapacityCalculator.compute_bearing_stiffener` calculates web bearing capacity without checking slenderness reduction. For an $8\text{ mm}$ web, $KL/r \approx 395.25$. While IS 800:2007 Cl. 8.7.3.1 limits the buckling resistance to $63.40\text{ kN}$, the baseline formula computed $134,083.2\text{ kN}$ ($70\times$ the material squash yield limit of $1918.8\text{ kN}$).

4. **Transverse Deck Slab Representation (DEF-14 / DEC-013):**
   Baseline code assigns half the longitudinal steel plate girder stiffness ($I_z = 0.00367\text{ m}^4$) to transverse members representing the concrete deck. A unit concrete deck strip has gross $I_z = 0.001302\text{ m}^4/\text{m}$, and transformed steel equivalent $I_z = 2.148 \times 10^{-4}\text{ m}^4/\text{m}$. Because the grillage transverse representation requires project engineering sign-off on modular ratio and torsion reduction, this test is properly held as **BLOCKED** pending DEC-013.

---

## 5. Artifacts & Evidence Archival

All execution evidence has been preserved in `testing/evidence/phase_2_1/`:
- `runner.log`: Full stdout/stderr capture of test execution.
- `phase_2_1_summary.json`: Machine-readable results with timestamps, commit hash, and manifest alignment.
- `exit_code.txt`: Value `1`.
- `sensitivity/`: 14 detailed JSON files and `sensitivity_matrix_summary.json` proving sensitivity under (a), (b), and (c).

---

## 6. Recommendation & Gate Status

With 14/14 manifest matches, 12 confirmed reproducible defects, 1 blocked pending architectural sign-off, 1 passing environment check, and 14/14 sensitivity verification, the test harness is completely trustworthy.

**Verdict: READY FOR FINAL INDEPENDENT GATE AUDIT**
