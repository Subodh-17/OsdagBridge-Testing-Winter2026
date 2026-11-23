# PHASE 3 BATCH 3 — DEFECT PRIORITIZATION & TECHNICAL INVESTIGATION

**Document ID:** P3-B3-PRI-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation  
**Activity:** Batch 3 Defect Prioritization & Technical Investigation  
**Date:** 19 November 2026  
**Status:** READ-ONLY RECONNAISSANCE (UNAUTHORIZED)  
**Remediation Branch:** `fix/phase-3-engineering-remediation`  
**Current HEAD:** `9e0b5883a247c8c0fb74b0890915600c7ab4a896`  
**Baseline Anchor:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`)  

---

## 1. Executive Summary

This document presents a rigorous technical investigation and weighted multi-attribute prioritization of the eligible candidate defects extracted in [BATCH_3_CANDIDATE_INVENTORY.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_CANDIDATE_INVENTORY.md). Each candidate is evaluated against actual codebase implementations, sealed baseline regression logs, dependency constraints, and structural mechanics standards (IRC:6-2017, IS 800:2007, IRC:22-2015).

A 5-dimensional weighted scoring rubric is applied to produce a principled, defensible ranking for Phase 3 Batch 3 scheduling.

---

## 2. Technical Investigation of Eligible Candidates

---

### 2.1 Candidate C1: DEF-01 — Load Factor Scaling Omission in `ospgrillage`
- **Source Location:**
  - `src/ospgrillage/load.py:1161–1168` (`LoadCase.add_load`)
  - `src/ospgrillage/osp_grillage.py:1952–2042` (`OspGrillage._distribute_load_types_to_model`)
  - `src/ospgrillage/osp_grillage.py:2059–2070` (`OspGrillage.add_load_case`)
- **Current Behavior & Mechanism:**
  When a load is added to a `LoadCase` with a scaling factor (e.g., `lc.add_load(line_load, load_factor=1.35)`), `load.py:1167` stores `load_dict = {"load": deepcopy(load), "factor": load_factor}`. However, in `osp_grillage.py:1964`, `_distribute_load_types_to_model` loops through `load_groups` extracting only `load_obj = load_dict["load"]`. The key `load_dict["factor"]` is completely ignored and dropped. Consequently, all load commands compiled into OpenSees are assigned raw, unfactored magnitudes ($1.00000\times$).
- **Demonstrable User & Engineering Impact:**
  **CRITICAL.** Under Indian standard IRC:6-2017 Table B.2, ultimate limit state (ULS) design demands require multiplying dead loads by $\gamma_G = 1.35$ and live loads by $\gamma_Q = 1.50$. Dropping these load factors causes the finite-element grillage solver to evaluate all internal member forces (bending moments $M_z$, shear forces $V_y$, and reactions $R_y$) at unfactored nominal levels. All ULS design checks in OsdagBridge underestimate design demands by **$26\%$ to $43\%$**, creating an extreme unconservative hazard.
- **Reproducibility & Existing Tests:**
  $100\%$ reproducible. Sealed baseline test `TC-REG-A01-FACTOR-SCALING` runs in $1.211\text{ s}$ (`testing/evidence/phase_2_13/baseline/tc_reg_a01_factor_scaling.log`):
  ```
  Unfactored Load Case (Line + Patch) max force: 26331.9016 N
  Factored Load Case (Line + Patch) max force:   26331.9016 N (Target ratio: 1.35000)
  Observed Force Ratio:                         1.00000
  ```
- **Independent Verification Oracle:**
  Linear structural elasticity: For linear grillage analysis, scaling applied loads by scalar $\gamma$ must scale all support reactions and member internal forces by exactly $\gamma$:
  $$\mathcal{R} = \frac{\max |F_{\text{factored}}|}{\max |F_{\text{unfactored}}|} = \frac{\sum R_{y,\text{factored}}}{\sum R_{y,\text{unfactored}}} \equiv 1.350000 \pm 10^{-6}$$
- **Dependencies & DAG Position:**
  Direct successor to Batch 2 (`DEF-18`). `DEF-18` conserved static equilibrium of the un-factored loads; `DEF-01` enables factoring of those conserved loads. Downstream defects (`DEF-02` barrier SIDL combinations, `DEF-19` live load factors, and `DEF-03/13` ULS combinations) directly depend on `DEF-01`.
- **Scope Isolation & Feasibility:**
  High. Modifies only `src/ospgrillage/osp_grillage.py` and `src/ospgrillage/load.py`. No coupling to `designer.py` or `executive_summary.py`.
- **Standards Reference:** IRC:6-2017 Clause 202, Table B.2; IS 800:2007 Clause 5.3.

---

### 2.2 Candidate C2: DEF-LATENT-ZP — Transverse Coordinate Indexing in `load.py:710`
- **Source Location:**
  - `src/ospgrillage/load.py:710` (`LineLoading.interpolate_udl_magnitude`)
- **Current Behavior & Mechanism:**
  Inside `interpolate_udl_magnitude`, line 710 executes `zp = point_coordinate[0]` instead of `point_coordinate[2]`. For a transverse line load ($x_1 = x_2, z_1 \ne z_2$), line 718–719 computes:
  $$p(z) = \frac{z_p - z_1}{z_2 - z_1}(p_2 - p_1) + p_1$$
  Because $z_p$ reads $x$ (`point_coordinate[0]`), the numerator evaluates $(x - z_1)$, which mixes longitudinal coordinates with transverse boundary offsets.
- **Demonstrable User & Engineering Impact:**
  **LOW / ZERO IN PRODUCTION.** In the authentic OsdagBridge plate girder bridge layout, crash barriers, railings, footpaths, and medians are longitudinal line loads running parallel to the bridge centerline along the $X$-axis ($z_1 = z_2 = \text{const}$, $x_1 = 0, x_2 = 24.0\text{ m}$). Line 718 is protected by the guard `if v[0] == 0 and self.load_point_2.x == self.load_point_1.x:`. Since $v[0] \ne 0$ for all longitudinal loads, this branch is dormant in production.
- **Reproducibility & Existing Tests:**
  Reproducible only on a synthetic fixture with $x_1 = x_2$ and varying intensity $p_1 \ne p_2$.
- **Independent Verification Oracle:**
  Closed-form linear interpolation along the transverse coordinate $z$:
  $$p(z) = p_1 + \frac{z - z_1}{z_2 - z_1}(p_2 - p_1) \pm 10^{-12}\text{ N/m}$$
- **Dependencies & DAG Position:**
  Independent of downstream modules. Sits inside `src/ospgrillage/load.py`.
- **Scope Isolation & Feasibility:**
  Extremely small (single-line fix: `zp = point_coordinate[2]`). Zero regression risk.
- **Limitation as Standalone Batch:**
  Fixing a single line that impacts zero authentic bridge load cases does not warrant a major standalone remediation batch unless authorized as a small hygiene item.

---

### 2.3 Candidate C3: DEF-02 — Crash Barrier SIDL Omission in Dead Load Combinations
- **Source Location:**
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1336–1339`
  - `src/osdagbridge/core/bridge_types/plate_girder/analyser.py:1532–1558` (`create_dead_load_combination`)
- **Current Behavior & Mechanism:**
  In `plategirderbridge.py:1336–1339`, the bridge sets up individual loads: `model.create_crash_barrier_load()`, `model.create_railing_load()`, `model.create_median_load()`, and then immediately calls `model.create_dead_load_combination()`. However, `create_dead_load_combination` in `analyser.py:1532` aggregates `_DL_ATTRS = ["self_weight_load_case", "deck_load_case", "footpath_load_case", "sidl_combination"]`. Because `create_sidl_combination()` is never invoked, `self.sidl_combination` is `None`. Consequently, crash barriers ($313.92\text{ kN}$), railings, and wearing course are omitted from the dead load combination.
- **Demonstrable User & Engineering Impact:**
  **HIGH.** Completely omits $313.92\text{ kN}$ of permanent edge barrier load from the dead load combination, leading to severe under-prediction of exterior girder moments and shears.
- **Dependencies & Coupling:**
  - **Single-Case vs Multi-Factor Dependency Clarification:** create_dead_load_combination calls model.add_load_case(DL_combined, load_factor=partial_safety_factor). In ospgrillage, OspGrillage.add_load_case sets the OpenSees 	imeSeries Constant -factor gamma_case (Mechanism 2), which successfully scales reactions on baseline today. Thus, single-case dead load combination scaling does not strictly depend on DEF-01.
  - However, for **multi-factor load combinations** (e.g. create_dl_ll_combination combining dead load $\gamma_G = 1.35$ and live load $\gamma_Q = 1.50$ into a compound case) and lane reduction factor composition (DEF-19b), component-level scaling via Mechanism 1 (LoadCase.add_load(..., load_factor=...)) is required. Therefore, while DEF-02's dead load combination can execute in isolation via Mechanism 2, full ULS/SLS combination workflows and lane factoring strictly depend on DEF-01.
- **DAG Position:** Step 4 (downstream of Step 3).

---

### 2.4 Candidate C4: DEF-07 — Sectional Fatigue Stress Range Sign Doubling & Zero-Clamping
- **Source Location:**
  - `src/osdagbridge/core/bridge_types/plate_girder/designer.py:2976–2996`
- **Current Behavior & Mechanism:**
  1. Clamps minimum moment to zero: `mz_range_Nm = max(mz_all.max(), 0.0) - min(mz_all.min(), 0.0)`. For sagging moments ($M > 0$), this evaluates $\Delta M = M_{\max} - 0.0 = M_{\max}$ instead of $M_{\max} - M_{\min}$.
  2. Concatenates `Mz_i` and `Mz_j` from 2-node beam elements without accounting for local coordinate sign reversal at end-j. Sagging bending moments have opposite signs at node i vs node j, causing `mz_all` to contain both $+M$ and $-M$ under purely static loading.
- **Demonstrable User & Engineering Impact:**
  **HIGH.** Produces a fictitious cyclic stress range of $62.73\text{ MPa}$ under pure static dead load, causing the executive summary to unconditionally report girder fatigue failure ($\text{UR} = 1.97$).
- **Dependencies & Coupling:**
  Depends on analysis force results from `analysis_results.ds.forces.sel(Loadcase=_sls_frequent_lcs)`. Located in Step 7 of the DAG. Implementing DEF-07 before stabilizing load combinations (`DEF-01`, `DEF-02`) would require re-verifying numerical stress thresholds when combinations are fixed later.

---

### 2.5 Candidate C5: DEF-10 — Reference Database Read-Only Packaging & Access Paths
- **Source Location:**
  - `src/osdagbridge/core/data/project_location/database.py:12–30, 356`
  - `src/osdagbridge/core/bridge_types/plate_girder/ui_fields_project_location.py:16–29`
  - `src/osdagbridge/core/reports/report_generator.py:666`
  - `src/osdagbridge/desktop/ui/dialogs/project_location.py:932`
  - `src/osdagbridge/core/data/project_location/zone_lookup.py:189`
- **Current Behavior & Mechanism:**
  SQLite connections open without URI read-only mode flags (`?mode=ro`). SQLite attempts to create journal sidecars (`-journal`, `-wal`) in the package directory or CWD, mutating the package tree or failing with permission errors in read-only installations (e.g. `/usr/lib/` or `Program Files`).
- **Demonstrable User & Engineering Impact:**
  **MEDIUM.** Software reliability, packaging, and filesystem isolation defect. Zero impact on structural calculations or safety factors.
- **Dependencies & Coupling:**
  Completely decoupled from FE grillage and structural mechanics. Sits at Step 8 in the DAG.
- **Scope Breadth:**
  Spans 5 distinct files across UI, reporting, and data models (17 `sqlite3.connect` sites).

---

### 2.6 Candidate C6: DEF-03 — Section Property Desynchronization (Snapped vs Initial)
- **Source Location:**
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1260–1277`
- **Current Behavior & Mechanism:**
  Grillage beam element cross-section properties ($A, I_z, J$) are generated using preliminary un-snapped sizing estimates rather than the final snapped plate dimensions determined during sizing optimization. This produces an $8.3\%$ discrepancy in bridge deflection.
- **Demonstrable User & Engineering Impact:**
  **HIGH.** Deflection and stiffness discrepancies between finite-element solver and code capacity checks.
- **Dependencies & Coupling:**
  Coupled with `DEF-13` in Step 5. Evaluated after load factoring and combination assembly.

---

### 2.7 Candidate C7: DEF-13 — Hardcoded Steel and Deck Concrete Density Propagation
- **Source Location:**
  - `src/osdagbridge/core/bridge_types/plate_girder/analyser.py:10, 416`
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1332–1333`
- **Current Behavior & Mechanism:**
  Method signatures hardcode $\rho_s = 78.5\text{ kN/m}^3$ and $\rho_c = 25.0\text{ kN/m}^3$, ignoring user inputs from `input_dict`.
- **Demonstrable User & Engineering Impact:**
  **MEDIUM.** Only affects non-standard density inputs (e.g. lightweight concrete or weathering steel).
- **Dependencies & Coupling:**
  Step 5 in DAG, coupled with DEF-03.

---

### 2.8 Candidate C8: DEF-05 — Wind Parameter Propagation Loss
- **Source Location:**
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1380–1416`
  - `src/osdagbridge/core/bridge_types/plate_girder/analyser.py:1310–1370`
- **Current Behavior & Mechanism:**
  Falls back to minimum wind speed $33\text{ m/s}$ and default reference heights, ignoring user-specified wind zone and terrain category.
- **Demonstrable User & Engineering Impact:**
  **MEDIUM.** Affects transverse wind force on bridge superstructure.
- **Dependencies & Coupling:**
  Step 6 in DAG. Independent of vertical dead load combinations.

---

### 2.9 Candidate C9: DEF-19 (DEF-19a / DEF-19b) — Live-Load Factor Composition
- **Source Location:**
  - `src/osdagbridge/core/codes/irc6_2017.py:534, 543` (`DEF-19a`)
  - `src/osdagbridge/core/bridge_types/plate_girder/analyser.py:1803, 1827–1841` (`DEF-19b`)
- **Current Behavior & Mechanism:**
  `DEF-19a`: `if KEY_VEHICLE[1]:` tests a truthy string, always returning $0.10$ impact.
  `DEF-19b`: Lane reduction factors indexed per-vehicle within vehicle type rather than per loaded lane count.
- **Demonstrable User & Engineering Impact:**
  **HIGH.** Affects live load demands under IRC Class 70R and Class A vehicles.
- **Dependencies & Coupling:**
  `DEF-19c` is blocked by DEC-019. In addition, `analyser.py` invokes `lc.add_load(vehicle, load_factor=lane_factor)`. If `DEF-01` is not fixed, `add_load` drops the lane factor anyway. Therefore, DEF-19 depends on DEF-01.

---

## 3. Prioritization Scoring Methodology

Each candidate is evaluated using a formal weighted decision matrix:

| Evaluation Dimension | Weight | Definition & Scale Criteria |
|:---|:---:|:---|
| **1. Structural Safety Significance** | **30%** | Direct impact on structural capacities, limit-state demands, and life-safety factors ($1=\text{Cosmetic/Packaging}$, $3=\text{Moderate}$, $5=\text{Severe unconservative demand error}$). |
| **2. Reproducibility & Oracle Quality** | **20%** | Availability of unambiguous, closed-form analytical oracles and reproducible test evidence ($1=\text{Heuristic/Unclear}$, $3=\text{Empirical only}$, $5=\text{Exact closed-form mechanics}$). |
| **3. Scope Isolation & DAG Alignment** | **20%** | Freedom from forward dependencies, architectural decisions, and regression risk ($1=\text{Highly coupled/Blocked}$, $3=\text{Manageable coupling}$, $5=\text{Immediate DAG position, isolated}$). |
| **4. Demonstrable Impact** | **15%** | Magnitude of quantifiable error eliminated in authentic workflows ($1=\text{Latent/Unexercised}$, $3=\text{Edge cases}$, $5=\text{Universal impact on all bridge designs}$). |
| **5. Implementation Feasibility** | **15%** | Complexity, test execution speed, and verification turnaround ($1=\text{High complexity/Slow}$, $3=\text{Moderate}$, $5=\text{Clean, direct, fast turnaround}$). |

---

## 4. Multi-Attribute Candidate Scoring Matrix

| Candidate ID | Defect Focus | Safety (30%) | Oracle (20%) | Scope/DAG (20%) | Impact (15%) | Feasibility (15%) | Weighted Score | Rank |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DEF-01** | Load Factor Scaling Engine | **5.0** | **5.0** | **5.0** | **5.0** | **4.5** | **4.925** | **1 (Primary)** |
| **DEF-02** | Crash Barrier SIDL in Combinations | **4.5** | **4.5** | **3.5** | **4.5** | **4.0** | **4.225** | **2 (Backup)** |
| **DEF-07** | Fatigue Stress Range Clamping & Sign | **4.0** | **4.0** | **3.0** | **4.0** | **3.5** | **3.725** | **3** |
| **DEF-LATENT-ZP**| Transverse Coordinate Index in `load.py` | **2.0** | **5.0** | **5.0** | **1.5** | **5.0** | **3.575** | **4** |
| **DEF-19 (a/b)** | Live-Load Factor Composition | **4.0** | **3.5** | **3.0** | **4.0** | **3.0** | **3.550** | **5** |
| **DEF-03** | Section Property Desynchronization | **4.0** | **4.0** | **2.5** | **3.5** | **3.0** | **3.475** | **6** |
| **DEF-13** | Material Density Propagation | **3.0** | **4.0** | **3.5** | **3.0** | **4.0** | **3.450** | **7** |
| **DEF-05** | Wind Parameter Propagation | **3.0** | **4.0** | **3.5** | **2.5** | **3.5** | **3.300** | **8** |
| **DEF-10** | Database Read-Only Packaging | **2.0** | **5.0** | **3.5** | **3.0** | **3.5** | **3.275** | **9** |

### Dimension-by-Dimension Justification for Top Candidates:

1. **DEF-01 (Score: 4.925 — Rank 1):**
   - *Safety (5.0):* Unconditionally drops $\gamma_G = 1.35$ and $\gamma_Q = 1.50$ across all ULS combinations.
   - *Oracle (5.0):* Closed-form linear scaling $\mathcal{R} \equiv 1.350000 \pm 10^{-6}$.
   - *Scope/DAG (5.0):* Immediate successor to Batch 2 (`DEF-18`). Confined strictly to vendored `src/ospgrillage/`.
   - *Impact (5.0):* Resolves fundamental $26\%\text{–}43\%$ under-prediction across all bridge projects.
   - *Feasibility (4.5):* Fast $1.2\text{ s}$ unit test execution; clear pass-through in `_distribute_load_types_to_model`.
2. **DEF-02 (Score: 4.225 — Rank 2):**
   - *Safety (4.5):* Restores $313.92\text{ kN}$ of missing barrier dead load into dead load combinations.
   - *Oracle (4.5):* Clean analytical sums ($313.92\text{ kN}$ unfactored, $423.792\text{ kN}$ factored).
   - *Scope/DAG (3.5):* Sits at Step 4; logically depends on DEF-01 to evaluate factored combinations properly.
   - *Impact (4.5):* High physical impact on girder demands.
   - *Feasibility (4.0):* Clean method invocation in `plategirderbridge.py`.
3. **DEF-LATENT-ZP (Score: 3.575 — Rank 4):**
   - *Safety (2.0):* Inactive in all production bridge load cases (longitudinal lines only).
   - *Oracle (5.0):* Exact 1D linear interpolation formula along $Z$.
   - *Scope/DAG (5.0):* Single line in `load.py:710`.
   - *Impact (1.5):* Zero current impact on authentic bridge models.
   - *Feasibility (5.0):* Trivial 1-line edit.

---

## 5. Prioritization Conclusion

The multi-attribute analysis definitively identifies **`DEF-01` (Load Factor Scaling Omission in `ospgrillage` Load Combinations)** as the clear primary candidate for Phase 3 Batch 3. **`DEF-02`** is established as the primary backup candidate. 

The complete justification and scope proposal are detailed in [BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_PRIMARY_CANDIDATE_PROPOSAL.md).
