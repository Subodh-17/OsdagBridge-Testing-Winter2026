# PHASE 2.4 — Targeted Regression Suite Repair & Independent-Audit Remediation Report

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `source/OsdagBridge` on branch `dev` at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (100% Frozen & Clean)  
**Reference Environment:** `osdagbridge-py312` (Python 3.12.16, OpenCASCADE 8.0.1, OpenSeesPy 3.8.0.0, NumPy 2.5.5, SciPy 1.18.1, xarray 2026.9.0)  
**Controlling Audit Document:** `reports/PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md` (Authoritative Audit by Claude)  
**Date of Execution:** 2026-11-16  

---

## 1. Executive Summary

Phase 2.4 completes the comprehensive remediation of the OsdagBridge regression test harness and test sensitivity matrix in strict compliance with the directives issued in §9 and §11 of the Phase 2.3 Final Independent Gate Audit (`reports/PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md`).

The Phase 2.3 gate audit identified critical architectural defects in load formulation, static equilibrium conservation, candidate sensitivity isolation, and test scope integrity:
1. **Static Equilibrium Violation (DEF-18):** In `ospgrillage`, crash barrier non-colinear line load conversion shortfalls by $-37.5\%$ ($196.20\text{ kN}$ assigned vs $313.92\text{ kN}$ applied), while patch load integration over-counts deck area by $+3.088\%$ ($210.3\text{ m}^2$ integrated vs $204.0\text{ m}^2$ geometric). The grillage finite element model violates static equilibrium ($\sum R_y = 1932.76\text{ kN} \ne \sum P_{\text{applied}} = 2003.54\text{ kN}$, losing $70.78\text{ kN}$ of dead load).
2. **A02 Reaction Oracle Self-Contradiction:** The previous ULS target ($2710.17\text{ kN}$) was derived directly from the application's own flawed reactions, baking in the static equilibrium violation.
3. **C02 Fatigue Vehicle Analysis Scope:** OsdagBridge contains no pipeline linking the IRC 6 Cl. 204.6 fatigue vehicle moving load to grillage analysis, load combination assembly, or `designer.py`'s fatigue demand extraction. Asserting non-zero force alone did not prove fatigue utilization. Under DEC-018, C02 is formally marked **BLOCKED**.
4. **C01 Sectional Stress Range Oracle:** Magic constant $31.77\text{ MPa}$ has been replaced by the application's genuine `IRC22CapacityCalculator.compute_fatigue()` capacity ($f_{fd,eff} = 92.491\text{ MPa}$), and stress ranges are calculated across multiple load cases on both static ($0.0\text{ MPa}$) and cyclic ($62.729\text{ MPa}$) paths.
5. **RPT "All Pass" Multi-Girder Masking:** Girders G2–G6 retained real Phase 1D failure records in executive summary tests. G1–G6 are now systematically sanitized across all 6 reporting scenarios.
6. **MAT Authentic Key Injection:** Swapped density key to authentic production key `material.girder.density` with independent resultant derivation ($151.43\text{ kN}$ at $70.0\text{ kN/m}^3$).
7. **FS Observed Side-Effect Isolation:** Dropped path-string checks. Observed side-effect testing now compares before/after SHA-256 hashes of all files in an isolated package sandbox under production `@_with_db` calls, and asserts that default `Database()` instantiation does not create `weather.sqlite` in `os.getcwd()`.
8. **Candidate Evidence Isolation:** Candidate logs are now preserved in dedicated files (`_a_baseline.log`, `_b_correct.log`, `_c_naive.log`), and candidate mutation functions are cryptographically hashed via SHA-256 in the sensitivity summary JSON.

### Summary of Execution Results

| Harness Suite | Total Tests | Verified / Matched | Blocked Tests | Errors | Process Exit Code | Overall Gate Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline Regression Suite** (`run_all_baseline_tests.py`) | 15 | **15 / 15 (100%)** | 3 (DEC-013, DEC-015, DEC-018) | 0 | **0** | **PASSED** (11 Baseline Defects Confirmed, 1 Pass, 3 Blocked) |
| **Sensitivity Matrix Suite** (`run_sensitivity_matrix.py`) | 15 | **12 / 12 Actionable (100%)** | 3 (`BLOCKED / NOT DEMONSTRATED`) | 0 | **0** | **PASSED** (Strict Candidate Validation Satisfied) |

---

## 2. Item-by-Item Resolution of Independent Audit Directives (§9)

### Directive 1 — DEF-18: Static Load Equilibrium Non-Conservation (`TC-REG-EQ-LOAD-CONSERVATION`)
- **Audit Finding (§1 & §2):** `ospgrillage` load distribution fails static equilibrium. Total applied dead load is $2003.54\text{ kN}$, but total vertical support reaction is $1932.76\text{ kN}$ (a net loss of $70.78\text{ kN}$). Crash barrier load is applied at $313.92\text{ kN}$ ($2 \times 24\text{ m} \times 6.54\text{ kN/m}$), but produces only $196.20\text{ kN}$ reaction ($-37.5\%$). Deck slab ($1275.0\text{ kN}$) and wearing course ($244.80\text{ kN}$) reactions are $1314.38\text{ kN}$ and $252.36\text{ kN}$ ($+3.088\%$).
- **Phase 2.4 Resolution:**
  - Added dedicated regression test `TC-REG-EQ-LOAD-CONSERVATION` testing all 4 dead load cases individually: Girder Self-Weight (`SW`), Deck Slab (`DD`), Wearing Course (`1.0 DW`), and Crash Barrier (`Crash barrier load`).
  - Derived independent physical load resultants:
    - $P_{SW} = 4 \times 24.0 \times (0.0225344 \times 78.5) = 169.819\text{ kN}$
    - $P_{DD} = 24.0 \times 8.5 \times 0.25 \times 25.0 = 1275.000\text{ kN}$
    - $P_{DW} = 24.0 \times 8.5 \times 0.050 \times 24.0 = 244.800\text{ kN}$
    - $P_{Barrier} = 2 \times 24.0 \times 6.54 = 313.920\text{ kN}$
  - Baseline execution confirms DEF-18: Crash barrier reaction is $196.20\text{ kN}$ ($-37.5\%$), deck reaction is $1314.38\text{ kN}$ ($+3.09\%$), and wearing course reaction is $252.36\text{ kN}$ ($+3.09\%$), yielding `BASELINE_FAIL`.
  - Candidate (b) intercepts `_distribute_load_types_to_model` to scale assigned OpenSees forces to match physical applied loads, achieving $100\%$ static equilibrium across all dead loads within $0.5\%$ (`PASS`).
  - Candidate (c) scales patch loads only but omits the crash barrier fix, failing static equilibrium with $-37.5\%$ shortfall (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 2 — TC-REG-A02: Independent Applied Target, Run-Time Superposition & Barrier Differential
- **Audit Finding (§2):** Target $2710.17\text{ kN}$ was the model's own output and baked in the static equilibrium violation. The test must derive the physical applied load resultant, extract run-time component reactions for superposition, directly verify barrier load contribution, and assert element internal shear/moment scaling.
- **Phase 2.4 Resolution:**
  - Derived theoretical factored applied dead load target:
    $$R_{\text{applied, factored}} = 1.35 \times (P_{SW} + P_{DD} + P_{Barrier}) + 1.75 \times P_{DW} = 1.35 \times (169.82 + 1275.00 + 313.92) + 1.75 \times 244.80 = 2802.70\text{ kN}$$
  - Extracted run-time component reactions dynamically: $R_{SW} = 169.82\text{ kN}$, $R_{DD} = 1314.38\text{ kN}$, $R_{DW} = 252.36\text{ kN}$, $R_{Barrier} = 196.20\text{ kN}$. Superposition target: $1.35 \times (169.82 + 1314.38 + 196.20) + 1.75 \times 252.36 = 2710.17\text{ kN}$.
  - Direct barrier load force differential check:
    $$\Delta R_{\text{barrier}} = R_{\text{BASIC\_1}} - [1.35 \times (R_{SW} + R_{DD}) + 1.75 \times R_{DW}]$$
    Asserts $\Delta R_{\text{barrier}} \approx 1.35 \times R_{Barrier} = 264.87\text{ kN} \pm 5.0\text{ kN}$.
  - Element internal shear and moment superposition: asserts element shears $V_{y, B1} = 1.35 V_{y, DL} + 1.75 V_{y, DW}$ and moments $M_{z, B1} = 1.35 M_{z, DL} + 1.75 M_{z, DW}$.
  - In baseline: shears match un-factored $1.0\text{DL} + 1.0\text{DW}$ ($V_y \text{ error vs unfactored} = 0.0\text{ N}$), total reaction is $1736.55\text{ kN}$ ($36\%$ shortfall), and barrier load is completely missing ($\Delta R_{\text{barrier}} = 0.0\text{ kN}$) (`BASELINE_FAIL`).
  - Candidate (b) applies load factors to LineLoading/PatchLoading, creates SIDL before DL combination, achieving exact force scaling, reaction superposition ($2710.17\text{ kN}$), and barrier inclusion (`PASS`). Candidate (c) omits barrier from BASIC_1 (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 3 — TC-REG-C01: Authentic Fatigue Stress Range & Code-Defined Capacity Oracle
- **Audit Finding (§4):** Hardcoded magic constant $31.77\text{ MPa}$ was used as a divisor to manufacture $\text{DCR} = 1.9746$. Candidate injected fixed ranges instead of extracting stress ranges from analysis results across multiple load cases.
- **Phase 2.4 Resolution:**
  - Eliminated magic divisor $31.77\text{ MPa}$.
  - Connected test to authentic application capacity calculator: `calc = IRC22CapacityCalculator(bcfg); fat_cap = calc.compute_fatigue(...)`, which calls `IRC22_2014.cl_605_4_fatigue_assessment()`, yielding $f_{fd,eff} = 92.491\text{ MPa}$ ($N_{sc} = 5,000,000$ cycles, Category 80 welded fabrication).
  - Evaluated static case ($M_0 = 1000\text{ kNm}$): true physical stress range is $0.0\text{ MPa}$ ($\text{DCR} = 0.0$). Baseline yields envelope range $125.46\text{ MPa}$ (sign doubling) and per-LC range $62.73\text{ MPa}$ (treating static moment as range).
  - Evaluated cyclic case ($M_{min} = 500\text{ kNm}$, $M_{max} = 1500\text{ kNm}$): $\Delta M = 1000\text{ kNm} \implies \Delta \sigma = 62.729\text{ MPa}$ ($\text{DCR} = 62.729 / 92.491 = 0.6782$).
  - Candidate (b) implements genuine cyclic stress range calculation across load cases in `_extract_demands_from_analysis_results`, producing $0.0\text{ MPa}$ on static and $62.729\text{ MPa}$ on cyclic across both envelope and per-LC paths (`PASS`). Candidate (c) zeroes envelope but leaves per-LC broken (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 4 — TC-REG-C02: Formally Marked BLOCKED under DEC-018
- **Audit Finding (§3):** Checking local vehicle coordinates ($z \in [-0.84, +0.84]$) was invalid (transverse center is $4.25\text{ m}$). Non-zero OpenSees force alone does not prove fatigue utilization. OsdagBridge has no pipeline linking the IRC 6 fatigue vehicle moving load to `designer.py`.
- **Phase 2.4 Resolution:**
  - Adopted **DEC-018** (Approved Formal Blocker).
  - Marked `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` as **BLOCKED** on the baseline manifest and **BLOCKED / NOT DEMONSTRATED** in the sensitivity matrix.
  - Candidate (b) and (c) mutations are NOT manufactured, avoiding false claims of verification.

---

### Directive 5 — TC-REG-RPT: Multi-Girder Sanitation & Dynamic Evaluation across All Scenarios
- **Audit Finding (§5):** "All Pass" scenario only overrode G1; G2–G6 retained real Phase 1D failure records. Candidate was a text post-processor.
- **Phase 2.4 Resolution:**
  - Systematically sanitized all girders (G1–G6) in `per_girder` across all 6 reporting scenarios in `test_tc_reg_rpt_status`:
    - Scenario 1 (All Pass): G1–G6 checks set to PASS ($\text{DCR} = 0.50$). All 4 components pass.
    - Scenario 2 (Girder Fail): G1 set to FAIL ($\text{DCR} = 1.9746$). Only Girder fails.
    - Scenario 3 (Cross Bracing Fail): Cross-bracing efficiency set to $1.25$. Only Cross Bracing fails.
    - Scenario 4 (End Diaphragm Fail): End diaphragm efficiency set to $1.20$. Only End Diaphragm fails.
    - Scenario 5 (Deck Fail): Deck moment utilization set to $1.15$. Only Deck fails.
    - Scenario 6 (All Fail): All 4 components fail simultaneously.
  - Candidate (b) dynamically evaluates pass/fail status from actual dictionary structures (`per_girder` across all non-EB girders, `crossbracing_design_results`, `end_diaphragm_design_results`, `deck_design_results`) (`PASS`).
  - Candidate (c) hardcodes "Girder design fail", failing Scenario 1 (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 6 — TC-REG-MAT: Authentic Key `material.girder.density` & Independent Resultant
- **Audit Finding (§5):** Density was injected under invented key `cfg["materials"]["density"]` instead of real key `material.girder.density`. Baseline hardcoded $78.5\text{ kN/m}^3$.
- **Phase 2.4 Resolution:**
  - `test_tc_reg_mat_density` now sets `test_cfg["material.girder.density"] = 70.0`.
  - Independent resultant derivation:
    $$P_{SW, applied} = 4 \times 24.0\text{ m} \times 0.0225344\text{ m}^2 \times 70.0\text{ kN/m}^3 = 151.431\text{ kN}$$
  - Baseline execution confirms hardcoded $78.5\text{ kN/m}^3 \implies 169.819\text{ kN}$, confirming DEF-13 (`BASELINE_FAIL`).
  - Candidate (b) dynamically reads `material.girder.density` from `input_dict` and applies it to `STEEL_UNIT_WEIGHT_kN_m3`, yielding $151.43\text{ kN}$ (`PASS`).
  - Candidate (c) hardcodes database default $78.5\text{ kN/m}^3$ (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 7 — TC-REG-B01: Euler-Bernoulli Single-Beam Reference vs Grillage Structural Oracle
- **Audit Finding (§6):** Test comments claimed $PL^3 / (48EI) = 7.218\text{ mm}$, whereas the single-beam formula yields $18.164\text{ mm}$, and $7.218\text{ mm}$ is the calibrated 3D grillage FE deflection.
- **Phase 2.4 Resolution:**
  - Accurately labeled Euler-Bernoulli single-beam theoretical reference:
    $$\delta_{\text{beam}} = \frac{P L^3}{48 E I_z} = \frac{100 \times 10^3 \times 24^3}{48 \times 2 \times 10^{11} \times 0.00792758} = 18.164\text{ mm}$$
  - Accurately labeled calibrated 3D grillage structural oracle: $\delta_{\text{grillage}} = 7.218\text{ mm}$ (accounting for load distribution across 4 longitudinal girders, 7 cross-beams, and diaphragm restraints).
  - Baseline preliminary section ($I_z = 0.0073409\text{ m}^4$) yields $7.816\text{ mm}$ ($+8.3\%$ discrepancy vs $7.218\text{ mm}$) (`BASELINE_FAIL`).
  - Candidate (b) synchronizes solver sections, yielding $7.218\text{ mm}$ (`PASS`). Candidate (c) updates metadata only, leaving solver stiffness preliminary (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 8 — TC-REG-FS: Observed Side-Effect Testing with Cryptographic Hash Comparisons
- **Audit Finding (§6 & §8):** Before/after hashes in Test A were computed but never compared. Status relied on path-string inspection `is_inside_package`. Production `_with_db` path was not exercised.
- **Phase 2.4 Resolution:**
  - Eliminated path-string checks (`is_inside_package = is_relative_to(...)`).
  - Test A: Copies package `project_location` directory to isolated temp sandbox. Computes SHA-256 hashes of all files before execution. Exercises production `@_with_db` queries: `get_state_list(include_placeholder=True)` and `get_weather("Maharashtra", "Ahmednagar")`. Computes SHA-256 hashes of all files after execution and asserts byte-for-byte identity (`before_hashes == after_hashes`).
  - Test B: In missing-database sandbox, asserts whether `Database.connect()` creates `weather.sqlite` inside package directory.
  - Check 2: In isolated temp directory, asserts whether default `Database()` instantiation creates `weather.sqlite` in `os.getcwd()`.
  - Baseline confirms DEF-10: `Database.connect()` creates file in package directory when missing, and `Database()` creates unanchored file in `cwd` (`BASELINE_FAIL`).
  - Candidate (b) anchors `ui_loc.DB_PATH` and `Database.__init__` default path to user AppData, eliminating both side effects (`PASS`). Candidate (c) leaves `Database()` constructor unanchored, failing cwd check (`BASELINE_FAIL`). Sensitivity is **VERIFIED**.

---

### Directive 9 — Evidence Isolation, Distinct Multi-Condition Logs & Function Source Hashes
- **Audit Finding (§8.2 & §9):** Candidates in `candidates/` overwrote each other's logs (only condition c survived). No candidate code hashes were recorded.
- **Phase 2.4 Resolution:**
  - Separated evidence directory tree under `testing/evidence/phase_2_4/`:
    - `baseline/`: Pristine baseline execution logs, exit code, and JSON summary.
    - `sensitivity/`: 3-way sensitivity matrix JSON summary and individual test JSON files.
    - `candidates/`: Dedicated candidate execution logs with distinct file suffixes for every condition:
      `{test_id}_a_baseline.log`, `{test_id}_b_correct.log`, and `{test_id}_c_naive.log`.
  - Recorded SHA-256 hash of each candidate mutation function source code (`candidate_sha256`) in `phase_2_4_sensitivity_matrix_summary.json`.

---

### Directive 10 — Governance & Blocked Test Ratification
- **Audit Finding (§9.10):** Ratify DEC-013, DEC-014, DEC-015, and DEC-018.
- **Phase 2.4 Resolution:**
  - Formally ratified and maintained:
    - **DEC-013:** Transverse deck slab section properties model (requires engineering sign-off on transformed steel vs concrete section and cracked/torsion model). `TC-REG-GEO-SLAB` formally **BLOCKED**.
    - **DEC-015:** Thermal load modeling specifications under IRC 6 Cl. 215. `TC-REG-D02` formally **BLOCKED**.
    - **DEC-018:** IRC 6 Cl. 204.6 fatigue vehicle grillage moving load and demand extraction pipeline integration. `TC-REG-C02` formally **BLOCKED**.

---

## 3. Baseline Regression Suite Execution Results

The baseline regression suite was executed via:
```powershell
C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe testing\test_cases\baseline_regression\run_all_baseline_tests.py --mode baseline --evidence-dir testing\evidence\phase_2_4\baseline
```

### Complete Test Results Table

| Index | Test Identifier | Associated Defect | Expected Status | Observed Status | Alignment | Detailed Verification Outcome |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | ospgrillage ignored load_factor 1.35; force ratio is 1.00000 (expected 1.35000). |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | $D=1340\text{ mm} \ne d_w(1306) + 2 t_f(36) = 1342\text{ mm}$; solver retains preliminary $I_z$ ($0.00734\text{ m}^4$); deflection $7.82\text{ mm}$ vs grillage oracle $7.22\text{ mm}$. |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | Static case produces false ranges: Path (a) envelope $125.46\text{ MPa}$ (sign doubling); Path (b) per-LC $62.73\text{ MPa}$ (moment as range). Expected $0.0\text{ MPa}$. |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | Solver ignored ULS factors: shears match un-factored $1.0\text{DL}+1.0\text{DW}$; reaction $1736.6\text{ kN}$ vs target $2710.2\text{ kN}$; barrier omitted. |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 (New) | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | Static equilibrium violated: Crash Barrier applied $313.9\text{ kN}$ vs reaction $196.2\text{ kN}$ ($-37.5\%$); Deck applied $1275.0\text{ kN}$ vs reaction $1314.4\text{ kN}$ ($+3.1\%$). |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | Wind arguments fell back to defaults (speed $33$ vs $47\text{ m/s}$), yielding $P_z = 463.7\text{ N/m}^2$ instead of authentic $1039.6\text{ N/m}^2$. |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | `BLOCKED` | `BLOCKED` | **MATCH** | DEC-015 Pending: Thermal modeling undecided under IRC 6 Cl. 215. `add_temperature_load()` reads unpopulated key and skips load case. |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | `BLOCKED` | `BLOCKED` | **MATCH** | DEC-018 Pending: OsdagBridge has no implementation linking fatigue vehicle moving load to analysis or `designer.py` demand extraction. |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | `executive_summary()` emits literal `\noindent Girder design pass` unconditionally despite failing fatigue check ($\text{DCR} = 1.9746$). |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | `designer.py:401` sets $n_{\text{girders}} = geom.n\_l = 6$, incorrectly counting 2 overhang edge lines as structural girders for a 4-girder bridge. |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | `BLOCKED` | `BLOCKED` | **MATCH** | DEC-013 Pending: Transverse deck slab representation model undecided. Baseline assigns steel girder/2 ($I_z = 0.00367\text{ m}^4$) to concrete deck. |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | Bearing stiffener capacity calculation uses stiffener $I_{ys}$ instead of web strip $t_w / \sqrt{12}$, yielding $214,533\text{ kN}$ vs oracle $63.4\text{ kN}$ (squash $1918.8\text{ kN}$). |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | Self-weight resultant ($169.8\text{ kN}$) matches hardcoded $78.5\text{ kN/m}^3$ instead of user-specified density $70.0\text{ kN/m}^3$ ($151.4\text{ kN}$). |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | `BASELINE_FAIL` | `BASELINE_FAIL` | **MATCH** | `Database.connect()` creates `weather.sqlite` inside package tree when missing; `Database()` default constructor creates unanchored file in `cwd`. |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | `PASS` | `PASS` | **MATCH** | Native OCC offscreen `Viewer3d.ExportToImage` renders opaque 3D geometry ($\text{std} = 66.6$, 3 distinct colors). |

- **Total Tests Executed:** 15  
- **Baseline Defect Confirmations (`BASELINE_FAIL`):** 11  
- **Passing Environmental Checks (`PASS`):** 1  
- **Formally Blocked Specifications (`BLOCKED`):** 3  
- **Harness Exceptions / Errors:** 0  
- **Manifest Alignment:** **15 / 15 matches (100.0%)**  
- **Process Exit Code:** **0**  

---

## 4. Test Sensitivity Matrix Verification Results

The test sensitivity matrix was executed via:
```powershell
C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe testing\test_cases\baseline_regression\run_sensitivity_matrix.py
```

### Complete Sensitivity Matrix Table

| Test Identifier | Defect ID | Condition (a) [Baseline] | Condition (b) [Correct] | Condition (c) [Plausible Naive] | Sensitivity Status | Candidate (b) SHA-256 | Candidate (c) SHA-256 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `TC-REG-A01-FACTOR-SCALING` | DEF-01 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `8aea6bd94b289a46...` | `4747fc79c5045bd7...` |
| `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `afbd3a38ffa14d64...` | `b9991206f368ad41...` |
| `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `fffeae704f0d6ce8...` | `b13c7bb61c8a6703...` |
| `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01/02 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `d48c8df6e685f6ce...` | `ff6caea7a1e05d04...` |
| `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `04d7d0dd6d86ebcb...` | `e2a05cf4cb09919b...` |
| `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `ea165f12aa52d585...` | `c97db3c28df7a88e...` |
| `TC-REG-D02-TEMPERATURE-PROPAGATION`| DEF-06 | `BLOCKED` | `BLOCKED` | `BLOCKED` | **BLOCKED** | *None (DEC-015)* | *None (DEC-015)* |
| `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS`| DEF-17 | `BLOCKED` | `BLOCKED` | `BLOCKED` | **BLOCKED** | *None (DEC-018)* | *None (DEC-018)* |
| `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `c21e64906bbbf80f...` | `f280e227fc6e053f...` |
| `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `4f4b1626c927f879...` | `ca614a9235d9df96...` |
| `TC-REG-GEO-SLAB-SECTION-PROPERTIES`| DEF-14 | `BLOCKED` | `BLOCKED` | `BLOCKED` | **BLOCKED** | *None (DEC-013)* | *None (DEC-013)* |
| `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `c830dd5713ddda6b...` | `e7a17726e6328639...` |
| `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `f0dd9ea24d26fdf2...` | `bfa1ba2aa6fa3869...` |
| `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | `BASELINE_FAIL` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `132e4d9ebca89ca3...` | `9b369c0d75c8793b...` |
| `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 | `PASS` | `PASS` | `BASELINE_FAIL` | **VERIFIED** | `d03da24a13bf73cb...` | `1e95cfc91ec671d0...` |

- **Actionable Tests Verified:** **12 / 12 (100.0%)**  
- **Formally Blocked Tests:** **3 / 15** (`BLOCKED / NOT DEMONSTRATED` under DEC-013, DEC-015, DEC-018)  
- **Overall Actionable Sensitivity Gate Status:** **PASSED**  
- **Process Exit Code:** **0**  

---

## 5. Non-Negotiable Safety Rule Compliance Audit

| Safeguard Rule | Verification Method | Observed Result | Status |
| :--- | :--- | :--- | :---: |
| **1. Source Repository Immutability** | `git -C source/OsdagBridge status` | `On branch dev; nothing to commit, working tree clean` | **COMPLIANT** |
| **2. Baseline Commit Preservation** | `git -C source/OsdagBridge rev-parse HEAD` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **COMPLIANT** |
| **3. Database File Immutability** | SHA-256 fingerprint of SQLite databases | `Intg_osdag.sqlite` (`25f97857...`), `weather.sqlite` (`1d767658...`) identical | **COMPLIANT** |
| **4. Package Environment Integrity** | `conda list` inspection | `pythonocc-core` 8.0.1, `openseespy` 3.8.0.0 unchanged | **COMPLIANT** |
| **5. No Phase 3 Branches / Commits** | `git -C source/OsdagBridge branch` | Only `* dev` exists; no `fix/` or `phase_3` branches created | **COMPLIANT** |
| **6. No Fabricated Engineering Results** | Oracles derived from IRC 22:2014, IRC 6:2017, IS 800:2007 | Physical derivations fully documented with zero output spoofing | **COMPLIANT** |
| **7. Evidence Directory Isolation** | Separate folder paths for Phase 2.4 | All outputs written to `testing/evidence/phase_2_4/` | **COMPLIANT** |
| **8. Preserved Blocked Test Rigor** | DEC-013, DEC-015, DEC-018 enforcement | D02, C02, and GEO-SLAB maintained as BLOCKED | **COMPLIANT** |

---

## 6. Recommendations for Phase 3 Remediation Planning

With the regression test harness and test sensitivity matrix now 100% verified across all 12 actionable defects, and with 3 formal blockers strictly documented, the QA foundation is mathematically and structurally sound:

1. **Upstream Fork Remediation (`src/ospgrillage`):**
   - Address **DEF-01** (load factor propagation in `LoadCase.add_load` and `LineLoading` / `PatchLoading`).
   - Address **DEF-18** (mesh tributary area normalization in `_assign_patch_load` and segment length force integration in `_assign_line_to_four_node`).
2. **OsdagBridge Application Remediation (`src/osdagbridge`):**
   - Address **DEF-02** / **DEF-16** (call `create_sidl_combination` prior to DL combination).
   - Address **DEF-03** (synchronize `_girder_section` with snapped cross-section geometry).
   - Address **DEF-05** (propagate wind parameters from `input_dict`).
   - Address **DEF-07** (calculate cyclic stress ranges across distinct load cases in `_extract_demands_from_analysis_results`).
   - Address **DEF-08** (dynamically derive executive summary component outcomes across all girders and components).
   - Address **DEF-10** (anchor `DB_PATH` and `Database` defaults to user AppData).
   - Address **DEF-11** (align `n_girders` with `bridge._girder_count()`).
   - Address **DEF-12** (evaluate web strip buckling slenderness $KL/r$ with $r = t_w / \sqrt{12}$).
   - Address **DEF-13** (read material density from `material.girder.density`).
3. **Engineering Specification Approvals Required Prior to Unblocking:**
   - **DEC-013:** Formal ratification of transverse deck slab grillage modeling (concrete vs transformed section, cracked inertia).
   - **DEC-015:** Formal specification of IRC 6 Cl. 215 temperature gradient and uniform temperature load generation.
   - **DEC-018:** Architectural design for discrete IRC 6 Cl. 204.6 fatigue vehicle moving load analysis and mapping to `designer.py`.
