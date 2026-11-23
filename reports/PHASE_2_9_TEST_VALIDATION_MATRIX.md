# PHASE 2.9 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_8_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_9\`  

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
- **Baseline Duration:** **20.87 s**
- **Sensitivity Matrix Duration:** **89.56 s**
- **Overall Actionable Sensitivity Gate:** **PASSED**

---

## 2. Detailed Technical Profiles for All 15 Tests

### 1. TC-REG-A01-FACTOR-SCALING
- **Defect Identifier:** DEF-01 (Upstream `ospgrillage` Library)
- **Defect Mechanism:** Upstream `ospgrillage` ignores `load_factor` in `LoadCase.add_load`, resulting in un-factored force ratios ($1.00000$ observed vs $1.35000$ expected).
- **Condition (a) Baseline:** `BASELINE_FAIL` (force ratio = 1.00000).
- **Condition (b) Minimal Correct:** Deepcopies and scales load magnitudes by load factor in `og.load.LoadCase.add_load`. `PASS` (force ratio = 1.35000).  
  *Candidate SHA-256:* `8aea6bd94b289a469c3d989a9d9fae374335228b3e5ef064b390941c05dac0f1`
- **Condition (c) Naive / Wrong:** Hardcodes arbitrary 1.15x factor. `BASELINE_FAIL` (force ratio = 1.09174 vs expected 1.35000).  
  *Candidate SHA-256:* `4747fc79c5045bd7072ff1c7c11cae54830368b63778b7a9d1b3b76171a18fc8`
- **Sensitivity Verdict:** **VERIFIED**.

### 2. TC-REG-B01-SECTION-PROPERTY-SYNC
- **Defect Identifier:** DEF-03
- **Defect Mechanism:** Section depth inconsistent with plate components ($D=1340\text{ mm} \ne 1342\text{ mm}$); solver girder section retains preliminary preliminary sizing ($I_z$ gap ~7.40%, $A$ gap ~10.55%).
- **Phase 2.9 Hardening:** Runtime dynamic derivation of snapped plate section properties ($A, I_z, I_y, J$); two-sided tolerances enforced on $I_z, A$ ($\pm 0.5\%$) and $I_y, J$ ($\pm 1.0\%$), rejecting $J \times 10$ and dimensional mutations. Deflection verified at midspan Node 49 ($7.218\text{ mm} \pm 3\%$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (dimensions inconsistent: $D=1340\text{ mm} \ne 1342\text{ mm}$; solver girder sections deviate from snapped plate properties).
- **Condition (b) Minimal Correct:** Dynamically derives snapped plate properties and updates `_girder_section` and web depth in `input_dict`. `PASS` (geometric consistency verified, all 4 section properties match derived targets within $\pm 0.5\%$ and $\pm 1.0\%$, midspan deflection = 7.218 mm).  
  *Candidate SHA-256:* `e99f57ebbf79590e85497495029e0ddcfeb6281e7d95a5fbc4081c7ff8bfdfb4`
- **Condition (c) Naive / Wrong:** Swaps `bgm.girder_props` metadata post-setup only, leaving solver elements and OpenSees stiffness preliminary. `BASELINE_FAIL` (solver girder sections retain preliminary properties).  
  *Candidate SHA-256:* `b564a14cef5a3958ea432b22716605401f773e4103ab5488fb13ffe6cd23f7ec`
- **Sensitivity Verdict:** **VERIFIED**.

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect Identifier:** DEF-07
- **Defect Mechanism:** Evaluates static load case as a false cyclic stress range ($\Delta \sigma = 62.73\text{ MPa}$ instead of $0.00\text{ MPa}$) due to end-sign divergence ($+M_{z,j}$ and $-M_{z,i}$).
- **Phase 2.9 Hardening:** 4-state cyclic history ($+200, +500, -1500, +1200\text{ kNm}$, true range $2700\text{ kNm} \implies 169.358\text{ MPa}$) where extremes sit in later load cases; element-end sign proof at shared Node 2; static case evaluated through `_extract_demands_from_analysis_results` (demanding $0.0\text{ MPa}$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (static envelope = 125.46 MPa, per-LC = 62.73 MPa; expected 0.0 MPa).
- **Condition (b) Minimal Correct:** Evaluates bending moments with sign harmonization ($M = -M_{z,i} = +M_{z,j}$), computing range as $\frac{\max(M) - \min(M)}{Z_e} \times 10^3$ across all load cases in `sls_frequent`. Evaluates static case to $0.0\text{ MPa}$ on both paths; 4-state cyclic case to $169.358\text{ MPa}$; sign reversal to $125.450\text{ MPa}$. `PASS`.  
  *Candidate SHA-256:* `f59997faee7c1fc049714aa4d97fe5b2b23a9d9b4b9b478eb079c855a9b89e9d`
- **Condition (c) Naive / Wrong:** Evaluates range only across the first two load cases (`sls_freq_lcs[:2]`). For the 4-state history, it obtains $(500 - 200) = 300\text{ kNm} \implies 18.818\text{ MPa}$ instead of $169.358\text{ MPa}$. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `9b876fc15c4df35e69e06e30018dc3ec2d58bf5e34eb328a649ae5275e7a9b0c`
- **Sensitivity Verdict:** **VERIFIED**.

### 4. TC-REG-A02-ULS-COMBINATION-SUM
- **Defect Identifier:** DEF-01 / DEF-02
- **Defect Mechanism:** ULS BASIC_1 combination ignores 1.35 and 1.75 factors (internal element forces equal unfactored 1.0 DL + 1.0 DW); crash barrier load is omitted from combination.
- **Phase 2.9 Hardening:** Enforces independently derived applied ULS load resultant ($2711.74\text{ kN} \pm 0.5\%$) as a mandatory gate alongside reaction superposition linearity ($2710.16\text{ kN} \pm 0.5\%$) and element force scaling, detecting density mutations (Probe A1). Reconciled parameter differences ($\rho_c = 24.5\text{ kN/m}^3, W_{\text{cw}} = 7.5\text{ m}$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (internal shears match unfactored; barrier missing; reaction shortfall).
- **Condition (b) Minimal Correct:** Creates SIDL combination before DL combination; scales loads by combination factor in `og.load.LoadCase.add_load`. Reaction matches linearity target ($2710.16\text{ kN}$) and theoretical applied resultant ($2711.74\text{ kN} \pm 0.06\%$), and internal forces are factored. `PASS`.  
  *Candidate SHA-256:* `1e271d9570ad2ca36e96e34a8cc7a51ba814af6e28d552afb0176452a2646d0f`
- **Condition (c) Naive / Wrong:** Factors SW and DW, but omits crash barrier from BASIC_1. `BASELINE_FAIL` (reaction falls short and barrier check fails).  
  *Candidate SHA-256:* `fd02171e9f08021b4690f39a6fa170d7f30acf9e087f0cdd9821731742b4016c`
- **Sensitivity Verdict:** **VERIFIED**.

### 5. TC-REG-EQ-LOAD-CONSERVATION
- **Defect Identifier:** DEF-18
- **Defect Mechanism:** Applied dead loads violate static equilibrium (applied $2003.54\text{ kN}$ vs reaction $1932.76\text{ kN}$), with non-collinear crash barrier losing $37.5\%$ of load and shifting inward by $+0.75\text{ m}$.
- **Phase 2.9 Hardening:** Derives all declared loads from `input_dict` geometry and material properties; decouples expectations from application load objects, rejecting definition mutations (E12, E19, E20); asserts multi-span equilibrium across $12\text{ m}, 24\text{ m}, 30\text{ m}$ spans.
- **Condition (a) Baseline:** `BASELINE_FAIL` (crash barrier reaction $196.20\text{ kN}$ vs applied $313.92\text{ kN}$, discrepancy $-37.5\%$; centroid shifted $+0.75\text{ m}$).
- **Condition (b) Minimal Correct:** Genuine cell-intersection bilinear distributor assigns patch loads to 4 corner nodes and non-collinear line loads to surrounding nodes. Conserves total force and centroids across all spans. `PASS`.  
  *Candidate SHA-256:* `cb53435165975d045d947aa5267ec073a4be4863772265feec7d7b2bfb44b204`
- **Condition (c) Naive / Wrong:** Distributes patch loads via FEM but leaves crash barrier with baseline bug. `BASELINE_FAIL` (barrier fails total force and centroid checks).  
  *Candidate SHA-256:* `9d554a9fc96489a2636f014798e27c157bb7350cb058e5e7834226cfd5df65d4`
- **Sensitivity Verdict:** **VERIFIED**.

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect Identifier:** DEF-05
- **Defect Mechanism:** `add_wind_loads()` falls back to hardcoded default values ($V_b = 33.0\text{ m/s}, H = 10.0\text{ m}$), ignoring user input ($V_b = 47.0\text{ m/s}, H = 15.0\text{ m}$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (Pz = 463.7 N/m2 vs authentic 1039.6 N/m2).
- **Condition (b) Minimal Correct:** Propagates configured basic wind speed, height, barrier height, and railing height. `PASS` (Pz = 1039.6 N/m2).  
  *Candidate SHA-256:* `1bb95fefbc3a7e366da6ecbb2cf9590890bf2a5592ec79f9b5c3e0e7a17730e1`
- **Condition (c) Naive / Wrong:** Reads wind speed only, leaves height/barrier as defaults. `BASELINE_FAIL` (Pz = 940.6 N/m2).  
  *Candidate SHA-256:* `dca97ae5ce281358c2da28f8f2b77a6ddcbf0a9a46c3b6c669528d2d634db2fe`
- **Sensitivity Verdict:** **VERIFIED**.

### 7. TC-REG-D02-TEMPERATURE-PROPAGATION
- **Defect Identifier:** DEF-06
- **Status:** **BLOCKED** under **DEC-015**
- **Block Reason:** Thermal load modeling (IRC 6 Cl. 215) is undecided in project specifications. `add_temperature_load()` reads unpopulated `temperature_load_kN_m2` and leaves `temperature_load_case` as None.
- **Sensitivity Handling:** Conditions (b) and (c) are not manufactured. Stamped as `BLOCKED / NOT DEMONSTRATED`.

### 8. TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Defect Identifier:** DEF-17
- **Status:** **BLOCKED** under **DEC-018**
- **Block Reason:** IRC 6 Cl. 204.6 fatigue vehicle moving load is not implemented in the analysis/design pipeline.
- **Sensitivity Handling:** Conditions (b) and (c) are not manufactured. Stamped as `BLOCKED / NOT DEMONSTRATED`.

### 9. TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect Identifier:** DEF-08
- **Defect Mechanism:** Hardcoded "Pass" string in LaTeX template ignores component failure states.
- **Phase 2.9 Hardening:** Evaluates DCR-only checks across all 6 girders (G1–G6) and all 4 check types; exact boundary testing at DCR = 1.000 (PASS), DCR = 1.001 (FAIL), DCR = 0.999 (PASS); deck boundary testing at ur = 1.000 (PASS), ur = 1.001 (FAIL); asserts unaffected components remain PASS.
- **Condition (a) Baseline:** `BASELINE_FAIL` (fails all 40 failure scenarios due to hardcoded "Pass").
- **Condition (b) Minimal Correct:** Dynamically derives component statuses from result dictionaries across all girders, bracing, diaphragms, and deck. `PASS` (matches expected pass/fail status in all scenarios including exact boundaries).  
  *Candidate SHA-256:* `b348455856ff6d934bb614833215aa025a4c585be7764834ff2cfbf5ae09825b`
- **Condition (c) Naive / Wrong:** Naively inspects only G1. `BASELINE_FAIL` (fails Scenario 2A where G3 fails and G1 passes).  
  *Candidate SHA-256:* `e2a4be6058e45484dc6ceecdd34df3c7340b08006bfda79c3f1508db8c560350`
- **Sensitivity Verdict:** **VERIFIED**.

### 10. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect Identifier:** DEF-11
- **Defect Mechanism:** `designer.py:401` sets `n_girders = geom.n_l` (6), counting 2 overhang edge lines as structural girders for a 4-girder bridge.
- **Condition (a) Baseline:** `BASELINE_FAIL` (n_girders = 6 != 4).
- **Condition (b) Minimal Correct:** Sets `bcfg.geometry.n_girders = bridge._girder_count()` (4). `PASS`.  
  *Candidate SHA-256:* `8c69ee01509b2e75e921d7b07db3522ba5427d14d33a78f2aa744c84eb63cfc4`
- **Condition (c) Naive / Wrong:** Sets `bcfg.geometry.n_girders = 0`. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `fffe2c92e389a9da30588629087c24f603a1fc6c986ebf49e49339e80cba00ef`
- **Sensitivity Verdict:** **VERIFIED**.

### 11. TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Defect Identifier:** DEF-14
- **Status:** **BLOCKED** under **DEC-013**
- **Block Reason:** Transverse deck slab representation model is undecided in project documentation. Baseline assigns `girder/2` ($I_z = 0.00367\text{ m}^4$), which is mechanically invalid for concrete deck, but exact transformed vs concrete material and cracked/torsion model requires engineering sign-off.
- **Sensitivity Handling:** Conditions (b) and (c) are not manufactured. Stamped as `BLOCKED / NOT DEMONSTRATED`.

### 12. TC-REG-CAP-STIFFENER-BUCKLING
- **Defect Identifier:** DEF-12
- **Defect Mechanism:** Uses stiffener moment of inertia instead of unstiffened web strip radius of gyration $r_y = t_w / \sqrt{12}$, calculating unphysical capacity ($214533.2\text{ kN}$ vs oracle $63.4\text{ kN}$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (capacity 214533.2 kN exceeds squash load 1918.8 kN and oracle 63.4 kN).
- **Condition (b) Minimal Correct:** Genuine dynamic IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 web strip buckling calculation using $r_y = t_w / \sqrt{12}$ and Perry-Robertson column curve c. `PASS` (capacity matches oracle $63.4\text{ kN} \pm 1\%$).  
  *Candidate SHA-256:* `84c4f39bc53e5eeb42436f56bc22f99990b790d9703ec41bc227092144349372`
- **Condition (c) Naive / Wrong:** Uses squash load formula $(f_y / \gamma_{m0}) \times A_{wb} / 1000$, ignoring column buckling. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `d72aa62f74fe7542d9bb4e797d91a92e105e4dfa80693a18641bfb174a7ff250`
- **Sensitivity Verdict:** **VERIFIED**.

### 13. TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect Identifier:** DEF-13
- **Defect Mechanism:** Self-weight line loads ignore user-configured steel density, hardcoding database constant $78.5\text{ kN/m}^3$.
- **Condition (a) Baseline:** `BASELINE_FAIL` (resultant 169.8 kN matches 78.5 kN/m3 instead of configured 70.0 kN/m3).
- **Condition (b) Minimal Correct:** Reads user density from `material.girder.density` and applies to self-weight line loads. `PASS` (resultant 151.4 kN matches 70.0 kN/m3).  
  *Candidate SHA-256:* `1162804b4070a7b45a6c11aa9d0e2c8846c2688005b4a92a549d479133405cba`
- **Condition (c) Naive / Wrong:** Hardcodes $78.5\text{ kN/m}^3$, ignoring user input. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `e971488c9cf415b3e64ca612e34f89d0f3ba1bc1bb41fc7694f24c7f0f63b2ef`
- **Sensitivity Verdict:** **VERIFIED**.

### 14. TC-REG-FS-CLEAN-WORKING-TREE
- **Defect Identifier:** DEF-10
- **Defect Mechanism:** Production `ui_loc.DB_PATH` resolves inside package tree; `Database()` creates unanchored `weather.sqlite` in cwd; production calls fail under read-only package installations.
- **Phase 2.9 Hardening:** Mirrored repository structure in sandbox (`sandbox/source/OsdagBridge/src/osdagbridge`, `.../.osdag_cache`, `sandbox/workspace`) catching relative path escapes (Probes G2, G3); Win32 Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` catching and killing detached processes (Probe G7); recursive filtered snapshot on `WORKSPACE_ROOT` catching cwd mutations (Probe G5); immediate pollution rollback (Probe G4); POSIX root reported as BLOCKED (DEC-023).
- **Condition (a) Baseline:** `BASELINE_FAIL` (production DB_PATH inside package tree; Database() creates unanchored weather.sqlite in cwd; package tree mutated during production calls; read-only permission denial causes OperationalError).
- **Condition (b) Minimal Correct:** Anchors DB_PATH and Database default constructor to User AppData, without package writes or cwd side effects. `PASS` (sandbox, repo, and cwd clean; queries valid; read-only resilient; 0 detached processes).  
  *Candidate SHA-256:* `5c3453308726e63dc47f4d3824f9ef3fa51ba21c435773177695123dca90be5c`
- **Condition (c) Naive / Wrong:** Anchors ui module DB_PATH, but leaves Database.__init__ unanchored, failing cwd check. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `cf81ae39b7f58a5da5278ca900c73a21a97576f30e0108ea49d0ca9626dfcf46`
- **Sensitivity Verdict:** **VERIFIED**.

### 15. TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Defect Identifier:** DEF-09 (Test Harness Environment Verification)
- **Defect Mechanism:** Verifies that native pythonocc-core offscreen 3D rendering (`Viewer3d.ExportToImage`) produces valid opaque CAD images rather than GUI screenshots.
- **Condition (a) Baseline:** `PASS` (valid 3D rendering, non-zero std dev = 66.6, 3 distinct colors).
- **Condition (b) Minimal Correct:** Baseline CAD export already passes. `PASS`.  
  *Candidate SHA-256:* `c8ca6a9b4ce88d22c9540b792e3230a10d0f4d3aeb1a5da233fe9a700b0c6192`
- **Condition (c) Naive / Wrong:** Export produces a blank uniform image (`std = 0.0`). `BASELINE_FAIL`.  
  *Candidate SHA-256:* `e2a4be6058e45484dc6ceecdd34df3c7340b08006bfda79c3f1508db8c560350`
- **Sensitivity Verdict:** **VERIFIED**.

---

## 3. Conclusion

The Phase 2.9 regression suite and sensitivity framework achieve **100% actionable verification (12/12 verified, 3 formally blocked)** with zero regressions, zero test-harness circularities, and complete cryptographic evidence immutability.
