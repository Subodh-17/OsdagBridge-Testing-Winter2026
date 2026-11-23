# PHASE 3 BATCH 2 — DEF-18 READINESS RECONNAISSANCE REPORT (REVISION 2.0)
## Finite Element Statics Non-Conservation in Grillage Load Distribution

**Document ID:** P3-B2-RR-002 (Supersedes P3-B2-RR-001)  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation (Batch 2 Readiness)  
**Defect:** DEF-18 — Finite Element Statics Non-Conservation in Grillage Load Distribution  
**Mode:** Strictly READ-ONLY Architectural & Algorithmic Reconnaissance  
**Author / Investigator:** Engineering Audit & Planning Persona  
**Audit Reconciliation Reference:** [CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_2_readiness/CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md) (P3-B2-AUDIT-CLAUDE-001)  
**Date:** 19 November 2026  
**Status:** REVISION 2.0 COMPLETE — READY FOR HUMAN AUTHORIZATION REVIEW  
**Remediation Branch:** `fix/phase-3-engineering-remediation`  
**Current HEAD:** `eaba0763daaf0a1e908a8b4575f501bb92f07cfb`  
**Baseline Anchor:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`, `origin/dev`)  

---

## 1. Executive Summary & Audit Reconciliation

This revised reconnaissance report resolves all five conditions established by independent auditor Claude in [CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_2_readiness/CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md).

### Summary of Revisions in Revision 2.0
1. **Mechanism C Impact Corrected:** Revised the description of Mechanism C (Coordinate Index Swap). We formally acknowledge that for uniform longitudinal line loads (including the sealed crash barrier), Mechanism C had **zero functional impact** on computed magnitudes. The $37.50\%$ baseline reaction deficit was driven exclusively by Mechanism A (magnitude scaling) and Mechanism B (end-bay out-of-mesh drop). Mechanism C is classified as a **latent defect & defensive correction**.
2. **Latent Bug in `load.py` Cataloged & Excluded:** Formally cataloged an upstream latent bug in `load.py:710` where `zp = point_coordinate[0]` as `DEF-LATENT-ZP`, and strictly excluded it from Batch 2 remediation scope.
3. **Deck Slab Oracle Reconciled:** Replaced the initial $1249.500\text{ kN}$ ($\rho_c = 24.5\text{ kN/m}^3$) oracle with the active application default parameter $\rho_c = 25.0\text{ kN/m}^3 \implies \mathbf{1275.000\text{ kN}}$, eliminating cross-batch conflation with DEF-13 (Batch 5).
4. **Wearing Course Geometry Reconciled:** Replaced the ambiguous carriageway oracle ($216.0\text{ kN}$) with the application's actual full-width ($204.0\text{ m}^2$) geometry oracle: $\mathbf{244.800\text{ kN}}$.
5. **Signed-Load & Zero-Crossing Policy:** Established a rigorous mechanical policy: segments with zero-crossings ($w_1 \cdot w_2 < 0$) are partitioned at $s_0 = \frac{|w_1|}{|w_1|+|w_2|} L$ into two independent sub-segments, preventing division-by-zero singularities or out-of-segment centroids.
6. **Eliminated Circular Test `TC-B2-05`:** Redesigned into an independent physical statics test on an oblique line load with analytical integrals ($P = 163.169\text{ kN}$, $\bar{x} = 11.667\text{ m}$, $\bar{z} = 3.333\text{ m}$); does not claim to detect Mechanism C.

---

## 2. Current Repository & Batch 1 State

The repository was verified using read-only Git plumbing tools:
- **Repository Location:** `F:\FOSSEE internship\source\OsdagBridge`
- **Active Branch:** `fix/phase-3-engineering-remediation`
- **Current HEAD SHA:** `eaba0763daaf0a1e908a8b4575f501bb92f07cfb`
- **Baseline Parent:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`, `origin/dev`)
- **Working Tree Status:** 100% clean (`nothing to commit, working tree clean`).
- **Batch 1 Commits Verified:**
  1. [`418fd75`](file:///F:/FOSSEE%20internship/source/OsdagBridge): DEF-12 (Bearing stiffener buckling capacity formula).
  2. [`12493c9`](file:///F:/FOSSEE%20internship/source/OsdagBridge): DEF-08 (Dynamic executive summary status reporting).
  3. [`eaba076`](file:///F:/FOSSEE%20internship/source/OsdagBridge): DEF-11 (Girder count alignment excluding overhang lines).
- **Remote Operations:** Strictly local branch; zero pushes, zero merges, zero PRs.
- **Batch 1 Integrity:** Verified untouched. All Batch 1 acceptance tests pass cleanly on current HEAD.

---

## 3. Forensic Defect Evidence from Baseline Run

The historical baseline evidence log at `F:\FOSSEE internship\testing\evidence\phase_2_13\baseline\tc_reg_eq_load_conservation.log` (sealed and verified under HMAC) establishes the following empirical behavior:

### 3.1 Crash Barrier Line Load Failure
```
[Crash barrier load] Crash Barrier:
    Applied Load:        313.920 kN (x_bar=12.000m, z_bar=4.250m)
    Support Reaction:    196.200 kN (x_bar=12.750m, z_bar=4.250m)
    Force Difference:   -117.720 kN (-37.50%) -> Force OK: False
    Centroid Shift:   dx=+0.750m, dz=-0.000m -> Centroid OK: False
    Equilibrium OK:   False
```
- **Force Loss:** The bridge has 2 barrier lines of $w = 6.54\text{ kN/m}$ over $L = 24.0\text{ m}$, yielding true physical load $2 \times (6.54 \times 24.0) = \mathbf{313.920\text{ kN}}$ ($156.960\text{ kN}$ per line). The total reaction is only $\mathbf{196.200\text{ kN}}$ ($98.100\text{ kN}$ per line), losing $\mathbf{117.720\text{ kN}}$ ($-37.50\%$).
- **Longitudinal Centroid Shift:** Applied load centroid is at bridge midspan $\bar{x} = 12.000\text{ m}$. The support reactions produce a centroid of $\bar{x} = \mathbf{12.750\text{ m}}$ ($dx = +0.750\text{ m}$).

### 3.2 Concrete Deck Slab & Wearing Course Patch Load Failure
```
[DD] Deck Slab:
    Applied Load:       1275.000 kN (x_bar=12.000m, z_bar=4.250m)
    Support Reaction:   1314.375 kN (x_bar=12.000m, z_bar=4.250m)
    Force Difference:    +39.375 kN ( +3.09%) -> Force OK: False

[1.0 DW] Wearing Course:
    Applied Load:        244.800 kN (x_bar=12.000m, z_bar=4.250m)
    Support Reaction:    252.360 kN (x_bar=12.000m, z_bar=4.250m)
    Force Difference:     +7.560 kN ( +3.09%) -> Force OK: False
```
- Both patch loads exhibit an identical $+3.09\%$ overprediction anomaly in total vertical reactions.

---

## 4. Root-Cause Analysis: The Four Failure Mechanisms

### 4.1 Mechanism A: Line Load Magnitude Omission of Segment Length
- **Location:** `src/ospgrillage/osp_grillage.py`, lines 1711–1728 in `_assign_line_to_four_node`.
- **Code:**
  ```python
  L = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[2] - p2[2]) ** 2)
  w1 = line_load_obj.interpolate_udl_magnitude([p1[0], 0, p1[1]])
  w2 = line_load_obj.interpolate_udl_magnitude([p2[0], 0, p2[1]])
  W = (w1 + w2) / 2
  ...
  load_str = self._assign_load_to_four_node(
      point=load_point, mag=W, shape_func=line_load_obj.shape_function
  )
  ```
- **Analysis:** `W` is average intensity (N/m). Line 1726 passes `mag = W` instead of `mag = W * L`.
- **Mathematical Impact:** For $\Delta L = 1.5\text{ m}$, the force assigned to each cell is $6.540\text{ kN}$ instead of $9.810\text{ kN}$ ($66.67\%$ of true force).

### 4.2 Mechanism B: First End-Bay Centroid Vector & Silent Out-of-Mesh Drop
- **Location:**
  - `src/ospgrillage/load.py`, lines 756–763 in `get_point_given_distance`.
  - `src/ospgrillage/osp_grillage.py`, lines 1693–1695 in `_assign_line_to_four_node`.
  - `src/ospgrillage/osp_grillage.py`, lines 1576–1579 in `_assign_load_to_four_node`.
- **Analysis:**
  1. In the first end bay ($x \in [0.0, 1.5\text{ m}]$), $p_2 = (0.0, z)$ and $p_1 = (1.5, z)$.
  2. `load.py:760` subtracts $x_{\text{dis}} = 0.75\text{ m}$ from $p_2[0]$, computing $x = -0.75\text{ m}$.
  3. $x = -0.75\text{ m}$ lies outside the bridge mesh $[0, L]$.
  4. `_assign_load_to_four_node` queries grid, gets `None`, and **silently returns `[]`**, dropping Bay 1.
- **Proof of Exact Baseline Match:**
  - 15 remaining bays $\times 6.540\text{ kN} = \mathbf{98.100\text{ kN}}$ per line ($2 \times 98.100 = \mathbf{196.200\text{ kN}}$).
  - Centroid of remaining 15 bays: $\bar{x} = \frac{1.5 + 24.0}{2} = \mathbf{12.750\text{ m}}$ ($dx = \mathbf{+0.750\text{ m}}$). Matches baseline log exactly.

### 4.3 Mechanism C: Coordinate Index Swap (Reconciled Impact Assessment)
- **Location:** `src/ospgrillage/osp_grillage.py`, lines 1714–1715.
- **Code:**
  ```python
  w1 = line_load_obj.interpolate_udl_magnitude([p1[0], 0, p1[1]])
  w2 = line_load_obj.interpolate_udl_magnitude([p2[0], 0, p2[1]])
  ```
- **Reconciled Audit Finding:**
  As established in Claude's independent audit (§3.3), `interpolate_udl_magnitude` (in `load.py`, line 721) uses only `xp = point_coordinate[0]` for non-vertical straight lines. Coordinate slot 2 is never read. Furthermore, for uniform loads ($w_1 = w_2 = 6540\text{ N/m}$), the gradient is zero.
  Therefore, **Mechanism C had ZERO functional impact on the baseline crash barrier results**. The defect is real, buggy code passing elevation $y=0$ instead of $z$, but its severity was dormant. It is retained as a **latent defect & defensive correction**.

### 4.4 Mechanism D: Patch Corner Double-Counting & Mutation Bug
- **Location:** `src/ospgrillage/osp_grillage.py`, lines 1802–1858 and 1894–1898 in `_assign_patch_load`.
- **Analysis:**
  1. The 4 corner cells intersect two perpendicular patch edges simultaneously and are added to `merged` without deduplication against adjacent edges.
  2. 4 corner cells $\times (1.5\text{ m} \times 1.05\text{ m}) = \mathbf{6.30\text{ m}^2}$ excess area.
  3. Excess force on deck slab: $6.30\text{ m}^2 \times 6.25\text{ kN/m}^2 = \mathbf{+39.375\text{ kN}}$ ($+3.09\%$).
  4. Excess force on wearing course: $6.30\text{ m}^2 \times 1.20\text{ kN/m}^2 = \mathbf{+7.560\text{ kN}}$ ($+3.09\%$).
  5. Line 1898 mutates `p_list` with `.pop(count)` inside `enumerate(p_list)`, corrupting deduplication.

---

## 5. Additional Finding: Latent Interpolation Bug in `load.py`

Independent audit finding C-04 identified an additional latent bug in `src/ospgrillage/load.py` (lines 708–710):
```python
xp = point_coordinate[0]
yp = point_coordinate[0]  # not used
zp = point_coordinate[0]  # BUG: should be point_coordinate[2]
```
- **Status:** **REAL BUG**. Line 710 sets `zp` to `point_coordinate[0]` ($x$).
- **Activation Condition:** Activates only for vertical/transverse line loads where $x_1 = x_2$ ($v[0] == 0$). Line 719 then evaluates `pp = (zp - z1) / v[2] * v[1] + p1`, using $x$ instead of $z$.
- **Disposition:** Because the current plate girder bridge implementation contains only longitudinal line loads ($x_1 \ne x_2$), this bug is dormant. To prevent scope creep and defect conflation, it is cataloged as a separate latent defect (`DEF-LATENT-ZP`) and **strictly excluded from Batch 2 remediation scope**. It will not be modified in Batch 2 commits. If remediated later, it requires separate defect registration, project director authorization, and dedicated batch planning.

---

## 6. Signed-Load & Near-Zero Denominator Mechanics

To address Claude's Condition 5 regarding the parametric centroid formula:
$$t = \frac{w_1 + 2w_2}{3(w_1 + w_2)}$$

We establish the following physical and mathematical handling policy:

### 6.1 Boundedness Under Non-Negative Loads
For all physically realistic gravity/dead loads ($w_1 \ge 0, w_2 \ge 0$, not both zero):
$$t \in \left[\frac{1}{3}, \frac{2}{3}\right] \subset (0, 1)$$
The centroid $\mathbf{p}_{\text{centroid}} = \mathbf{p}_1 + t(\mathbf{p}_2 - \mathbf{p}_1)$ is **strictly mathematically guaranteed** to lie within the central third of the physical segment. It can **never** step outside the cell.

### 6.2 Singularity & Zero-Crossing Handling ($w_1 \cdot w_2 < 0$)
When endpoint loads have opposite signs, $w_1 + w_2$ can approach zero, creating a pure force couple ($R = 0, M \ne 0$) where a single resultant centroid does not exist. Furthermore, if $w_1 + w_2 \ne 0$, the resultant centroid can lie far outside the segment.
- **Mechanically Correct Policy:**
  Segments with zero crossings are **partitioned into two sub-segments at the zero-crossing point**:
  $$s_0 = \frac{|w_1|}{|w_1| + |w_2|} L, \quad \mathbf{p}_0 = \mathbf{p}_1 + \left(\frac{|w_1|}{|w_1| + |w_2|}\right)(\mathbf{p}_2 - \mathbf{p}_1)$$
  1. Positive lobe $[\mathbf{p}_1, \mathbf{p}_0]$: Triangular load from $w_1$ to $0$. Force $R_+ = \frac{1}{2} w_1 s_0 > 0$. Centroid at $\mathbf{p}_{\text{cent}, +} = \mathbf{p}_1 + \frac{1}{3}(\mathbf{p}_0 - \mathbf{p}_1)$.
  2. Negative lobe $[\mathbf{p}_0, \mathbf{p}_2]$: Triangular load from $0$ to $w_2$. Force $R_- = \frac{1}{2} w_2 (L - s_0) < 0$. Centroid at $\mathbf{p}_{\text{cent}, -} = \mathbf{p}_0 + \frac{2}{3}(\mathbf{p}_2 - \mathbf{p}_0)$.
  Both sub-segments are assigned independently. Division by zero is completely eliminated.

### 6.3 Near-Zero Load Guard ($|w_1 + w_2| < 10^{-12}\text{ N/m}$)
If both $|w_1| < \epsilon$ and $|w_2| < \epsilon$, the segment carries zero load; assignment is skipped.

---

## 7. Reconciled Test Oracles & Matrix Reference

The full 17-test validation matrix is documented in [DEF_18_PROPOSED_TEST_MATRIX.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_2_readiness/DEF_18_PROPOSED_TEST_MATRIX.md) (Revision 2.0).

Key reconciled oracles:
1. **Crash Barrier (`TC-B2-10`):** $P = \mathbf{313.920\text{ kN}}$ ($2 \times 6.54 \times 24.0$), $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$.
2. **Concrete Deck Slab (`TC-B2-11`):** $P = \mathbf{1275.000\text{ kN}}$ ($204.0\text{ m}^2 \times 0.25\text{ m} \times 25.0\text{ kN/m}^3$), $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$.
3. **Wearing Course (`TC-B2-12`):** $P = \mathbf{244.800\text{ kN}}$ ($204.0\text{ m}^2 \times 0.05\text{ m} \times 24.0\text{ kN/m}^3$), $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$.
4. **Independent Skew Line (`TC-B2-05`):** $P = \mathbf{163.169\text{ kN}}$, $\bar{x} = 11.667\text{ m}$, $\bar{z} = 3.333\text{ m}$ (validates physical force and vector centroid conservation; does not claim to detect Mechanism C).

---

## 8. Implementation Scope & Batch Recommendation

- **Batch Scope Assessment:** Mechanisms A, B, and C share `_assign_line_to_four_node` and cannot be split. Mechanism D affects `_assign_patch_load` in the same file.
- **Strict Exclusion of DEF-LATENT-ZP:** Latent defect `DEF-LATENT-ZP` (`load.py:710`) is strictly excluded from Batch 2 and will not be touched.
- **Recommended Architecture:** Keep **Batch 2 as a single authorization batch** executed via **two isolated atomic Git commits**:
  - **Commit 1:** `fix(ospgrillage): correct line load magnitude scaling, vector centroid, and coordinate index (DEF-18-LINE)` strictly confined to `_assign_line_to_four_node` and `_assign_load_to_four_node` in `src/ospgrillage/osp_grillage.py`.
  - **Commit 2:** `fix(ospgrillage): eliminate patch load corner overcounting and iteration mutation bug (DEF-18-PATCH)` strictly confined to `_assign_patch_load` in `src/ospgrillage/osp_grillage.py`.
- **DEC Items:** Zero interaction with `DEC-013`, `DEC-015`, `DEC-018`, `DEC-019`, or `DEC-020`.

---

## 9. Conclusion

All five independent audit conditions are resolved. Revision 2.0 establishes complete readiness for implementation authorization review.
