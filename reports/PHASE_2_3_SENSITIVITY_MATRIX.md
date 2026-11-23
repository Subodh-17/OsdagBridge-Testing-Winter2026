# Phase 2.3 Sensitivity Matrix & Candidate Implementation Audit Report

**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`)  
**Environment:** `osdagbridge-py312` (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | Python 3.12.16)  
**Execution Timestamp:** 2026-11-16T14:23:19 UTC  
**Total Run Duration:** 58.90 seconds  
**Actionable Verification Rate:** **12 / 12 (100.0%)**  
**Formal Blockers:** 2 / 14 (`TC-REG-D02` pending DEC-015, `TC-REG-GEO-SLAB` pending DEC-013)  
**Overall Actionable Gate Status:** **PASSED**  

---

## 1. Executive Protocol & History Disclosure

### 1.1 Strict Candidate-Validation Protocol (Phase 2.2 Audit §11)
The sensitivity matrix enforces a rigorous 3-condition diagnostic verification for every test:
- **Condition (a) — Frozen Baseline:** The test runs against untouched baseline code. It must reproduce the genuine defect (`BASELINE_FAIL`) or confirm environmental setup (`PASS` for CAD).
- **Condition (b) — Minimal Correct Candidate:** The test runs against a candidate implementation that modifies the upstream structural model, section definition, or finite element solver assembly *prior to solution*. It must pass the test (`PASS`) by satisfying genuine physics and engineering standards.
- **Condition (c) — Plausible Naive / Flawed Candidate:** The test runs against an incomplete, naive, or superficial patch. The test must reject this candidate (`BASELINE_FAIL` or `FAIL`), proving that the test cannot be duped by superficial or partial fixes.

### 1.2 Evolution & History Disclosure
In compliance with project QA transparency standards:
- **Phase 2.1 Matrix:** Recorded multiple UNVERIFIED tests due to mock/clamp failures.
- **Phase 2.2 Matrix:** Attempted candidate repairs but was rejected by the independent audit (`PHASE_2_2_FINAL_INDEPENDENT_GATE_AUDIT.md`) due to:
  1. Injected 96 kN median load and `LineLoading.__eq__` monkeypatch in `TC-REG-A02`.
  2. Load case reordering to force BASIC_1 as the final OpenSees state.
  3. Narrow test scopes in C01, C02, RPT, and CAP.
- **Phase 2.3 Re-engineered Matrix:** 
  1. Fully eradicated all synthetic loads (no median load), reordering tricks, and `__eq__` monkeypatches in A02.
  2. Implemented case-specific reaction solve `bgm.model.analyze(load_case=b1_name)`.
  3. Replaced object-identity check with physical force resultant difference: $\Delta R_{\text{barrier}} = 1.35 \times 196.20 = 264.87\text{ kN}$.
  4. Expanded C01 to dual static (0.0 MPa) and cyclic (62.729 MPa) validation with DCR check.
  5. Built authentic 40-tonne 3-axle IRC 6 Cl. 204.6 fatigue vehicle inside carriageway with full OpenSees solution.
  6. Tested 6 full pass/fail scenarios dynamically in RPT across all 4 bridge components.
  7. Multi-geometry IS 800 Cl. 8.7.3.1 / 7.1.2.1 web strip buckling oracle in CAP ($r_y = t_w / \sqrt{12}$).
  8. Preserved D02 and GEO-SLAB as `BLOCKED / NOT DEMONSTRATED` pending formal project decisions (DEC-015, DEC-013).
  9. Partitioned evidence into isolated directories, guaranteeing baseline log immutability.

---

## 2. Complete 14-Test Sensitivity Matrix

| # | Test ID | Defect ID | Condition (a): Baseline | Condition (b): Minimal Correct | Condition (c): Naive / Incomplete | Sensitivity Verdict |
|---|---|---|---|---|---|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | **BASELINE_FAIL**<br>Ratio: 1.00000 | **PASS**<br>Ratio: 1.35000 | **BASELINE_FAIL**<br>Ratio: 1.15000 | **VERIFIED** |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | **BASELINE_FAIL**<br>$\Delta D = 2\text{ mm}$, $\delta = 7.816\text{ mm}$ | **PASS**<br>$D = 1340\text{ mm}$, $\delta = 7.218\text{ mm}$ | **BASELINE_FAIL**<br>Metadata only, $\delta = 7.816\text{ mm}$ | **VERIFIED** |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | **BASELINE_FAIL**<br>Static: Env=125.5, LC=62.7 MPa | **PASS**<br>Static: 0.0; Cyclic: 62.73 MPa | **BASELINE_FAIL**<br>Static Env=0.0, LC=62.73 MPa | **VERIFIED** |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | **BASELINE_FAIL**<br>$R = 1736.55\text{ kN}$, Barrier missing | **PASS**<br>$R = 2710.16\text{ kN}$, $\Delta R_b = 264.87\text{ kN}$ | **BASELINE_FAIL**<br>$R = 2445.29\text{ kN}$, Barrier missing | **VERIFIED** |
| 5 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | **BASELINE_FAIL**<br>$P_z = 463.7\text{ N/m}^2$ (defaults) | **PASS**<br>$P_z = 1039.6\text{ N/m}^2$ (propagated) | **BASELINE_FAIL**<br>$P_z = 940.6\text{ N/m}^2$ (partial) | **VERIFIED** |
| 6 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | **BLOCKED**<br>DEC-015 pending | **BLOCKED**<br>DEC-015 pending | **BLOCKED**<br>DEC-015 pending | **BLOCKED / NOT DEMONSTRATED** |
| 7 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | **BASELINE_FAIL**<br>Fatigue vehicle omitted | **PASS**<br>40t vehicle solved in OpenSees | **BASELINE_FAIL**<br>Mock object without loads/forces | **VERIFIED** |
| 8 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | **BASELINE_FAIL**<br>Unconditional pass string | **PASS**<br>Dynamic derivation (6 scenarios) | **BASELINE_FAIL**<br>Hardcoded fail (fails Scenario 1) | **VERIFIED** |
| 9 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | **BASELINE_FAIL**<br>$n_{\text{girders}} = 6$ (overhangs counted) | **PASS**<br>$n_{\text{girders}} = 4$ (physical count) | **BASELINE_FAIL**<br>$n_{\text{girders}} = 0$ | **VERIFIED** |
| 10 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | **BLOCKED**<br>DEC-013 pending | **BLOCKED**<br>DEC-013 pending | **BLOCKED**<br>DEC-013 pending | **BLOCKED / NOT DEMONSTRATED** |
| 11 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | **BASELINE_FAIL**<br>G1: 214533 kN, G2: 370184 kN | **PASS**<br>G1: 63.4 kN, G2: 158.5 kN | **BASELINE_FAIL**<br>G1: 1918.8 kN, G2: 1909.1 kN | **VERIFIED** |
| 12 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | **BASELINE_FAIL**<br>$R_{SW} = 169.8\text{ kN}$ (78.5 kN/m3) | **PASS**<br>$R_{SW} = 151.4\text{ kN}$ (70.0 kN/m3) | **BASELINE_FAIL**<br>$R_{SW} = 169.8\text{ kN}$ (78.5 kN/m3) | **VERIFIED** |
| 13 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | **BASELINE_FAIL**<br>Package written, cwd side-effect | **PASS**<br>Cleanly anchored to user AppData | **BASELINE_FAIL**<br>UI anchored, constructor in cwd | **VERIFIED** |
| 14 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | **PASS**<br>OCC 8.0.1 offscreen render | **PASS**<br>OCC 8.0.1 offscreen render | **BASELINE_FAIL**<br>Blank uniform image (std=0.0) | **VERIFIED** |

---

## 3. Technical Analysis of Candidate Implementations

### 3.1 TC-REG-A02: ULS Combination Sum & Case-Specific Extraction
- **Candidate (b):** 
  - Fixes upstream `apply_load_factor` for `LineLoading` (scales `line_end_point.p`) and `PatchLoading` (re-executes `_define_patch_edge_lines`).
  - Scales load magnitudes by `load_factor` in `LoadCase.add_load`.
  - In `PlateGirderBridge.add_dead_loads`, invokes `model.create_sidl_combination()` before `model.create_dead_load_combination(partial_safety_factor=1.0)`, bundling the crash barrier load into SIDL and DL.
  - Zero median line load is injected. Zero load case reordering. Zero monkeypatching of `__eq__`.
  - Case-specific solve `bgm.model.analyze(load_case=b1_name)` yields:
    $$R_{\text{BASIC\_1}} = 2710.16\text{ kN} \quad (\text{Target: } 2710.17\text{ kN}, \text{ Error: } 8.4\text{ N})$$
    $$\Delta R_{\text{barrier}} = 2710.16 - (1.35 \times (169.82 + 1314.38) + 1.75 \times 252.36) = 264.87\text{ kN} \quad (\text{Target: } 1.35 \times 196.20 = 264.87\text{ kN})$$
  - Finite element element shear and moment superposition match factored sums within 0.001%. Result: **PASS**.
- **Candidate (c):**
  - Factors self-weight ($1.35\times$) and wearing course ($1.75\times$), but omits the crash barrier load.
  - Reaction reaches only $2445.29\text{ kN}$ (missing 264.87 kN of barrier load). Result: **BASELINE_FAIL**.

### 3.2 TC-REG-C02: IRC 6 Cl. 204.6 Fatigue Vehicle Analysis
- **Candidate (b):**
  - Synthesizes authentic 40-tonne 3-axle vehicle compound load (Axle 1: 117.72 kN, Axle 2: 137.34 kN, Axle 3: 137.34 kN) with 6 wheel point loads spaced transversely at $1.68\text{ m}$ track width.
  - Centerline placed at carriageway center ($z = 4.25\text{ m}$), placing wheel lines at $z = 3.41\text{ m}$ and $z = 5.09\text{ m}$ (strictly inside deck $0.0 \le z \le 8.5\text{ m}$).
  - Adds moving load along bridge length ($x = -10.0\text{ m}$ to $34.0\text{ m}$) and solves in OpenSees, producing non-zero solver response and dynamic forces. Result: **PASS**.
- **Candidate (c):**
  - Appends a `MockFatigueLC` placeholder with empty load array (`loads = []`), mimicking the shallow cheat flagged by the Phase 2.1 audit. The test rejects it due to zero axle weight and zero solver response. Result: **BASELINE_FAIL**.

### 3.3 TC-REG-RPT: Multi-Scenario Executive Summary
- **Candidate (b):**
  - Implements dynamic component evaluation from `output_dict`:
    * Girder: scans `per_girder` check statuses and DCRs.
    * Cross bracing: checks `crossbracing_design_results` member efficiencies ($> 1.0$).
    * End diaphragm: checks `end_diaphragm_design_results` member efficiencies ($> 1.0$).
    * Deck slab: checks `deck_design_results` utilization ratios ($> 1.0$).
  - Evaluates all 6 required scenarios (All pass, Girder fail, Cross-bracing fail, Diaphragm fail, Deck fail, Multi fail). In every scenario, emitted LaTeX accurately reflects the true component outcome. Result: **PASS**.
- **Candidate (c):**
  - Hardcodes `\noindent Girder design fail` under Key Design Outcomes. When Scenario 1 (All Pass) runs, it emits a false failure. Result: **BASELINE_FAIL**.

### 3.4 TC-REG-CAP: Multi-Geometry Web Strip Buckling Oracle
- **Candidate (b):**
  - Implements genuine IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 web strip buckling:
    $$r_{wb} = \frac{t_w}{\sqrt{12}}, \quad \frac{KL}{r_{wb}} = \frac{0.7 d_w}{r_{wb}}, \quad f_{cd} = \text{Column Curve c}$$
    $$F_{cdw} = \frac{f_{cd} \times (b_1 + n_1) t_w}{1000}$$
  - Evaluates both Geometry 1 ($d_w = 1304\text{ mm}, t_w = 8\text{ mm}, b_1 = 101.81\text{ mm} \rightarrow 63.4\text{ kN}$) and Geometry 2 ($d_w = 1000\text{ mm}, t_w = 10\text{ mm}, b_1 = 100.0\text{ mm} \rightarrow 158.5\text{ kN}$), matching hand oracles within 0.1%. Result: **PASS**.
- **Candidate (c):**
  - Uses squash load formula $(f_y / \gamma_{m0}) \times A_{wb} / 1000$, producing $1918.8\text{ kN}$ and $1909.1\text{ kN}$ and completely ignoring web slenderness buckling. Result: **BASELINE_FAIL**.

---

## 4. Verification Rate & Gate Status

- **Actionable Tests Total:** 12
- **Actionable Tests Verified:** **12 (100.0%)**
- **Blocked Architectural Tests:** 2 (`TC-REG-D02`, `TC-REG-GEO-SLAB`)
- **Process Exit Code:** `0`
- **Overall Sensitivity Status:** **PASSED**
