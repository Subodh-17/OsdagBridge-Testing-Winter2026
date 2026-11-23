# PHASE 2.4 — Test Sensitivity & Validation Matrix

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `source/OsdagBridge` (`dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Controlling Audit:** `reports/PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Execution Timestamp:** 2026-11-16T15:36:54 UTC  
**Total Matrix Runtime:** 136.88 seconds  
**Reference Environment:** `osdagbridge-py312` (Python 3.12.16, OpenCASCADE 8.0.1, OpenSeesPy 3.8.0.0, NumPy 2.5.5, SciPy 1.18.1, xarray 2026.9.0)  

---

## 1. Matrix Overview & Validation Principles

In strict accordance with §11 of the Phase 2.2 Independent Gate Audit and §9 of the Phase 2.3 Independent Gate Audit, every regression test must satisfy the 3-condition sensitivity validation protocol to prove that the test genuinely detects defects and validates resolution:
- **Condition (a) [Frozen Baseline]:** Application behavior under pristine repository commit `d74f56d` must produce the expected baseline status (`BASELINE_FAIL`, `BLOCKED`, or `PASS` for CAD).
- **Condition (b) [Minimal Correct Candidate]:** A genuine, minimal implementation altering production execution or solver state must produce `PASS`. No constant-return overrides or mock objects without solver participation.
- **Condition (c) [Plausible Incorrect Candidate]:** A flawed, naive, or partial candidate implementation must be caught by the test, producing `BASELINE_FAIL` or `FAIL`.
- **Formally Blocked Tests:** Tests where specifications or architectural decisions are undecided (**DEC-013**, **DEC-015**, **DEC-018**) are marked `BLOCKED` across all conditions, with status `BLOCKED / NOT DEMONSTRATED`. No artificial passing candidates are manufactured.

---

## 2. Master Test Validation Matrix

| Index | Test Identifier | Defect ID | Condition (a) [Baseline] | Condition (b) [Correct] | Condition (c) [Plausible Naive] | Sensitivity Verdict | Candidate (b) Source SHA-256 | Candidate (c) Source SHA-256 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `8aea6bd94b289a469c3d989a9d9fae374335228b3e5ef064b390941c05dac0f1` | `4747fc79c5045bd7072ff1c7c11cae54830368b63778b7a9d1b3b76171a18fc8` |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `afbd3a38ffa14d64155ced209df4bee92a48021a4eb588c2dc2d48787a9016e1` | `b9991206f368ad41d6b0577fc20c4a4505316ff1a0c4f82875a61dbadabeb858` |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `fffeae704f0d6ce8e3760ea4db247d48348633bf54b98fae8705e4f4fb02f542` | `b13c7bb61c8a6703554030635e98f0e57209930f78c89da442f9b2fa68fba9a3` |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01/02 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `d48c8df6e685f6ce5fa8bf7d2d3858c89ce47101683be81f9ca086e42b6a78ea` | `ff6caea7a1e05d045c704f05252ae07b22591ae9f893fa9e4ea235bf328905e4` |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `04d7d0dd6d86ebcb13ce474f85e5cf64d39ee73507d9fcaee7fa70222a075253` | `e2a05cf4cb09919b489ef0c30a597a7da9318b76c8c4bc6ec2cf4fdb07a98ca9` |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `ea165f12aa52d585b7468134710a30b2003c2069c99173c38bdae9c9f75ec54c` | `c97db3c28df7a88eb22c7a6e138a2e58286ca0792a5438885b59744c803ffc0d` |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION`| DEF-06 | `BLOCKED` | `BLOCKED` | `BLOCKED` | **BLOCKED** | *None (DEC-015 Pending)* | *None (DEC-015 Pending)* |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS`| DEF-17 | `BLOCKED` | `BLOCKED` | `BLOCKED` | **BLOCKED** | *None (DEC-018 Pending)* | *None (DEC-018 Pending)* |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `c21e64906bbbf80f682d3ea9549326e9594f87243cbeceb0255c464aa6bfd5ea` | `f280e227fc6e053fedd0da7e3160a3734e5a9539fa344e2ee04c004c0ff95a32` |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `4f4b1626c927f87961298816c27867fa780d6f466b70a793fc0c5f2ec39f506e` | `ca614a9235d9df967a33bc21d603e91129994c5e31f0cfb3f9ff7bdf7f938aa8` |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES`| DEF-14 | `BLOCKED` | `BLOCKED` | `BLOCKED` | **BLOCKED** | *None (DEC-013 Pending)* | *None (DEC-013 Pending)* |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `c830dd5713ddda6b37ba4ef577b21dc98276f7535b91a78c187be06ee69cb0eb` | `e7a17726e6328639e44bc6055d7fc7cf78a705193630fba1eecfa34341aa91e3` |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `f0dd9ea24d26fdf24368dd9ea3114d591fe50d4f13459c735d46002f1a30263d` | `bfa1ba2aa6fa3869b2d861d8bc5db2ef25bfbc94477db1f94532a8435d045d0b` |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `132e4d9ebca89ca39d671b56360c7b2c58976b9ee27b031cbaec11c2a1c2269a` | `9b369c0d75c8793b82736e4f32dc8fa97ee89dc1d84ea235542fca1215bb5fe7` |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 | `PASS` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `d03da24a13bf73cb11b157488f7871b2d354a93322d716d123e4ebdfa05fa147` | `1e95cfc91ec671d02cf12c3f8f12db01484ca8f5f643e990390f1d5e3be0a4f5` |

---

## 3. Detailed Technical Analysis of Candidate Behaviors

### 1. TC-REG-A01-FACTOR-SCALING (DEF-01)
- **Candidate (b):** Deepcopies and scales load magnitudes by `load_factor` in `LoadCase.add_load`. Scales `line_end_point.p` in `LineLoading.apply_load_factor` and invokes `_define_patch_edge_lines()` in `PatchLoading.apply_load_factor`. Linear grillage forces scale by exactly $1.35000\times$ (`PASS`, $1.225\text{ s}$).
- **Candidate (c):** Naively applies partial $1.15\times$ scaling regardless of specified `load_factor`. Force ratio is $1.09174 \ne 1.35000$, failing the assertion (`BASELINE_FAIL`, $1.217\text{ s}$).

### 2. TC-REG-B01-SECTION-PROPERTY-SYNC (DEF-03)
- **Candidate (b):** Synchronizes `PlateGirderBridge._girder_section` with snapped cross-section geometry ($I_z = 0.00792758\text{ m}^4$, $A = 0.025192\text{ m}^2$) and aligns web depth in `input_dict`. OpenSees midspan deflection under $100\text{ kN}$ drops from $7.816\text{ mm}$ to $7.218\text{ mm}$, matching calibrated grillage oracle within $0.01\%$ (`PASS`, $0.301\text{ s}$).
- **Candidate (c):** Updates `bgm.girder_props` metadata post-setup only, leaving solver OpenSees elements preliminary ($I_z = 0.0073409\text{ m}^4$, deflection $7.816\text{ mm}$). Fails deflection probe (`BASELINE_FAIL`, $0.302\text{ s}$).

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE (DEF-07)
- **Candidate (b):** Evaluates true cyclic stress ranges across load cases in `_extract_demands_from_analysis_results`. Single loadcase yields $0.0\text{ MPa}$; cyclic cases yield $62.729\text{ MPa}$ on both envelope and per-LC paths. Derived DCR matches $62.729 / 92.491 = 0.6782$ (`PASS`, $1.611\text{ s}$).
- **Candidate (c):** Zeroes static envelope, but leaves per-LC broken (evaluating static moment $M_z$ as range $= 62.73\text{ MPa}$), failing per-LC check (`BASELINE_FAIL`, $1.597\text{ s}$).

### 4. TC-REG-A02-ULS-COMBINATION-SUM (DEF-01 / DEF-02)
- **Candidate (b):** Factors `LineLoading` and `PatchLoading`, invokes `create_sidl_combination()` before `create_dead_load_combination()` in `add_dead_loads()`. Reaction matches factored superposition target $2710.17\text{ kN}$ within $0.001\%$, barrier differential $\Delta R_{\text{barrier}} = 264.87\text{ kN}$ matches $1.35 \times 196.20\text{ kN}$, and internal shears/moments scale exactly (`PASS`, $25.337\text{ s}$).
- **Candidate (c):** Factors SW and DW, but omits crash barrier from BASIC_1. Reaction is $1736.55\text{ kN}$ (shortfall $973.6\text{ kN}$) and barrier check fails (`BASELINE_FAIL`, $21.574\text{ s}$).

### 5. TC-REG-EQ-LOAD-CONSERVATION (DEF-18)
- **Candidate (b):** Patches `_distribute_load_types_to_model` to scale distributed OpenSees load commands for DD ($1275.0\text{ kN}$), DW ($244.8\text{ kN}$), and Crash Barrier ($313.92\text{ kN}$), achieving $100\%$ static equilibrium across all 4 dead load cases within $0.5\%$ (`PASS`, $4.593\text{ s}$).
- **Candidate (c):** Scales patch loads only (DD, DW), leaving crash barrier shortfall (reaction $196.20\text{ kN}$ vs applied $313.92\text{ kN}$, a $-37.5\%$ error), failing static equilibrium (`BASELINE_FAIL`, $4.629\text{ s}$).

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION (DEF-05)
- **Candidate (b):** Propagates user wind speed ($47.0\text{ m/s}$), exposed height ($15.0\text{ m}$), crash barrier height ($1.1\text{ m}$), and railing height ($1.2\text{ m}$) from `input_dict`. Produces authentic pressure $P_z = 1039.6\text{ N/m}^2$ and lateral thrust $F_T = 62.38\text{ kN}$ (`PASS`, $0.297\text{ s}$).
- **Candidate (c):** Reads wind speed only, leaving height and barrier heights at defaults, producing incorrect $P_z = 944.3\text{ N/m}^2 \ne 1039.6\text{ N/m}^2$ (`BASELINE_FAIL`, $0.295\text{ s}$).

### 7. TC-REG-RPT-EXEC-SUMMARY-STATUS (DEF-08)
- **Candidate (b):** Dynamically evaluates component statuses across all non-EB girders in `per_girder` and all 3 substructure components. Correctly identifies All Pass in Scenario 1 and flags specific failures in Scenarios 2–6 (`PASS`, $0.022\text{ s}$).
- **Candidate (c):** Hardcodes "Girder design fail", failing Scenario 1 (`BASELINE_FAIL`, $0.016\text{ s}$).

### 8. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT (DEF-11)
- **Candidate (b):** Sets `bcfg.geometry.n_girders = bridge._girder_count() = 4` (`PASS`, $0.347\text{ s}$).
- **Candidate (c):** Sets `bcfg.geometry.n_girders = 0`, failing assertion (`BASELINE_FAIL`, $0.344\text{ s}$).

### 9. TC-REG-CAP-STIFFENER-BUCKLING (DEF-12)
- **Candidate (b):** Evaluates unstiffened web strip buckling under IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 using web strip radius of gyration $r_y = t_w / \sqrt{12}$ and column buckling curve c. Yields $63.4\text{ kN}$ for Geometry 1 and $158.5\text{ kN}$ for Geometry 2 (`PASS`, $0.007\text{ s}$).
- **Candidate (c):** Evaluates squash load $(f_y / \gamma_{m0}) \times A_{wb} / 1000 = 1918.8\text{ kN}$, ignoring slenderness and column buckling (`BASELINE_FAIL`, $0.007\text{ s}$).

### 10. TC-REG-MAT-DENSITY-CONSISTENCY (DEF-13)
- **Candidate (b):** Dynamically reads user density from `material.girder.density` ($70.0\text{ kN/m}^3$) and applies it to `STEEL_UNIT_WEIGHT_kN_m3`, producing resultant $151.43\text{ kN}$ (`PASS`, $0.803\text{ s}$).
- **Candidate (c):** Hardcodes database default $78.5\text{ kN/m}^3 \implies 169.82\text{ kN}$, failing density assertion (`BASELINE_FAIL`, $0.805\text{ s}$).

### 11. TC-REG-FS-CLEAN-WORKING-TREE (DEF-10)
- **Candidate (b):** Anchors `ui_loc.DB_PATH` and `Database.__init__` default path to user AppData. Package directory files exhibit identical before/after SHA-256 hashes under production `@_with_db` queries, missing-db connect does not create files in package, and `Database()` creates zero files in `os.getcwd()` (`PASS`, $3.711\text{ s}$).
- **Candidate (c):** Anchors `ui_loc.DB_PATH` only, leaving `Database()` constructor unanchored, creating `weather.sqlite` in `cwd` (`BASELINE_FAIL`, $15.539\text{ s}$).

### 12. TC-REG-CAD-EXPORT-VS-SCREENSHOT (DEF-09)
- **Candidate (b):** Baseline offscreen export already passes (`PASS`, $2.695\text{ s}$).
- **Candidate (c):** Emits uniform blank image ($\text{std} = 0.0$), failing image entropy threshold (`BASELINE_FAIL`, $2.551\text{ s}$).

---

## 4. Formal Gate Status Summary

- **Actionable Tests Verified:** **12 / 12 (100.0%)**
- **Formally Blocked Tests:** **3 / 15** (`BLOCKED / NOT DEMONSTRATED` under DEC-013, DEC-015, DEC-018)
- **Sensitivity Matrix Gate Verdict:** **APPROVED / READY FOR RE-AUDIT**
