# PHASE 3 BATCH 3 — INDEPENDENT CHALLENGE AUDIT (DEF-01 PROPOSAL)
**Adversarial Technical Verification of Candidate Selection, Architecture, Factor Semantics & Numerical Oracles**

**Document ID:** P3-B3-CA-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation (Batch 3 Selection & Prioritization)  
**Proposed Candidate:** DEF-01 (Load Factor Scaling Omission in `ospgrillage` Load Combinations)  
**Auditor:** Independent Engineering Verification Auditor (Claude / Verification Harness)  
**Date:** 19 November 2026  
**Audited Branch:** `fix/phase-3-engineering-remediation`  
**Current HEAD:** `9e0b5883a247c8c0fb74b0890915600c7ab4a896`  
**Baseline Anchor:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`)  
**Authorization Status:** BATCH 3 IS STRICTLY UNAUTHORIZED — PROPOSAL AUDIT ONLY  
**Final Audit Verdict:** **CONDITIONALLY READY**

---

## 1. Audit Scope & Inspected Evidence

### 1.1 Mandate & Adversarial Posture
This independent challenge audit evaluates the selection, prioritization, architectural justification, and proposed scope for **Phase 3 Batch 3 (DEF-01)**. In accordance with the project instructions, the auditor adopts an adversarial posture: the objective is not to validate Antigravity's conclusions, but to actively attempt to falsify them, challenge architectural assumptions, recalculate scoring matrices, trace factor semantics end-to-end through the code, and test the robustness of proposed numerical oracles.

### 1.2 Inspection Protocol & Read-Only Invariant
The audit was performed under strict read-only constraints:
- Verified working tree cleanliness: `nothing to commit, working tree clean`.
- Verified commit HEAD: `9e0b5883a247c8c0fb74b0890915600c7ab4a896` on branch `fix/phase-3-engineering-remediation`.
- Zero application code, test fixtures, or planning documents were modified during this audit.
- No git commits, pushes, merges, or branch switches were executed.

### 1.3 Inspected Documents & Artifacts
1. **Batch 3 Selection Reconnaissance Dossier:**
   - [BATCH_3_CANDIDATE_INVENTORY.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_CANDIDATE_INVENTORY.md) (`P3-B3-INV-001`)
   - [BATCH_3_DEFECT_PRIORITIZATION.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_DEFECT_PRIORITIZATION.md) (`P3-B3-PRI-001`)
   - [BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md) (`P3-B3-PROP-001`)
   - [BATCH_3_SELECTION_MANIFEST.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_SELECTION_MANIFEST.md) (`P3-B3-MAN-001`)
2. **Prior Batch Governance & Closure Records:**
   - [PHASE_3_BATCH_1_CLOSURE_REPORT.md](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_BATCH_1_CLOSURE_REPORT.md) (`P3-CR-001`)
   - [PHASE_3_BATCH_2_CLOSURE_RECORD.md](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_BATCH_2_CLOSURE_RECORD.md) (`P3-CR-002`)
   - [PHASE_3_BATCH_2_INDEPENDENT_AUDIT.md](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_BATCH_2_INDEPENDENT_AUDIT.md) (`P3-IA-002`)
3. **Application Source Modules & Call Paths:**
   - `src/ospgrillage/load.py` (lines 518–570, 1017–1060, 1140–1200)
   - `src/ospgrillage/osp_grillage.py` (lines 1940–2080, 2170–2250, 2370–2550, 2875–2975)
   - `src/osdagbridge/core/bridge_types/plate_girder/analyser.py` (lines 420–440, 580–590, 985–1045, 1515–1560, 1820–1850, 2080–2120, 2340–2415, 2530–2600)
   - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` (lines 1330–1345, 2115–2125, 3220–3235)
4. **Existing Regression Fixtures & Baseline Evidence:**
   - `testing/test_cases/baseline_regression/run_all_baseline_tests.py` (lines 251–326, `test_tc_reg_a01`)
   - `testing/evidence/phase_2_13/baseline/tc_reg_a01_factor_scaling.log`

---

## 2. Independent Architecture Trace

To rigorously establish where load factors are created, stored, transformed, ignored, or evaluated, the auditor traced all factor pathways from user input to finite-element reaction extraction.

```
+---------------------------------------------------------------------------------------------------------+
|                                    OsdagBridge Load Architecture Trace                                  |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  1. Load Object Creation                                                                                |
|     line_load = og.create_load(loadtype="line", point1=p1, point2=p2)                                   |
|     (Raw geometric intensities stored in LoadVertex namedtuples; p has units N, N/m, or N/m²)          |
|                                         |                                                               |
|                                         v                                                               |
|  2. Load Added to LoadCase                                                                              |
|     lc.add_load(line_load, load_factor=gamma_i)           [load.py:1161-1168]                            |
|     --> Stored in lc.load_groups:                                                                       |
|         load_dict = {"load": deepcopy(line_load), "factor": gamma_i}                                    |
|                                         |                                                               |
|                                         v                                                               |
|  3. LoadCase Added to Model                                                                             |
|     model.add_load_case(lc, load_factor=gamma_case)      [osp_grillage.py:2046-2070]                    |
|     |                                                                                                   |
|     +---> A. Discretization Compilation:                                                                |
|     |        load_str = _distribute_load_types_to_model(lc)   [osp_grillage.py:1952-2042]               |
|     |        *** ARCHITECTURAL CRITICAL FAILURE POINT (DEF-01) ***                                      |
|     |        Loops over lc.load_groups: extracts only load_dict["load"].                                |
|     |        load_dict["factor"] IS COMPLETELY DROPPED AND NEVER PASSED TO ALLOCATION HELPERS.          |
|     |        -> _assign_line_to_four_node() receives raw, unfactored w1, w2                             |
|     |        -> _assign_patch_load() receives raw, unfactored p                                         |
|     |        -> _assign_load_to_four_node() receives raw, unfactored mag                                |
|     |        Output load_str contains UNFACTORED (1.0x) OpenSees command tuples.                       |
|     |                                                                                                   |
|     +---> B. Load Case Registration in Model:                                                           |
|              Stored in model.load_case_list:                                                            |
|              load_case_dict = {                                                                         |
|                  "name": lc.name,                                                                       |
|                  "loadcase": lc,                                                                        |
|                  "load_command": load_str,                                                              |
|                  "load_factor": gamma_case   <-- Stored separately!                                     |
|              }                                                                                          |
|                                         |                                                               |
|                                         v                                                               |
|  4. OpenSees Model Compilation & Analysis Execution                                                     |
|     model.analyze(load_case=lc.name)                     [osp_grillage.py:2178-2205]                    |
|     |                                                                                                   |
|     +---> Creates Analysis(load_case=lc)                                                                |
|     +---> Calls load_case_analysis.add_load_command(load_str, load_factor=gamma_case)                   |
|     |        [osp_grillage.py:2895-2919]                                                                |
|     |        Creates OpenSees pattern & timeSeries:                                                     |
|     |        timeSeries Constant tag -factor gamma_case  <-- Case-level scaling works!                  |
|     |        pattern Plain tag timeSeries_tag                                                           |
|     |        Dispatches load_str inside pattern.                                                        |
|     |                                                                                                   |
|     +---> Evaluates static linear system in OpenSees:                                                   |
|              ops.analyze(1)                                                                             |
|              Internal forces & reactions = gamma_case * (sum of loads in load_str)                      |
|                                         |                                                               |
|                                         v                                                               |
|  5. Results Extraction                                                                                  |
|     model.get_results()                                  [osp_grillage.py:2373-2541]                    |
|     Extracts forces and displacements into xarray DataSet.                                              |
|     (Optional post-processing: get_results(combinations={...}) provides xarray superposition)           |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Factor Semantics Findings

### 3.1 The Three Competing Factor Mechanisms
Our trace reveals that `ospgrillage` actually contains **three distinct, competing scaling mechanisms**:

1. **Mechanism 1: Component Load Factor (`LoadCase.add_load(load, load_factor=gamma_i)`)**
   - Intended Purpose: Scale individual load components *within* a single load case (e.g., permanent load $\gamma_G = 1.35$ vs surfacing $\gamma_S = 1.75$ in a composite ULS case, or live-load lane factor $\alpha = 0.8$ vs $1.0$).
   - Current State: **BROKEN (DEF-01).** Stored in `load_dict["factor"]` at `load.py:1167`, but completely dropped by `osp_grillage.py:1964` inside `_distribute_load_types_to_model`.
2. **Mechanism 2: LoadCase Factor (`OspGrillage.add_load_case(lc, load_factor=gamma_case)`)**
   - Intended Purpose: Scale an entire load case uniformly at the OpenSees time-series level.
   - Current State: **FUNCTIONAL.** Passed to `_time_series_command(gamma_case)`, which generates `("timeSeries", ("Constant", tag, "-factor", gamma_case), {})`. OpenSees scales the entire pattern by `gamma_case`.
3. **Mechanism 3: Post-Processing Superposition (`OspGrillage.get_results(combinations={lc_name: gamma_c})`)**
   - Intended Purpose: Compute linear combinations on solved xarray DataArrays post-solve without re-running OpenSees.
   - Current State: **FUNCTIONAL FOR BASIC CASES.** Evaluates `summation_array += basic_da.sel(Loadcase=name) * gamma_c`.

### 3.2 Production Application Usage in OsdagBridge
A critical question is: *Which of these three mechanisms does OsdagBridge production code actually use?*

Inspection of `analyser.py` reveals the real-world operational architecture:
- **`create_dead_load_combination` (`analyser.py:1556`):**
  Uses **Mechanism 2**. It aggregates dead loads into `DL_combined` with nominal unity weights and calls `model.add_load_case(DL_combined, load_factor=partial_safety_factor)`.
- **`create_dl_ll_combination` (`analyser.py:2088, 2098, 2110`):**
  Uses **Mechanism 1**. It creates `combo = og.create_load_case(name="1.35 DL + 1.5 LL")` and iterates over dead loads with `load_factor=float(dl_factor)` and live loads with `load_factor=float(ll_factor)`. It then adds `combo` to the model with default `load_factor=1.0`.
- **`create_uls_combinations` (`analyser.py:2348, 2406`):**
  Uses **Mechanism 1**. It copies permanent, surfacing, live, and wind loads into a composite `combo_lc` using `target_lc.add_load(entry["load"], load_factor=float(factor))`, and registers `combo_lc` with default `load_factor=1.0`.
- **`create_sls_combinations` (`analyser.py:2543, 2593`):**
  Uses **Mechanism 1**. Exactly mirrors ULS.
- **`create_vehicle_load_cases` (`analyser.py:1836, 1841`):**
  Uses **Both Mechanism 1 and Mechanism 2 simultaneously!** It adds the vehicle compound load using `lc.add_load(vehicle, load_factor=lane_factor)` (Mechanism 1), and then adds the load case using `model.add_load_case(lc, load_factor=dla)` (Mechanism 2, where `dla` is dynamic load allowance).
- **`model.get_results()`:**
  OsdagBridge **never** passes `combinations={...}` to `get_results()`. It relies entirely on solving explicit combination load cases inside OpenSees and extracting raw datasets via `model.get_results()`.

### 3.3 Double-Multiplication & Factor Loss Hazards

| Operational Scenario | Mechanism 1 (add_load) | Mechanism 2 (add_load_case) | Expected Math Result | OpenSees Physical Result Under Proposed DEF-01 | Risk Assessment |
|:---|:---:|:---:|:---:|:---:|:---|
| **A. Uniform Case (e.g. DL)** | $1.0$ (default) | $\gamma = 1.35$ | $1.35000 \times P$ | $1.0 \times 1.35 = 1.35000 \times P$ | **SAFE.** No double multiplication. |
| **B. Multi-Factor Combo (ULS)**| $\gamma_i = [1.35, 1.75, 1.5]$ | $1.0$ (default) | $\sum \gamma_i P_i$ | $\sum (\gamma_i \times 1.0) P_i = \sum \gamma_i P_i$ | **SAFE.** Correctly activates multi-factor combinations. |
| **C. Compounded Live Load** | $\text{lane} = 0.8$ | $\text{dla} = 1.10$ | $0.8 \times 1.10 \times P = 0.88 P$ | $(0.8 \times P) \times 1.10 = 0.88 P$ | **SAFE & MATHEMATICALLY EXACT.** Factors compound correctly. |
| **D. Accidental Double Entry** | $\gamma = 1.35$ | $\gamma = 1.35$ | $1.35000 \times P$ | $1.35 \times 1.35 = 1.8225 \times P$ | **HAZARD.** If an author passes $\gamma$ to *both* calls, OpenSees compounds them quadratically ($\gamma^2$). |
| **E. Post-Processing Clash** | $\gamma = 1.35$ | $1.0$ | $1.35000 \times P$ | In OpenSees: $1.35 P$. If `get_results(comb={"LC": 1.35})` is run: $1.8225 P$ | **HAZARD.** Post-processing superposition must only be run on unfactored cases. |

**Auditor Architectural Verdict on Factor Semantics:**  
Propagating `load_dict["factor"]` into `_distribute_load_types_to_model` is the mathematically correct remediation for Mechanism 1. It compounds linearly with Mechanism 2 ($\gamma_{\text{total}} = \gamma_{\text{load}} \times \gamma_{\text{case}}$). However, implementation guidelines must explicitly warn against applying factors to both `add_load` and `add_load_case` simultaneously unless compound scaling is intended.

---

## 4. Downstream Dependency Challenge & Falsification of Claims

### 4.1 Falsification of Claim: "DEF-02 Depends on DEF-01"
In [BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md) Section 2.2, Antigravity claims:
> *"DEF-02 (Batch 4): Superimposed dead load integration calls `create_dead_load_combination(partial_safety_factor=1.35)`. If `DEF-01` is not remediated first, `create_dead_load_combination` will continue to evaluate at nominal $1.0\times$, preventing complete verification of factored combinations."*

**The auditor conducted an empirical OpenSees experiment to test this claim:**
Using the authentic production bridge model on branch HEAD (`9e0b588`):
```python
bridge.grillage_model.create_dead_load_combination(partial_safety_factor=1.35)
bridge.grillage_model.model.analyze(load_case="1.0 DL")
r_100 = sum(-float(ops.nodeReaction(n, 2)) for n in ops.getNodeTags())
bridge.grillage_model.model.analyze(load_case="1.35 DL")
r_135 = sum(-float(ops.nodeReaction(n, 2)) for n in ops.getNodeTags())
```
**Empirical Results:**
- $\sum R_{y} (\text{1.0 DL}) = 1,444,818.79\text{ N}$
- $\sum R_{y} (\text{1.35 DL}) = 1,950,505.36\text{ N}$
- $\text{Observed Ratio} = \frac{1,950,505.36}{1,444,818.79} = \mathbf{1.350000}$ (Exact to 6 decimal places!)

**Falsification Conclusion:**  
Antigravity's claim is **FALSE**. `create_dead_load_combination` passes its safety factor to `model.add_load_case(DL_combined, load_factor=partial_safety_factor)` (Mechanism 2). In `osp_grillage.py:2067, 2197`, `add_load_case` stores this factor and passes it to OpenSees via `timeSeries Constant -factor 1.35`. OpenSees scales the reactions to **exact 1.35000** today, on the baseline codebase!  
Therefore, **DEF-02 does NOT depend on DEF-01** for its own dead load combination verification. DEF-02 could be scheduled and fully verified with a $1.35$ factor independently of DEF-01.

### 4.2 Where the Real Dependency on DEF-01 Lies
While DEF-02 does not depend on DEF-01 for single-case dead load scaling, the auditor identified where the true downstream dependencies actually exist:
1. **`create_dl_ll_combination` (`analyser.py:2088, 2098`):**  
   Here, dead load ($\gamma_D = 1.35$) and live load ($\gamma_L = 1.50$) have *different* factors within the same load case. Mechanism 2 cannot scale them independently. This method relies strictly on Mechanism 1 (`add_load(load_factor=...)`).
2. **`create_uls_combinations` (`analyser.py:2348`):**  
   IRC:6 Table B.2 combinations combine dead load ($1.35$), surfacing ($1.75$), and live load ($1.50$) in single cases. Currently, **all 24 ULS combinations in OsdagBridge evaluate at unfactored 1.0x**.
3. **`DEF-19b` (Lane Reduction Factors):**  
   `analyser.py:1836` passes `lane_factor` (0.8, 0.4) to `add_load()`. Because DEF-01 is broken, multi-lane bridges fail to apply lane reduction factors, overpredicting multi-lane live load demands.

**Auditor Dependency Verdict:**  
Antigravity overstated the dependency for DEF-02, but correctly identified the critical role of DEF-01 in unblocking multi-factor ULS/SLS combinations and live-load lane factor composition.

---

## 5. Candidate Prioritization & Scoring Recalculation

The auditor independently recalculated the multi-attribute weighted decision matrix across all eligible candidates using the governing weights:
- Structural Safety Significance: **30%**
- Reproducibility & Oracle Quality: **20%**
- Scope Isolation & DAG Alignment: **20%**
- Demonstrable Impact: **15%**
- Implementation Feasibility: **15%**

$$\text{Score} = 0.30 S + 0.20 O + 0.20 SC + 0.15 I + 0.15 F$$

### 5.1 Recalculated Scoring Table & Discrepancy Matrix

| Candidate ID | Defect Focus | Safety (30%) | Oracle (20%) | Scope (20%) | Impact (15%) | Feas. (15%) | Antigravity Reported Score | Auditor Recalculated Score | Arithmetic Residual | Reported Rank | Correct Rank |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DEF-01** | Load Factor Scaling Engine | 5.0 | 5.0 | 5.0 | 5.0 | 4.5 | 4.925 | **4.9250** | $0.0000$ | 1 | **1** |
| **DEF-02** | Crash Barrier SIDL in Combos | 4.5 | 4.5 | 3.5 | 4.5 | 4.0 | 4.225 | **4.2250** | $0.0000$ | 2 | **2** |
| **DEF-07** | Fatigue Stress Range Clamping | 4.0 | 4.0 | 3.0 | 4.0 | 3.5 | 3.725 | **3.7250** | $0.0000$ | 3 | **3** |
| **DEF-LATENT-ZP**| Transverse Coordinate Index | 2.0 | 5.0 | 5.0 | 1.5 | 5.0 | 3.575 | **3.5750** | $0.0000$ | 4 | **4** |
| **DEF-19 (a/b)** | Live-Load Factor Composition | 4.0 | 3.5 | 3.0 | 4.0 | 3.0 | 3.550 | **3.5500** | $0.0000$ | 5 | **5** |
| **DEF-03** | Section Property Desync | 4.0 | 4.0 | 2.5 | 3.5 | 3.0 | **3.450** | **3.4750** | **+0.0250** | 7 | **6** |
| **DEF-13** | Material Density Propagation | 3.0 | 4.0 | 3.5 | 3.0 | 4.0 | 3.450 | **3.4500** | $0.0000$ | 6 | **7** |
| **DEF-05** | Wind Parameter Propagation | 3.0 | 4.0 | 3.5 | 2.5 | 3.5 | 3.300 | **3.3000** | $0.0000$ | 9 | **8** |
| **DEF-10** | Database Read-Only Packaging | 2.0 | 5.0 | 3.5 | 3.0 | 3.5 | 3.275 | **3.2750** | $0.0000$ | 8 | **9** |

### 5.2 Arithmetic & Ranking Discrepancies Uncovered
The audit revealed three distinct clerical errors in Antigravity's prioritization report:
1. **DEF-03 Calculation Error:**  
   $0.30(4.0) + 0.20(4.0) + 0.20(2.5) + 0.15(3.5) + 0.15(3.0) = 1.20 + 0.80 + 0.50 + 0.525 + 0.45 = \mathbf{3.4750}$.  
   Antigravity reported **3.450** (an off-by-0.025 arithmetic discrepancy).
2. **DEF-03 vs DEF-13 Rank Inversion:**  
   Because DEF-03's true score is $3.4750$ and DEF-13's score is $3.4500$, **DEF-03 ranks 6th and DEF-13 ranks 7th**. Antigravity inverted them (ranking DEF-13 6th and DEF-03 7th).
3. **DEF-05 vs DEF-10 Rank Inversion:**  
   DEF-05 scored $3.3000$ and DEF-10 scored $3.2750$. Therefore, **DEF-05 ranks 8th and DEF-10 ranks 9th**. Antigravity inverted them (ranking DEF-10 8th and DEF-05 9th).

### 5.3 Integrity of Top Recommendations
Crucially, these discrepancies occur exclusively among ranks 6 through 9.  
- **DEF-01 (Score: 4.9250, Rank 1)** and **DEF-02 (Score: 4.2250, Rank 2)** are mathematically exact and hold a dominant margin over all other candidates.
- DEF-01's selection as Primary Candidate and DEF-02's selection as Backup Candidate are robust and fully justified.

---

## 6. Inventory Discrepancy Reconciliation

In [BATCH_3_CANDIDATE_INVENTORY.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_CANDIDATE_INVENTORY.md) Section 5, the document states:
> *"Applying the exclusion filters yields a clean candidate pool of **8 distinct defects / sub-defects**:"*

However, the table that follows lists **9 candidate rows (C1 through C9)**:
1. C1: DEF-01
2. C2: DEF-LATENT-ZP
3. C3: DEF-02
4. C4: DEF-03
5. C5: DEF-05
6. C6: DEF-07
7. C7: DEF-10
8. C8: DEF-13
9. C9: DEF-19 (19a/b)

**Reconciliation Finding:**  
This is a documentation off-by-one clerical error. Antigravity initially counted 8 defect IDs (treating DEF-19 as a single item and omitting DEF-LATENT-ZP from the count, or vice versa), but enumerated 9 distinct candidate rows. The prioritization matrix evaluated all 9 candidates. This error is non-material to the top ranking, but must be reconciled in the final batch selection records.

---

## 7. Numerical Oracle Assessment & Minimum Required Test Suite

### 7.1 Deficiency of Antigravity's Proposed Oracles
Antigravity proposed five test criteria in [BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md) Section 6.1:
- Point load scaling by 1.35
- Uniform line load scaling by 1.35
- Uniform patch load scaling by 1.35
- Compound 2-point load case ($50\text{ kN} \times 1.35 + 100\text{ kN} \times 1.50$)
- Unfactored invariance ($\gamma = 1.0$)

**The auditor challenges this set as INSUFFICIENT to guarantee production safety:**
1. **No CompoundLoad (Vehicle) Verification:**  
   Vehicles in `ospgrillage` are modeled as `CompoundLoad` instances. In `analyser.py:1836`, lane reduction factors are applied to `CompoundLoad` instances. Antigravity's AC-B3-04 tests two simple point loads, *not* a `CompoundLoad` object. If `_distribute_load_types_to_model` traverses `load_obj.compound_load_obj_list` without propagating the parent `CompoundLoad`'s factor, vehicle scaling will fail silently!
2. **No Beam-Element Line Load Verification:**  
   Line loads can be assigned to 2-node beam elements (`_assign_beam_ele_line_load`) when `long_beam_ele_load_flag` is set. Antigravity's proposal only tests 4-node grillage mesh line loads.
3. **No Zero-Factor / Relief Load Verification:**  
   Under IRC:6 Table B.2, relief loads have $\gamma = 0.0$ or $0.9$. A factor of $0.0$ must cleanly eliminate the load without producing NaN, division by zero, or lingering OpenSees commands.
4. **No Negative Factor / Reversible Load Verification:**  
   Seismic and wind combinations use negative factors (e.g. $-1.2 \text{ EQ}$). For line loads, negative factors invert intensities ($w_1, w_2 < 0$). The zero-crossing and centroid interpolation mechanisms developed in Batch 2 must be verified to maintain exact spatial centroid stability under negative scaling.
5. **No Compounding Verification:**  
   Must explicitly verify that when `lc.add_load(load, load_factor=alpha)` AND `model.add_load_case(lc, load_factor=beta)` are both used, the resulting force is exactly $\alpha \times \beta \times P$.

### 7.2 Minimum Required Independent Oracle Set (9 Oracles)
For Batch 3 to be accepted, the test matrix must implement the following 9 independent analytical fixtures:

| Oracle ID | Test Scenario | Input Load Parameters | Scaling Factor(s) | Closed-Form Analytical Oracle | Acceptance Tolerance | Mechanics Justification |
|:---|:---|:---|:---:|:---|:---:|:---|
| **OR-B3-01** | Point Load Scaling | $P = 100.0\text{ kN}$ at $(10, 0, 4)$ | $\gamma = 1.35$ | $R_y = 135.000\text{ kN}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Static equilibrium |
| **OR-B3-02** | Uniform Line Load Scaling | $w = 10.0\text{ kN/m}$, $L = 20\text{ m}$ | $\gamma = 1.35$ | $R_y = 270.000\text{ kN}$, $\bar{x} = 10.0\text{ m}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$, $|\Delta \bar{x}| \le 10^{-5}\text{ m}$ | Statics & centroid stability |
| **OR-B3-03** | Patch Load Scaling | $p = 2.0\text{ kPa}$, $A = 200\text{ m}^2$ | $\gamma = 1.35$ | $R_y = 540.000\text{ kN}$, $\bar{x} = 10.0\text{ m}, \bar{z} = 5.0\text{ m}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Area force conservation |
| **OR-B3-04** | Compound Multi-Load Case | $P_1 = 60\text{ kN}$ (Line), $P_2 = 100\text{ kN}$ (Patch) | $\gamma_1 = 1.35, \gamma_2 = 1.75$ | $R_y = 1.35(60) + 1.75(100) = \mathbf{256.000\text{ kN}}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Superposition of distinct factors |
| **OR-B3-05** | Vehicle `CompoundLoad` Scaling | 2-axle vehicle ($P_1 = 40\text{ kN}, P_2 = 60\text{ kN}$) | $\gamma = 0.80$ (Lane factor) | $R_y = 0.80(100.0) = \mathbf{80.000\text{ kN}}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Traversal of `compound_load_obj_list` |
| **OR-B3-06** | Beam-Element Line Load | $w = 8.0\text{ kN/m}$, $L = 20\text{ m}$ (on main girder) | $\gamma = 1.35$ | $R_y = 1.35(160.0) = \mathbf{216.000\text{ kN}}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Scaling in `_assign_beam_ele_line_load` |
| **OR-B3-07** | Zero-Factor Relief Load | $P = 150.0\text{ kN}$ (Dead), $P = 80\text{ kN}$ (Relief) | $\gamma_1 = 1.35, \gamma_2 = \mathbf{0.00}$ | $R_y = 1.35(150.0) + 0.0 = \mathbf{202.500\text{ kN}}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Zero-multiplication safety |
| **OR-B3-08** | Negative Factor (Reversible) | $w_1 = 4, w_2 = 8\text{ kN/m}$, $L = 20\text{ m}$ ($P = 120\text{ kN}$) | $\gamma = \mathbf{-1.20}$ | $R_y = \mathbf{-144.000\text{ kN}}$, $\bar{x} = 12.000\text{ m}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$, $|\Delta \bar{x}| \le 10^{-5}\text{ m}$ | Uplift & centroid sign stability |
| **OR-B3-09** | Compounded Dual Scaling | $P = 50.0\text{ kN}$ on Load, Case Factor on LC | $\gamma_{\text{load}} = 0.80, \gamma_{\text{case}} = 1.10$ | $R_y = (0.80 \times 1.10) \times 50.0 = \mathbf{44.000\text{ kN}}$ | $|\Delta R_y| \le 10^{-9}\text{ kN}$ | Multiplicative compounding |

---

## 8. Scope Boundary Recommendation

### 8.1 Rigorous File Scope
The auditor reviewed whether the proposed 2-file scope is justified.  
- `src/ospgrillage/load.py`:  
  Inspection of lines 1161–1168 confirmed that `LoadCase.add_load` **already correctly records** `load_factor` into `load_dict["factor"]`. Therefore, `load.py` may not even require modification unless `NodalLoad` requires an optional `factor` parameter on `get_nodal_load_call()`.
- `src/ospgrillage/osp_grillage.py`:  
  This is the primary remediation target:
  - `_distribute_load_types_to_model` (lines 1952–2042): Extract `load_dict.get("factor", 1.0)` and propagate it to all assignment calls (including nested `CompoundLoad` traversal).
  - Allocation helpers: Add optional `factor=1.0` parameter to `_assign_load_to_four_node`, `_assign_line_to_four_node`, `_assign_patch_load`, and `_assign_beam_ele_line_load`.

### 8.2 Mandatory Scope Exclusions
To maintain strict batch discipline:
1. **`DEF-LATENT-ZP` (`load.py:710`):** Must remain **EXCLUDED**. It is dormant in longitudinal bridge models and must not be opportunistically bundled into DEF-01.
2. **Application Bridge Code:** Zero changes to `analyser.py`, `designer.py`, `plategirderbridge.py`, or `executive_summary.py`.
3. **DEC Decisions:** Zero architectural decisions touched.

---

## 9. Acceptance & Rejection Criteria for Batch 3

### 9.1 Acceptance Criteria (Gates to Pass)
For DEF-01 implementation to be accepted:
1. **All 9 Oracles (OR-B3-01 to OR-B3-09) Pass:** With relative error $\le 10^{-9}$ on analytical statics and $\le 10^{-5}\text{ m}$ on centroids.
2. **Existing Baseline Test Flips to PASS:** `test_tc_reg_a01` in `run_all_baseline_tests.py` flips from `BASELINE_FAIL` (ratio 1.00000) to `PASS` (ratio 1.35000).
3. **Batch 1 & Batch 2 Invariance:** Zero regressions on DEF-12 ($63.40\text{ kN}$), DEF-08 (dynamic DCRs), DEF-11 (4 girders), and DEF-18 (barrier $313.92\text{ kN}$, slab $1275.00\text{ kN}$, overlay $244.80\text{ kN}$).
4. **Governance Invariance:** All 27 tests in `test_evidence_governance.py` pass; all 6 historical HMAC seals verified intact.

### 9.2 Rejection Criteria (Conditions That Abort Candidate)
Batch 3 must be rejected or redesigned if:
1. Scaling loads mutates the original `Loads` object in-place, causing state leakage across load cases or combinations.
2. Any existing unfactored load case ($\gamma = 1.0$) exhibits non-zero reaction differences ($|\Delta R_y| > 10^{-12}\text{ N}$).
3. OpenSees static linear solver diverges or becomes ill-conditioned under zero or negative load factors.

---

## 10. Remaining Uncertainty

1. **Memory & Copy Overhead in Moving Loads:**  
   When moving loads create hundreds of incremental load cases, does propagating factors impact memory or execution speed? (Preliminary analysis indicates zero additional overhead since factors are scalars).
2. **Interaction with Future DEF-19 Remediation:**  
   When DEF-19b (lane factors) is eventually remediated in `analyser.py`, it will rely on the scaling engine established here. Ensuring `CompoundLoad` scaling is 100% verified in Batch 3 eliminates future integration risk.

---

## 11. Final Audit Verdict

### **VERDICT:** **CONDITIONALLY READY**

### Justification:
The proposal to select **`DEF-01` (Load Factor Scaling Omission in `ospgrillage` Load Combinations)** as the primary candidate for Phase 3 Batch 3 is **technically sound, structurally urgent, and architecturally superior** to all other remaining candidates. Its resolution is essential to unblock meaningful verification of ULS and SLS load combinations across the bridge.

However, authorization cannot be granted unconditionally due to the analytical deficiencies and documentation discrepancies uncovered in this audit.

### Mandatory Pre-Authorization Conditions:
1. **Condition 1 (Correction of DEF-02 Dependency Claim):**  
   Antigravity must formally update the planning record to note that `DEF-02` does *not* depend on DEF-01 for single-case dead load scaling (as verified by OpenSees achieving 1.35000 on baseline), but that DEF-01 is required for multi-factor ULS/SLS combinations.
2. **Condition 2 (Adoption of 9-Oracle Test Suite):**  
   The Batch 3 Test Matrix must incorporate the 9-oracle specification established in Section 7.2 of this audit, explicitly including `CompoundLoad` vehicles, beam-element line loads, factor 0.0, negative factors, and dual-multiplier compounding.
3. **Condition 3 (Reconciliation of Inventory & Scoring Glitches):**  
   Antigravity must acknowledge in the Batch 3 Reconnaissance Dossier the candidate inventory off-by-one count (8 vs 9) and the minor scoring arithmetic/ranking adjustments for DEF-03, DEF-13, DEF-05, and DEF-10.
4. **Condition 4 (Strict Scope Containment):**  
   Source modifications must be restricted to `src/ospgrillage/osp_grillage.py` (and minimally `src/ospgrillage/load.py` only if required for signature compatibility). `DEF-LATENT-ZP` must remain strictly unbundled.
5. **Condition 5 (Human Project Director Authorization Gate):**  
   No branch switches, code modifications, or commits may occur until the Human Project Director formally issues the **Batch 3 Implementation Directive**.

---

*Report prepared and certified by Claude / Antigravity Independent Verification Auditor.*  
*Repository state verified: HEAD at `9e0b5883a247c8c0fb74b0890915600c7ab4a896`, working tree 100% clean.*
