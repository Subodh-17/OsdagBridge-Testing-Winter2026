# PHASE 2.10 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_9_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_10\`  

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
- **Baseline Duration:** **59.74 s**
- **Sensitivity Matrix Duration:** **73.26 s**
- **Post-Manifest Verification:** **SUCCESS (0 file drift across all directories)**
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
- **Phase 2.10 Hardening (P1):** Added independent fixed-input hand reference oracle ($A = 0.025192\text{ m}^2, I_z = 0.00792758\text{ m}^4, I_y = 0.00020682\text{ m}^4, J = 1.81663\times 10^{-6}\text{ m}^4$) independent of `_girder_value`. Added asymmetric-flange section oracle fixture verifying general parallel axis formulas ($A = 0.0325\text{ m}^2, \bar{y} = 0.539577\text{ m}, I_z = 0.0088700\text{ m}^4, I_y = 0.0003672\text{ m}^4, J = 4.0708\times 10^{-6}\text{ m}^4$).
- **Condition (a) Baseline:** `BASELINE_FAIL` (dimensions inconsistent: $D=1340\text{ mm} \ne 1342\text{ mm}$; solver girder sections deviate from snapped plate properties and fixed hand oracle).
- **Condition (b) Minimal Correct:** Dynamically derives snapped plate properties and updates `_girder_section` and web depth in `input_dict`. `PASS` (geometric consistency verified, all 4 section properties match fixed and derived targets within $\pm 0.5\%$ and $\pm 1.0\%$, midspan deflection = 7.218 mm).  
  *Candidate SHA-256:* `e99f57ebbf79590e85497495029e0ddcfeb6281e7d95a5fbc4081c7ff8bfdfb4`
- **Condition (c) Naive / Wrong:** Swaps `bgm.girder_props` metadata post-setup only, leaving solver elements and OpenSees stiffness preliminary. `BASELINE_FAIL` (solver girder sections retain preliminary properties).  
  *Candidate SHA-256:* `b564a14cef5a3958ea432b22716605401f773e4103ab5488fb13ffe6cd23f7ec`
- **Sensitivity Verdict:** **VERIFIED**.

### 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
- **Defect Identifier:** DEF-07
- **Defect Mechanism:** Evaluates static load case as a false cyclic stress range ($\Delta \sigma = 62.73\text{ MPa}$ instead of $0.00\text{ MPa}$) due to end-sign divergence ($+M_{z,j}$ and $-M_{z,i}$).
- **Phase 2.10 Hardening (P2):** Upgraded cyclic case to 5 load cases with non-adjacent extrema (+200, +1200 MAX in LC2, +300, -1500 MIN in LC4, +100 kNm) across 3 elements along G1, with asymmetric end moments (governing 2700 kNm range in midspan Element 2 end j).
- **Condition (a) Baseline:** `BASELINE_FAIL` (static load case evaluates to false cyclic range on envelope and per-LC paths).
- **Condition (b) Minimal Correct:** Evaluates section bending moments with consistent sign convention across all frequent load cases and elements, producing true range 2700 kNm (169.358 MPa) and 0.00 MPa on static load. `PASS`.  
  *Candidate SHA-256:* `a96eb2df3e25ba114e9e1c3132bb820ddcbe43b4db09156b27e85c13b7337cb0`
- **Condition (c) Naive / Wrong:** Inspects only first two load cases. `BASELINE_FAIL` (evaluates range as 1000 kNm / 18.82 MPa instead of 2700 kNm / 169.36 MPa).  
  *Candidate SHA-256:* `6ef8cf5ecbe3d87042a177ff8d05dd31bb488737ea73f00f074dff285321f8a8`
- **Sensitivity Verdict:** **VERIFIED**.

### 4. TC-REG-A02-ULS-COMBINATION-SUM
- **Defect Identifier:** DEF-01 / DEF-02
- **Defect Mechanism:** FE solver ignores ULS combination factors in BASIC_1; crash barrier load omitted from combination.
- **Phase 2.10 Hardening (P1):** Added component-wise reaction assertions against independent physical oracles (SW: 165.28 kN, DD: 1249.50 kN, DW: 216.00 kN, CB: 313.92 kN) within 1.0% tolerance, eliminating the error cancellation noted in Claude's audit (§8).
- **Condition (a) Baseline:** `BASELINE_FAIL` (shears un-factored; barrier omitted; component reactions deviate: SW 169.82 vs 165.28 kN, DD 1314.38 vs 1249.50 kN, DW 252.36 vs 216.00 kN, CB 196.20 vs 313.92 kN; total reaction 1736.55 kN != 2710.16 kN).
- **Condition (b) Minimal Correct:** Scaled load magnitudes in `LoadCase.add_load`, creates SIDL before DL combination, sets carriageway width and densities, and applies FEM distribution. `PASS` (all component reactions match within 1.0%, applied resultant matches 2711.74 kN within 0.001%).  
  *Candidate SHA-256:* `72d73f114c026e6900f8623714b13a726715f3cb935ee5b30ce5a5efc272bc19`
- **Condition (c) Naive / Wrong:** Factors SW and DW, but omits crash barrier and FEM patch fix. `BASELINE_FAIL` (barrier omitted; component reactions deviate).  
  *Candidate SHA-256:* `943da4628ee3e2c3586a11e8ddfc7df620579e0f10c6607e4d8a25c156f082e6`
- **Sensitivity Verdict:** **VERIFIED**.

### 5. TC-REG-EQ-LOAD-CONSERVATION
- **Defect Identifier:** DEF-18
- **Defect Mechanism:** Static equilibrium and transverse spatial load distribution violated in FE grillage (barrier force shortfall -37.5%, centroid shift +0.75m).
- **Phase 2.10 Hardening (P1):** Reconciled physical oracles with A02 ($\rho_c = 24.5\text{ kN/m}^3, W_{\text{cw}} = 7.5\text{ m}, W_{\text{deck}} = 8.5\text{ m}$). Eliminated production helper circularity; derived applied loads and exact transverse line shares from raw input keys. Tightened tolerance to 0.5% (`rel_tol=0.005`).
- **Condition (a) Baseline:** `BASELINE_FAIL` (barrier force diff -117.7 kN (-37.5%), centroid shift dx=+0.750m; DD and DW line shares deviate).
- **Condition (b) Minimal Correct:** Bilinear shape function distribution over finite element grid for patch loads and non-collinear line loads, combined with input-derived dead loads. `PASS` (exact 100% force and centroid conservation across SW, DD, DW, CB).  
  *Candidate SHA-256:* `d30b65f7c352932f913d9cf9e1d88bb44778e7276725ea3e9fcae9db98e6a100`
- **Condition (c) Naive / Wrong:** Distributes patch loads via FEM but leaves crash barrier line loads un-fixed. `BASELINE_FAIL` (barrier force shortfall -37.5%, centroid shift dx=+0.750m).  
  *Candidate SHA-256:* `e94f1c7c9ec9ca66a4bc20d75471d5ea2f3780feae2eefec8f08f237ef5805c8`
- **Sensitivity Verdict:** **VERIFIED**.

### 6. TC-REG-D01-WIND-SPEED-PROPAGATION
- **Defect Identifier:** DEF-05
- **Defect Mechanism:** Wind load module ignores user basic wind speed (uses default 33.0 m/s), ignores exposed height (uses default 10.0 m), and sets barrier/railing heights to 0.0 m.
- **Condition (a) Baseline:** `BASELINE_FAIL` (wind load magnitude 153.2 kN matches hardcoded default 33 m/s / 10 m instead of user 47 m/s / 18 m target 310.8 kN).
- **Condition (b) Minimal Correct:** Reads user basic wind speed, height, barrier height, and railing height from `input_dict` and passes to `create_wind_load()`. `PASS` (load magnitude 310.8 kN matches user parameters).  
  *Candidate SHA-256:* `d9cb011855e4bf37d1d2b86940608fa844b20a3597d351be8c9be3b3064beff3`
- **Condition (c) Naive / Wrong:** Reads `basic_wind_speed` only, leaving height and barrier as 0.0 defaults. `BASELINE_FAIL` (load magnitude 226.4 kN falls short of expected 310.8 kN).  
  *Candidate SHA-256:* `8c3be318f70d74431db61e6d309228ebaa2ce355ce778cbe4a30e84b80e4ddfc`
- **Sensitivity Verdict:** **VERIFIED**.

### 7. TC-REG-D02-TEMPERATURE-PROPAGATION
- **Defect Identifier:** DEF-06
- **Status:** **BLOCKED / NOT DEMONSTRATED** (DEC-015 Pending: Thermal modeling undecided under IRC 6 Cl. 215).

### 8. TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS
- **Defect Identifier:** DEF-17
- **Status:** **BLOCKED / NOT DEMONSTRATED** (DEC-018 Pending: IRC 6 Cl. 204.6 fatigue vehicle moving load not implemented in analysis/design pipeline).

### 9. TC-REG-RPT-EXEC-SUMMARY-STATUS
- **Defect Identifier:** DEF-08
- **Defect Mechanism:** `executive_summary()` unconditionally emits `\noindent Girder design pass` regardless of component or single-girder failures.
- **Phase 2.10 Hardening (P2):** Added cross-bracing and end-diaphragm exact 0.999 / 1.000 / 1.001 boundary tests; added narrative independence scenarios (component failure with `overall_status` PASS, and all pass with `overall_status` FAIL). Total 74 scenarios evaluated.
- **Condition (a) Baseline:** `BASELINE_FAIL` (emits hardcoded pass narrative in 64 of 74 failure scenarios).
- **Condition (b) Minimal Correct:** Dynamically derives component statuses from results dictionaries, enforces exact $> 1.0$ boundaries, and derives table overall status. `PASS` (all 74 scenarios verified).  
  *Candidate SHA-256:* `5d80016baea1e342898ea0ea1d86d528b7e6bc7ef04e287fa4900a394ec5ce66`
- **Condition (c) Naive / Wrong:** Evaluates G1 only, ignoring G2–G6. `BASELINE_FAIL` (fails in 54 of 74 scenarios).  
  *Candidate SHA-256:* `6ef438b4d1b816ae529ec96c3eb447b864a78cb9be1d12521c7d3d2cf59fa943`
- **Sensitivity Verdict:** **VERIFIED**.

### 10. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
- **Defect Identifier:** DEF-11
- **Defect Mechanism:** `BridgeConfig.from_plate_girder_bridge` sets `geometry.n_girders = geom.n_l` (6), incorrectly counting 2 overhang edge lines as structural girders.
- **Condition (a) Baseline:** `BASELINE_FAIL` (`bcfg.geometry.n_girders = 6`, expected 4).
- **Condition (b) Minimal Correct:** Sets `bcfg.geometry.n_girders = bridge._girder_count()` (4). `PASS`.  
  *Candidate SHA-256:* `d577ca226d7010a30b42c67fe99742c3be992c43ee6df9f929d2b27150c33a20`
- **Condition (c) Naive / Wrong:** Sets `n_girders = 0`. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `82e36bf860a9f3818e381ae2128a5cf57d69b9f365d9e51b1451f28b3cf17d2a`
- **Sensitivity Verdict:** **VERIFIED**.

### 11. TC-REG-GEO-SLAB-SECTION-PROPERTIES
- **Defect Identifier:** DEF-14
- **Status:** **BLOCKED / NOT DEMONSTRATED** (DEC-013 Pending: Transverse deck slab representation model undecided).

### 12. TC-REG-CAP-STIFFENER-BUCKLING
- **Defect Identifier:** DEF-12
- **Defect Mechanism:** Bearing stiffener capacity calculation uses stiffener plate second moment of area $I_{ys}$ instead of unstiffened web strip radius of gyration $r_y = t_w / \sqrt{12}$, overpredicting capacity by ~3300x.
- **Condition (a) Baseline:** `BASELINE_FAIL` (capacity reported as 214533.2 kN vs oracle 63.4 kN).
- **Condition (b) Minimal Correct:** Genuine dynamic IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 web strip buckling calculation using $r_y = t_w / \sqrt{12}$. `PASS` (capacity reported as 63.4 kN, matching oracle within 0.1%).  
  *Candidate SHA-256:* `e5ce18a8b273418c3558b297b8332997282b8a7f4ea24329a28564a2f8b5a034`
- **Condition (c) Naive / Wrong:** Squash load formula $(f_y / \gamma_{m0}) \cdot A_{wb}$ ignoring buckling. `BASELINE_FAIL` (capacity 1918.8 kN deviates from buckling oracle 63.4 kN).  
  *Candidate SHA-256:* `7982f1b40742f9b1fe2ca097e30561211dcbf5df98b0dd479a0937a6b32df54d`
- **Sensitivity Verdict:** **VERIFIED**.

### 13. TC-REG-MAT-DENSITY-CONSISTENCY
- **Defect Identifier:** DEF-13
- **Defect Mechanism:** Self-weight line loads hardcode steel density to 78.5 kN/m³ in `analyser.py:STEEL_UNIT_WEIGHT_kN_m3`, ignoring user input (e.g. 70.0 kN/m³).
- **Condition (a) Baseline:** `BASELINE_FAIL` (self-weight resultant 169.8 kN matches 78.5 kN/m³ instead of user 70.0 kN/m³ target 151.4 kN).
- **Condition (b) Minimal Correct:** Dynamically reads user density from `input_dict` and applies to `STEEL_UNIT_WEIGHT_kN_m3`. `PASS` (self-weight resultant 151.4 kN matches user input).  
  *Candidate SHA-256:* `c0ba3c8da88a032890dbcefeeb2244249a5b8f05fe3108c3d9a19c62377b5597`
- **Condition (c) Naive / Wrong:** Retains hardcoded 78.5 kN/m³. `BASELINE_FAIL`.  
  *Candidate SHA-256:* `fa1734f40f0a59be8c8942b0ce89547ea87cfd7a127a3be20e6a4ba567793d93`
- **Sensitivity Verdict:** **VERIFIED**.

### 14. TC-REG-FS-CLEAN-WORKING-TREE
- **Defect Identifier:** DEF-10
- **Defect Mechanism:** Production `ui_loc.DB_PATH` resolves inside the package tree; `Database()` default constructor creates unanchored `weather.sqlite` in current working directory.
- **Phase 2.10 Hardening (P0):** OS-level `ProcessLifetimeJob` with Win32 Job Objects / POSIX process groups tracking active process count. 5.0 s bounded polling window to detect delayed background writers.
- **Condition (a) Baseline:** `BASELINE_FAIL` (package tree mutated: created `src/osdagbridge/core/data/project_location/weather.sqlite`; cwd unanchored).
- **Condition (b) Minimal Correct:** Anchors `DB_PATH` and `Database` constructor to User AppData, without package writes or cwd side effects. `PASS` (zero package or cwd pollution detected across 5.0 s observation window).  
  *Candidate SHA-256:* `aa315aa6fcf378877bc9910d65ffc4fca240f92b772b1d3d63bb70d9e2b1a8d1`
- **Condition (c) Naive / Wrong:** Anchors `ui_loc.DB_PATH`, but leaves `Database.__init__` unanchored. `BASELINE_FAIL` (fails unanchored cwd check).  
  *Candidate SHA-256:* `074bcda318eec7bf29606888ee27e69c6cfaf140787a71fcce30c1be79b76eeb`
- **Sensitivity Verdict:** **VERIFIED**.

### 15. TC-REG-CAD-EXPORT-VS-SCREENSHOT
- **Defect Identifier:** DEF-09 (Harness Reliability)
- **Mechanism:** Verifies native OCC offscreen 3D CAD rendering produces non-uniform opaque images without UI interaction.
- **Condition (a) Baseline:** `PASS` (native OCC renders 3D bridge model: standard deviation = 66.6, 3 distinct colors).
- **Condition (b) Minimal Correct:** Baseline behavior verified. `PASS`.  
  *Candidate SHA-256:* `0fc060d40e1bc07908b8b049d592476d06cfd38865f12e84e51bfd497c65cb07`
- **Condition (c) Naive / Wrong:** Mutates exporter to produce a blank uniform image (std = 0.0). `BASELINE_FAIL` (image rejected as uniform blank screenshot).  
  *Candidate SHA-256:* `f65c52c1e4c76b92a2a0ebae682701e855ae2be579c8cebf009d66144e138a37`
- **Sensitivity Verdict:** **VERIFIED**.

---

## 3. Cryptographic Provenance & Exit Codes

```
Baseline Run Exit Code:    0 (Recorded to testing/evidence/phase_2_10/baseline/baseline_exit_code.txt)
Sensitivity Run Exit Code: 0 (Recorded to testing/evidence/phase_2_10/sensitivity/sensitivity_exit_code.txt)
Post-Manifest Verification: SUCCESS (0 file drift across all directories)
```

**Provenance Hash Manifest:**
- `evidence_guard.py` SHA-256: `7823e2dc920155b9ffdfa3648a14ecb37f84a441e88e22700e12ea99d52528b7`
- `run_all_baseline_tests.py` SHA-256: `c830eb87e8e77a0c86807d4b4a1c52b2f6ef3f70624ce8c7a6e1df639c0fa370`
- `run_sensitivity_matrix.py` SHA-256: `ad121b6d91daecf89ae3298ecf0d959ca99be44c06e23ca6e8a4a58438b4d8ec`
