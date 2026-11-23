# DEF-18 Scope Boundary & Acceptance Criteria (Revision 2.0)

**Document ID:** P3-B2-SBAC-002  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation (Batch 2 Implementation Readiness)  
**Defect:** DEF-18 — Finite Element Statics Non-Conservation in Grillage Load Distribution  
**Mode:** READ-ONLY Technical Specification (Pre-Implementation)  
**Status:** COMPLETE — READY FOR HUMAN IMPLEMENTATION AUTHORIZATION  
**Remediation Branch:** `fix/phase-3-engineering-remediation`  
**Current HEAD SHA:** `eaba0763daaf0a1e908a8b4575f501bb92f07cfb`  
**Baseline Anchor SHA:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  

---

## 1. Scope Boundary Specification

### 1.1 In-Scope Implementation Items
The scope of Batch 2 remediation is strictly confined to the following concrete code sites in `source/OsdagBridge/src/ospgrillage/`:

1. **`src/ospgrillage/osp_grillage.py` — `_assign_line_to_four_node` (lines 1663–1753):**
   - **Magnitude Scaling:** Replace `mag = W` with `mag = W * L` on line 1726, converting average intensity (N/m) to total segment force (N).
   - **Vector Centroid Interpolation:** Replace `load.py:get_point_given_distance` with direct parametric vector interpolation:
     $$\mathbf{p}_{\text{centroid}} = \mathbf{p}_1 + \left(\frac{w_1 + 2w_2}{3(w_1 + w_2)}\right) (\mathbf{p}_2 - \mathbf{p}_1)$$
     eliminating coordinate subtraction and preventing out-of-mesh coordinate drift ($x = -0.75\text{ m}$).
   - **Zero-Crossing & Singularity Guard:** When $w_1 \cdot w_2 < 0$, partition the segment at $s_0 = \frac{|w_1|}{|w_1|+|w_2|} L$ into two independent triangular lobes, eliminating division-by-zero singularities.
   - **Coordinate Index Correction:** Pass `p1[2]` and `p2[2]` (transverse $z$) instead of `p1[1]` and `p2[1]` (elevation $y$) into `interpolate_udl_magnitude`.
2. **`src/ospgrillage/osp_grillage.py` — `_assign_load_to_four_node` (lines 1576–1579):**
   - **Fail-Closed Out-of-Mesh Exception:** Replace silent `return []` with an explicit `ValueError` when `grid_nodes is None`.
3. **`src/ospgrillage/osp_grillage.py` — `_assign_patch_load` (lines 1795–1915):**
   - **Corner Cell Deduplication:** Track processed grid cells using an explicit `visited_grids = set(bound_grid)` set, preventing the 4 corner cells from being processed across multiple edge intersection dictionaries.
   - **Iteration List Mutation Bug:** Replace `p_list.pop(count)` inside `enumerate(p_list)` (lines 1894–1898) with a non-mutating list comprehension or set deduplication.

### 1.2 Strictly Out-of-Scope Items
The following items are explicitly **excluded** from Batch 2 and must not be modified:
- **Latent Vertical Line Coordinate Defect (`DEF-LATENT-ZP`):** The upstream latent bug in `src/ospgrillage/load.py:710` (`zp = point_coordinate[0]`) is **strictly excluded** from Batch 2 remediation scope. It is preserved as a separately documented latent defect. If remediated later, it requires separate defect registration, project director authorization, and batch planning.
- **Load Factor Application (DEF-01 / DEF-19):** Belongs to Batch 3. Batch 2 operates purely on nominal base loads with load factors set to 1.0.
- **Crash Barrier ULS Combination Integration (DEF-02):** Belongs to Batch 4. Batch 2 fixes isolated barrier statics only.
- **Dynamic Density Propagation (DEF-13):** Belongs to Batch 5. Batch 2 tests use application default parameters ($\rho_c = 25.0\text{ kN/m}^3$).
- **Wearing Course Extent Modification:** No modification to `load_placement.py` or `plategirderbridge.py` wearing course layout.
- **Unresolved Decision Items:** `DEC-013` (overhang lines), `DEC-015` (lane reduction), `DEC-018` (fatigue category), `DEC-019` (stiffener K), and `DEC-020` (Pucher charts) remain strictly frozen.
- **Batch 1 Code:** `designer.py` and `executive_summary.py` must remain completely untouched.

---

## 2. Quantitative Acceptance Criteria

For Batch 2 to be formally closed and accepted, all of the following criteria must be independently satisfied:

| Metric / Check | Governing Invariant | Expected Value / Range | Relative Tolerance | Status |
|:---|:---|:---|:---:|:---:|
| **Line Load Force Conservation** | Discretization Integrals | $\sum P_{\text{nodal}} = \int_0^L w(s) \, ds$ across $\Delta x = 1.0, 1.5, 2.0\text{ m}$ | $\le 10^{-9} \cdot P_{\text{total}}$ | **MANDATORY** |
| **Line Load Centroid Alignment** | Moment Equilibrium | $|\bar{x}_{\text{reactions}} - \bar{x}_{\text{analytical}}| \le 10^{-5}\text{ m}$ | Absolute: $\le 0.01\text{ mm}$ | **MANDATORY** |
| **End-Bay Load Inclusion** | Mesh Boundary Statics | All 16 bays contribute force; zero load points outside $[0, L]$ | Exact ($16/16$ bays) | **MANDATORY** |
| **Out-of-Mesh Rejection** | Fail-Closed Robustness | Explicit `ValueError` raised when applying load at $x < 0$ or $x > L$ | Exception Raised | **MANDATORY** |
| **Patch Area Conservation** | Geometric Integrals | Evaluated patch area $\sum A_{\text{cells}} = A_{\text{patch}}$ ($200.0\text{ m}^2$ on $20\times 10$ deck) | $\le 10^{-9} \cdot A_{\text{patch}}$ | **MANDATORY** |
| **Patch Force Conservation** | Solver Equilibrium | Full-bridge deck slab reaction $\sum R_y = \mathbf{1275.000\text{ kN}}$ ($\rho = 25.0$) | $\le 10^{-6} \cdot P$ | **MANDATORY** |
| **Wearing Course Equilibrium** | Solver Equilibrium | Full-bridge wearing course reaction $\sum R_y = \mathbf{244.800\text{ kN}}$ ($c = 0.0$) | $\le 10^{-6} \cdot P$ | **MANDATORY** |
| **Crash Barrier Equilibrium** | Solver Equilibrium | Full-bridge crash barrier reaction $\sum R_y = \mathbf{313.920\text{ kN}}$, $\bar{x} = 12.000\text{ m}$ | $\le 10^{-6} \cdot P$ | **MANDATORY** |
| **Zero-Crossing Robustness** | Mechanical Kinematics | Opposite-sign segment correctly split into two lobes without division by zero | Zero Division Free | **MANDATORY** |
| **Batch 1 Invariance** | Regression Suite | DEF-12: PASS ($63.4\text{ kN}$), DEF-08: PASS (74/74), DEF-11: PASS (4 girders) | 100% PASS | **MANDATORY** |

---

## 3. Atomic Commit Plan

To maintain flawless Git commit traceability, Batch 2 shall be executed as two isolated atomic commits on branch `fix/phase-3-engineering-remediation`:

### Commit 1: Line Load Statics Remediation
- **Target Files:**
  - `src/ospgrillage/osp_grillage.py` (`_assign_line_to_four_node`, `_assign_load_to_four_node`)
- **Commit Message:**
  ```
  fix(ospgrillage): correct line load magnitude scaling, vector centroid, and coordinate index (DEF-18-LINE)
  
  - Multiply average segment intensity by segment length (mag = W * L)
  - Replace get_point_given_distance with direct parametric vector interpolation
  - Implement zero-crossing segment partitioning for opposite-sign loads
  - Fix transverse coordinate index in interpolate_udl_magnitude call (p1[2])
  - Raise explicit ValueError on out-of-mesh load placement in _assign_load_to_four_node
  ```

### Commit 2: Patch Load Deduplication Remediation
- **Target File:**
  - `src/ospgrillage/osp_grillage.py` (`_assign_patch_load`)
- **Commit Message:**
  ```
  fix(ospgrillage): eliminate patch load corner overcounting and iteration mutation bug (DEF-18-PATCH)
  
  - Track processed grid cells via visited_grids set to prevent corner cell duplication
  - Eliminate 4x corner cell area excess (+6.30 m2 on 24x8.5m deck)
  - Replace mutating p_list.pop() in enumerate loop with clean deduplication
  - Restore exact deck slab (1275.0 kN) and wearing course (244.8 kN) static equilibrium
  ```

---

## 4. Verification and Governance Protocol

1. **Pre-Implementation Check:** Verify working tree clean, HEAD is `eaba076`, baseline is `d74f56d`.
2. **Implementation Execution:** Execute Commit 1 then Commit 2 in strict isolation.
3. **Evidence Capture:** Execute the 17-test validation suite (`DEF_18_PROPOSED_TEST_MATRIX.md`), saving evidence logs to `testing/evidence/phase_3/batch_2/`.
4. **Governance Verification:** Run `test_evidence_governance.py` (27/27 must pass).
5. **Independent Review:** Submit for Claude independent audit before requesting Batch 2 closure.
