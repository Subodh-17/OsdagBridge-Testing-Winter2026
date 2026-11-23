# PHASE 2.7 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`)  
**Controlling Document:** `reports/PHASE_2_6_FINAL_INDEPENDENT_GATE_AUDIT.md`  
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
- **Defect:** Upstream `ospgrillage` ignores `load_factor` in `LoadCase.add_load`, resulting in un-factored force ratios ($1.00000$ observed vs $1.35000$ expected).
- **Condition (a) Baseline:** `BASELINE_FAIL` (force ratio = 1.00000).
- **Condition (b) Minimal Correct:** Deepcopies and scales load magnitudes by load factor in `og.load.LoadCase.add_load`. `PASS` (force ratio = 1.35000).  
  *Candidate SHA-256:* `8aea6bd94b289a469c3d989a9d9fae374335228b3e5ef064b390941c05dac0f1`
- **Condition (c) Naive / Wrong:** Hardcodes arbitrary 1.15x factor. `BASELINE_FAIL` (force ratio = 1.15000).  
  *Candidate SHA-256:* `4747fc79c5045bd7072ff1c7c11cae54830368b63778b7a9d1b3b76171a18fc8`
- **Sensitivity Status:** **VERIFIED**.

### 2. TC-REG-B01-SECTION-PROPERTY-SYNC
- **Defect:** Section depth inconsistent with plate components ($D=1340\text{ mm} \ne 1342\text{ mm}$); solver girder section retains preliminary preliminary sizing ($I_z$ gap ~7.40%, $A$ gap ~10.55%).
- **Condition (a) Baseline:** `BASELINE_FAIL` (dimension gap detected, solver Iz gap ~7.40%).
- **Condition (b) Minimal Correct:** Synchronizes `_girder_section` with snapped plate dimensions and aligns `input_dict` web depth. `PASS` (dimensions consistent, properties match oracle, midspan deflection = 7.218 mm within 1%).  
  *Candidate SHA-256:* `e9e254e21e1a69a680a3ceea94089b5d43f21236adb0d3ccac05bbb0d6e37cbb`
- **Condition (c) Naive / Wrong:** Modifies `bgm.girder_props` metadata post-setup only, leaving solver stiffness preliminary. `BASELINE_FAIL` (solver retained preliminary sections).  
  *Candidate SHA-256:* `b564a14cef5a3958ea432b22716605401f773e4103ab5488fb13ffe6cd23f7ec`
- **Sensitivity Status:** **VERIFIED**.

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect:** Evaluates static load case as a false cyclic stress range ($\Delta \sigma = 62.73\text{ MPa}$ instead of $0.00\text{ MPa}$) due to end-sign divergence ($+M_{z,j}$ and $-M_{z,i}$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (static load case produces 62.73 MPa false cyclic range).
- **Condition (b) Minimal Correct:** Evaluates bending moments with sign harmonization ($M = -M_{z,i} = +M_{z,j}$), computing range as $\frac{\max(M) - \min(M)}{Z_e} \times 10^3$. Evaluates both Hogging $\to$ Sagging and Sagging $\to$ Hogging directions identically, and zeroes static moment across internal Node 2 envelope ($0.00\text{ MPa}$). `PASS`.  
  *Candidate SHA-256:* `95fdb5c817ee2d228939adddb2626a9deb0fdfd800b0e143d335ce0f15688736`
- **Condition (c) Naive / Wrong:** Zeros envelope statically, but leaves per-load-case broken. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `9b7a49d6d5588e77d3f782807ff2461be7ea6c64ed49412c54208cbd7dc12556`
- **Sensitivity Status:** **VERIFIED**.

### 4. TC-REG-A02-ULS-COMBINATION-SUM
- **Defect:** ULS BASIC_1 combination ignores 1.35 and 1.75 factors (internal element forces equal unfactored 1.0 DL + 1.0 DW); crash barrier load is omitted from combination.
- **Condition (a) Baseline:** `BASELINE_FAIL` (reactions and shears match unfactored; barrier missing).
- **Condition (b) Minimal Correct:** Creates SIDL combination before DL combination so barrier is registered; scales loads by combination factor in `og.load.LoadCase.add_load`. Reaction matches linearity target ($2710.16\text{ kN} \pm 0.001\%$) and internal forces are factored. `PASS`.  
  *Candidate SHA-256:* `1e271d9570ad2ca36e96e34a8cc7a51ba814af6e28d552afb0176452a2646d0f`
- **Condition (c) Naive / Wrong:** Factors SW and DW, but omits crash barrier from BASIC_1. `BASELINE_FAIL` (reaction falls short and barrier check fails).  
  *Candidate SHA-256:* `fd02171e9f08021b4690f39a6fa170d7f30acf9e087f0cdd9821731742b4016c`
- **Sensitivity Status:** **VERIFIED**.

### 5. TC-REG-EQ-LOAD-CONSERVATION
- **Defect:** Finite element grillage load distribution causes $-37.5\%$ crash barrier force shortfall and $+0.75\text{ m}$ centroid shift; $+3.1\%$ excess on deck slab and wearing course; and lacks along-span load conservation.
- **Condition (a) Baseline:** `BASELINE_FAIL` (barrier force diff $-117.7\text{ kN}$, centroid $+0.75\text{ m}$, DD excess $+39.4\text{ kN}$).
- **Condition (b) Minimal Correct:** FEM cell-intersection bilinear shape function distribution for patches and non-collinear line loads; SW derived from applied steel density; asserts support node share $\le 12\%$ and midspan region $[0.25L, 0.75L]$ share $\in [45\%, 60\%]$. `PASS`.  
  *Candidate SHA-256:* `e1e92b5ad5ced8935cd32404d38075bd33ed0b71defc0fd096eb2510e78c6384`
- **Condition (c) Naive / Wrong:** FEM distribution on patches, but leaves barrier line loads with baseline bug. `BASELINE_FAIL` (barrier shortfall $-37.5\%$, centroid $+0.75\text{ m}$).  
  *Candidate SHA-256:* `3e3aee4700eb8cc9db91ea7319550ff8e89cb8798a5696945ee8155d87d19ebf`
- **Sensitivity Status:** **VERIFIED**.

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect:** Hardcoded basic wind speed ($33.0\text{ m/s}$) and geometric heights ($10.0\text{ m}$) used during wind load generation, ignoring user input configuration ($47.0\text{ m/s}$, $15.0\text{ m}$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (speed 33.0 m/s, height 10.0 m used).
- **Condition (b) Minimal Correct:** Propagates user basic wind speed, exposed height, and barrier/railing heights from `input_dict`. `PASS`.  
  *Candidate SHA-256:* `1aae54f8d09b29254d8140df2a61bb93d6237e40fe2fc0b23e5de5b4aa9fef47`
- **Condition (c) Naive / Wrong:** Reads wind speed only, leaves heights at default. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `5f57a59399df274e87cb0a34741fb386ac360b504ecf6af5bad82396457af3ff`
- **Sensitivity Status:** **VERIFIED**.

### 7. TC-REG-D02-TEMPERATURE-PROPAGATION
- **Defect:** `analyser.py` looks for nonexistent key `'temperature_load_kN_m2'`; thermal effects omitted.
- **Condition (a) Baseline:** `BLOCKED` (Formal specification pending under DEC-015).
- **Condition (b) Minimal Correct:** `BLOCKED`.  
  *Candidate SHA-256:* `None`
- **Condition (c) Naive / Wrong:** `BLOCKED`.  
  *Candidate SHA-256:* `None`
- **Sensitivity Status:** **BLOCKED / NOT DEMONSTRATED**.

### 8. TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Defect:** Genuine IRC 6 Cl. 204.6 fatigue vehicle moving load analysis not implemented in pipeline.
- **Condition (a) Baseline:** `BLOCKED` (Formal specification pending under DEC-018).
- **Condition (b) Minimal Correct:** `BLOCKED`.  
  *Candidate SHA-256:* `None`
- **Condition (c) Naive / Wrong:** `BLOCKED`.  
  *Candidate SHA-256:* `None`
- **Sensitivity Status:** **BLOCKED / NOT DEMONSTRATED**.

### 9. TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect:** Executive summary emits hardcoded `\noindent Girder design pass` unconditionally, ignoring girder failures, member failures, and table status.
- **Condition (a) Baseline:** `BASELINE_FAIL` (emits pass across 23/24 failure scenarios).
- **Condition (b) Minimal Correct:** Dynamically derives component pass/fail status across all girders G1–G6, cross-bracing members, end-diaphragm members, and deck slab, synchronizing with `Overall Design Status`. Passes all 25 scenarios. `PASS`.  
  *Candidate SHA-256:* `70020738b6c969d954421bf617ac574c9db112d742b61dcefc97eecf5df73217`
- **Condition (c) Naive / Wrong:** Inspects only G1 and the first member of CB/ED. `BASELINE_FAIL` (fails in 20/24 failure scenarios).  
  *Candidate SHA-256:* `6ddab2ca36563e83a811ec261fe3ae96f387e234e008cf7c159fe9850574b170`
- **Sensitivity Status:** **VERIFIED**.

### 10. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect:** `designer.py:401` sets `n_girders = geom.n_l` (6), incorrectly counting slab overhang edge lines as structural girders for a 4-girder bridge.
- **Condition (a) Baseline:** `BASELINE_FAIL` (n_girders = 6 vs 4).
- **Condition (b) Minimal Correct:** Assigns `bcfg.geometry.n_girders = bridge._girder_count()` (4). `PASS`.  
  *Candidate SHA-256:* `9d60549b7c549fcba77d33c720f5e6ada33efbc30b6b73503feb1da9d757c561`
- **Condition (c) Naive / Wrong:** Assigns `n_girders = 0`. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `546ed5285c58798de84b6c5b7c18891ebbd6edb71a516b1cf224fca235afec3f`
- **Sensitivity Status:** **VERIFIED**.

### 11. TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Defect:** Transverse deck slab members assigned half the section properties of longitudinal steel girders (`girder/2`).
- **Condition (a) Baseline:** `BLOCKED` (Formal specification pending under DEC-013).
- **Condition (b) Minimal Correct:** `BLOCKED`.  
  *Candidate SHA-256:* `None`
- **Condition (c) Naive / Wrong:** `BLOCKED`.  
  *Candidate SHA-256:* `None`
- **Sensitivity Status:** **BLOCKED / NOT DEMONSTRATED**.

### 12. TC-REG-CAP-STIFFENER-BUCKLING
- **Defect:** Uses stiffener moment of inertia ($I_{ys} = 8.16\times 10^7\text{ mm}^4$) instead of unstiffened web strip radius of gyration ($r_y = t_w / \sqrt{12} \approx 2.309\text{ mm}$), overestimating buckling capacity by 3300x.
- **Condition (a) Baseline:** `BASELINE_FAIL` (capacity 214,533 kN vs oracle 63.4 kN).
- **Condition (b) Minimal Correct:** Evaluates IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 web strip buckling with $r_{wb} = t_w / \sqrt{12}$ and Perry-Robertson curve c. `PASS` (capacity 63.4 kN matches oracle).  
  *Candidate SHA-256:* `ee7d2205f4e3fac18f4f64b97f9067fb9ee39b1a81925f99b023ca7ab0264699`
- **Condition (c) Naive / Wrong:** Uses squash load formula $(f_y / \gamma_{m0}) \times A_{wb} / 1000$ (1918.8 kN), ignoring buckling. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `d153f36a995395be7ab7359be96fb27344194732efef1e5dbd7f27b281a37124`
- **Sensitivity Status:** **VERIFIED**.

### 13. TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect:** Self-weight line loads hardcode $78.5\text{ kN/m}^3$, ignoring user input configuration ($70.0\text{ kN/m}^3$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (resultant 169.8 kN vs expected 151.4 kN).
- **Condition (b) Minimal Correct:** Reads `material.girder.density` and applies it dynamically to self-weight line loads across multiple spans (24m: 151.43 kN; 30m: 189.29 kN). `PASS`.  
  *Candidate SHA-256:* `27dcde31fcebf3a4b86a950fbe77428537a16067003af037db0cf7ea0ab4247c`
- **Condition (c) Naive / Wrong:** Retains hardcoded default 78.5 kN/m3. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `e7ce2665803ab3767a2b503a4817b27677a61ffd87e5317df9d020fec1dbab2a`
- **Sensitivity Status:** **VERIFIED**.

### 14. TC-REG-FS-CLEAN-WORKING-TREE
- **Defect:** Default `DB_PATH` resolves inside package tree; `Database()` default constructor creates unanchored `weather.sqlite` in current working directory; attempts to write to package tree under production calls; fails in read-only environments.
- **Condition (a) Baseline:** `BASELINE_FAIL` (DB inside package, creates cwd file, mutates package copy, raises `OperationalError` under write denial).
- **Condition (b) Minimal Correct:** Anchors database paths to User AppData; passes production query assertions (32 states, max temp 48.2); leaves real package tree and sandboxes 100% pristine; succeeds under real OS read-only permission denial (`icacls /deny`). `PASS`.  
  *Candidate SHA-256:* `5ca492306e7f244ebbc921fb5cbe630189cd6ac17dc2157dbf68e5a5ab3e0aaf`
- **Condition (c) Naive / Wrong:** Anchors `ui_loc.DB_PATH` but leaves `Database.__init__` unanchored, creating file in cwd. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `06fe6694b196a51f59d23d742e499d882d16c5cfabf242bb0792db26f1179cee`
- **Sensitivity Status:** **VERIFIED**.

### 15. TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Defect:** Verifies that CAD export uses genuine OpenCASCADE offscreen 3D rendering pipeline rather than GUI viewport window screenshots.
- **Condition (a) Baseline:** `PASS` (native offscreen Viewer3d.ExportToImage produces non-blank 3D render: std=66.6, 3 distinct colors).
- **Condition (b) Minimal Correct:** Standard baseline pipeline. `PASS`.  
  *Candidate SHA-256:* `b488b1a3676bbfa2988617f4ef9ec47c138cb8922db887ebbc6b7c214b685ab2`
- **Condition (c) Naive / Wrong:** Emits blank uniform image (std=0.0). `BASELINE_FAIL`.  
  *Candidate SHA-256:* `d9cd7ff8656bf6a3592aa4dce24dd3b2c40d89f05fccb14adf0a456238ae0616`
- **Sensitivity Status:** **VERIFIED**.
