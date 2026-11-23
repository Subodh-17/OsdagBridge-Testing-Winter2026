# PHASE 3 BATCH 3 — PRIMARY CANDIDATE REMEDIATION PROPOSAL

**Document ID:** P3-B3-PROP-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation  
**Activity:** Batch 3 Candidate Recommendation & Scope Boundary  
**Date:** 19 November 2026  
**Status:** PROPOSAL ONLY (UNAUTHORIZED — REQUIRES HUMAN APPROVAL)  
**Remediation Branch:** `fix/phase-3-engineering-remediation`  
**Current HEAD:** `9e0b5883a247c8c0fb74b0890915600c7ab4a896`  
**Baseline Anchor:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`)  

---

## 1. Executive Summary & Candidate Recommendations

Following the technical investigation in [BATCH_3_DEFECT_PRIORITIZATION.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_DEFECT_PRIORITIZATION.md), this proposal provides the formal candidate recommendation for **Phase 3 Batch 3**:

| Recommendation Role | Defect Identifier | Defect Title | Target Source File | Weighted Score |
|:---|:---:|:---|:---|:---:|
| **PRIMARY RECOMMENDATION** | **`DEF-01`** | **Load Factor Scaling Omission in `ospgrillage` Load Combinations** | `src/ospgrillage/osp_grillage.py`<br>`src/ospgrillage/load.py` | **4.925 / 5.0** |
| **BACKUP RECOMMENDATION** | **`DEF-02`** | **Crash Barrier SIDL Omission in Dead Load Combinations** | `src/osdagbridge/.../plategirderbridge.py`<br>`src/osdagbridge/.../analyser.py` | **4.225 / 5.0** |

---

## 2. Architectural Justification: Why DEF-01 is Preferable

### 2.1 The Mathematical Prerequisite to All Load Combinations
In Phase 3 Batch 2 (`DEF-18`), the finite element grillage load allocator was remediated to ensure strict Newtonian statics conservation ($\sum F_y = P_{\text{applied}}$, $\sum M = 0$). However, conserving static loads is futile if the grillage engine **unconditionally discards partial safety factors** when assembling limit-state combinations.

Under Indian standard IRC:6-2017 Table B.2, ultimate limit state (ULS) design demands require dead load scaling ($\gamma_G = 1.35$) and live load scaling ($\gamma_Q = 1.50$). Currently, `ospgrillage` drops `load_factor` in `_distribute_load_types_to_model`, compiling all loads into OpenSees at nominal unity scale ($1.00000\times$).

### 2.2 Unblocking Downstream Batches
In the Phase 3 Directed Acyclic Graph (DAG):
1. **DEF-02 (Batch 4 — Superimposed Dead Load Combinations):** Single-case dead load scaling in `create_dead_load_combination` utilizes Mechanism 2 (`add_load_case(..., load_factor=1.35)`), which generates an OpenSees `timeSeries Constant -factor 1.35` and scales reactions on baseline today. However, combining dead and live loads into compound limit-state cases (`create_dl_ll_combination`, `create_uls_combinations`, `create_sls_combinations`) relies on component-level scaling (Mechanism 1 via `LoadCase.add_load(..., load_factor=...)`), which strictly depends on DEF-01.
2. **DEF-19 (Live-Load Factor Composition):** Live-load combinations pass lane reduction factors ($\alpha = 0.8, 0.4$) via `add_load(vehicle, load_factor=lane_factor)`. These factors are discarded downstream if `DEF-01` is absent.
3. **DEF-03 / DEF-13 (Batch 5):** The full unified ULS dead load combination ($P_{\text{ULS}} = 2818.242\text{ kN}$) mathematically requires both conserved statics (`DEF-18`, complete) and factored load scaling (`DEF-01`).

Remediating `DEF-01` next directly fulfills the natural, linear progression of the load engine.

### 2.3 Strict Scope Isolation
`DEF-01` is confined entirely to the vendored finite element grillage package (`src/ospgrillage/`). It does not modify application sizing logic, UI bindings, database connections, or reporting templates. This provides clean scope isolation and minimal regression risk.

---

## 3. Disqualification Analysis: What Would Make DEF-01 Unsuitable

`DEF-01` should be disqualified or deferred only if:
1. **Vendored Code Freeze:** The Human Project Director explicitly directs that vendored `src/ospgrillage/` library code must not receive further modifications. (Note: Batch 2 successfully modified `osp_grillage.py` under explicit authorization).
2. **Upstream Bypass Discovered:** If OsdagBridge application code were found to manually pre-scale load intensities before passing them into `ospgrillage`. (Forensic inspection of `plategirderbridge.py` and `analyser.py` confirms OsdagBridge does **not** pre-scale intensities; it relies entirely on `ospgrillage` to apply combination factors).

If either condition occurs, **`DEF-02` (Crash Barrier SIDL Omission)** should immediately activate as the backup candidate.

---

## 4. Preliminary Scope Boundary for Batch 3 (DEF-01)

### 4.1 In-Scope Target Files
- `source/OsdagBridge/src/ospgrillage/osp_grillage.py`:
  - `_distribute_load_types_to_model` (lines 1952–2042): Extract `factor = load_dict.get('factor', 1.0)` and propagate it into load assignment helper calls.
  - Load assignment helpers: Pass scalar factor into magnitude scaling for point loads, line loads, patch loads, and beam element loads.
- `source/OsdagBridge/src/ospgrillage/load.py`:
  - Code inspection confirms `LoadCase.add_load` (lines 1161–1168) already correctly captures and stores `load_dict = {'load': deepcopy(load), 'factor': load_factor}`. Therefore, `load.py` requires **ZERO modifications**, strictly confining all implementation changes to `osp_grillage.py`.

### 4.2 Explicit Scope Exclusions
- **Application Bridge Code:** Zero modifications to `analyser.py`, `designer.py`, `plategirderbridge.py`, or `executive_summary.py`.
- **`DEF-LATENT-ZP` (`load.py:710`):** Sits in `interpolate_udl_magnitude`. As established in audit finding R2-03, `DEF-LATENT-ZP` is a separate defect with separate activation conditions. It must **NOT** be bundled into DEF-01 unless explicitly authorized as an independent atomic commit by the Human Project Director.
- **DEC Decisions:** Zero DEC items touched.

---

## 5. What Must Be Verified Before Implementation Authorization

Before authorizing implementation of Batch 3, a dedicated **Reconnaissance & Readiness Phase** must verify:
1. **Factor Interaction Mapping:** Audit how `add_load_case(load_case, load_factor=...)` interacts with `load_case.add_load(load, load_factor=...)` to ensure factors are compounded multiplicatively ($\gamma_{\text{case}} \times \gamma_{\text{load}}$) without double-counting.
2. **Compound & Moving Load Traversal:** Verify how compound loads and incremental moving loads traverse `_distribute_load_types_to_model`.
3. **Nodal & Beam Element Loads:** Ensure line loads mapped to beam elements (`_assign_beam_ele_line_load`) scale identically to 4-node surface loads.

---

## 6. Proposed Test Acceptance Criteria & Oracles

### 6.1 Acceptance Oracles
The implementation must satisfy the nine acceptance oracles (OR-B3-01 through OR-B3-09) frozen in [BATCH_3_DEF_01_IMPLEMENTATION_READINESS.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_DEF_01_IMPLEMENTATION_READINESS.md):

| Oracle ID | Test Fixture & Load Case | Nominal Input | Factored Target | Acceptance Tolerance | Governing Principle |
|:---|:---|:---:|:---:|:---:|:---|
| **OR-B3-01** | Point Load Scaling | $P = 100.0\text{ kN}$, $\gamma=1.35$ | $R_y = 135.000\text{ kN}$ | $|\mathcal{R} - 1.35| \le 10^{-6}$ | Linear Elasticity |
| **OR-B3-02** | Uniform Line Load Scaling | $w = 10.0\text{ kN/m}$, $L=20\text{ m}$, $\gamma=1.35$ | $R_y = 270.000\text{ kN}$ | $|\mathcal{R} - 1.35| \le 10^{-6}$, $\bar{x}=10.0\text{ m}$ | Centroid & Force Conservation |
| **OR-B3-03** | Uniform Patch Load Scaling | $p = 2.0\text{ kPa}$, $A=200\text{ m}^2$, $\gamma=1.35$ | $R_y = 540.000\text{ kN}$ | $|\mathcal{R} - 1.35| \le 10^{-6}$ | Equilibrium Conservation |
| **OR-B3-04** | Compound Multi-Load Case | $P_1 = 60\text{ kN}$ ($\gamma_1=1.35$), $P_2 = 100\text{ kN}$ ($\gamma_2=1.75$) | $R_y = 81.0 + 175.0 = 256.000\text{ kN}$ | $\Delta R_y \le 10^{-6}\text{ kN}$ | Superposition Equilibrium |
| **OR-B3-05** | CompoundLoad / Vehicle | $P_1 = 40\text{ kN}$, $P_2 = 60\text{ kN}$, $\gamma=0.80$ | $R_y = 80.000\text{ kN}$ | $\Delta R_y \le 10^{-6}\text{ kN}$ | Vehicle Aggregation |
| **OR-B3-06** | Beam-Element Line Load | $w = 8.0\text{ kN/m}$, $L=20\text{ m}$, $\gamma=1.35$ | $R_y = 216.000\text{ kN}$ | $|\mathcal{R} - 1.35| \le 10^{-6}$ | Direct Element Allocation |
| **OR-B3-07** | Zero-Factor Relief Load | $P_1 = 150\text{ kN}$ ($\gamma_1=1.35$), $P_2 = 80\text{ kN}$ ($\gamma_2=0.00$) | $R_y = 202.500\text{ kN}$ | $\Delta R_y \le 10^{-6}\text{ kN}$ | Zero-Factor Scaling |
| **OR-B3-08** | Negative / Reversible Factor | $P = 120\text{ kN}$, $\gamma=-1.20$ | $R_y = -144.000\text{ kN}$ | $\Delta R_y \le 10^{-6}\text{ kN}$ | Directional Conservation |
| **OR-B3-09** | Compounded Dual Scaling | $P = 50\text{ kN}$, $\gamma_{\text{load}}=0.80$, $\gamma_{\text{case}}=1.10$ | $R_y = 44.000\text{ kN}$ | $\Delta R_y \le 10^{-6}\text{ kN}$ | Multiplicative Compounding |

### 6.2 Regression and Governance Gates
- **AC-REG-01:** Baseline regression test `TC-REG-A01-FACTOR-SCALING` flips from `BASELINE_FAIL` to `PASS`.
- **AC-REG-02:** Prior batch invariance (`DEF-12`, `DEF-08`, `DEF-11`, `DEF-18`) verified invariant.
- **AC-REG-03:** Evidence governance passes 27/27 checks.

## 7. Independent Verification Test Strategy

1. **Standalone Test Suite:** Create `testing/test_cases/phase_3/test_batch_3_factor_scaling.py` containing dedicated unit tests for point, line, patch, and compound factor scaling.
2. **Baseline Regression Harness Gate:** Confirm that existing sealed test `TC-REG-A01-FACTOR-SCALING` in `run_all_baseline_tests.py` flips cleanly from `BASELINE_FAIL` to `PASS`.
3. **Evidence Governance Gate:** Execute `test_evidence_governance.py` (27/27 OK) to verify historical seals remain protected.

---

## 8. Risks That Should Force Rejection of Candidate

During reconnaissance or pre-implementation verification, Batch 3 authorization must be aborted if:
1. Multiplying factors inside `_distribute_load_types_to_model` alters the unscaled load definitions stored in `load_case.load_groups` (in-place mutation hazard).
2. The `load_factor` is applied twice when `get_results(combinations={...})` is executed downstream.
3. OpenSees domain commands become malformed or unstable under scaled magnitudes.

---

## 9. Submission for Human Review

This proposal is submitted to the Human Project Director for consideration. 

**Batch 3 remains strictly UNAUTHORIZED.** No implementation planning at code level, branch switching, or code modification will proceed without explicit Human Project Director authorization.
