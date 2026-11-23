# CLAUDE — DEF-18 REVISION 2 INDEPENDENT ENGINEERING AUDIT

**Document ID:** P3-B2-AUDIT-CLAUDE-002
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting
**Phase:** Phase 3 — Engineering Remediation (Batch 2 Readiness)
**Defect:** DEF-18 — Finite Element Statics Non-Conservation in Grillage Load Distribution
**Mode:** Independent Engineering Audit — Revision 2 (READ-ONLY)
**Author:** Claude (Independent Auditor)
**Date:** 19 November 2026
**Prior Audit:** [CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_2_readiness/CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md) (P3-B2-AUDIT-CLAUDE-001)
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`
**Branch:** `fix/phase-3-engineering-remediation`
**HEAD SHA:** `eaba0763daaf0a1e908a8b4575f501bb92f07cfb`
**Baseline SHA:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

---

## 1. Audit Scope & Inspected Files

### 1.1 Documents Inspected

| Document | Version | Purpose |
|:---|:---|:---|
| `DEF_18_RECONNAISSANCE_REPORT.md` | Revision 2.0 (P3-B2-RR-002) | Root-cause analysis with reconciled Mechanism C |
| `DEF_18_PROPOSED_TEST_MATRIX.md` | Revision 2.0 (P3-B2-TM-002) | 17-test matrix with redesigned TC-B2-05 |
| `DEF_18_READINESS_REVISION_2.md` | (P3-B2-RR-REV2) | Condition resolution record |
| `DEF_18_SCOPE_BOUNDARY_AND_ACCEPTANCE_CRITERIA.md` | (P3-B2-SBAC-002) | Scope boundary and quantitative criteria |
| `CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md` | Prior audit (P3-B2-AUDIT-CLAUDE-001) | Preserved; not modified |

### 1.2 Source Files Re-Inspected

| File | Lines | Purpose |
|:---|:---|:---|
| `src/ospgrillage/osp_grillage.py` | 1571–1660, 1663–1760, 1795–1920 | `_assign_load_to_four_node`, `_assign_line_to_four_node`, `_assign_patch_load` |
| `src/ospgrillage/load.py` | 55–82, 228, 611–670, 700–765 | `create_load_vertex`, `LoadVertex`, `LineLoading.__init__`, `interpolate_udl_magnitude`, `get_point_given_distance` |
| `src/ospgrillage/utils.py` | 479–508, 963–1004 | `get_slope`, `check_dict_same_keys` |
| `src/osdagbridge/.../analyser.py` | 435–475, 466, 672–748 | `create_deck_load` (density parameter), `create_crash_barrier_load` |
| `src/osdagbridge/.../load_placement.py` | 25–65 | `CrashBarrier.to_global`, `OverlayLoad.to_global` |
| `src/osdagbridge/.../geometry.py` | 7 | `WET_CONCRETE_DENSITY_kN_m3 = DEFAULT_CONCRETE_DENSITY` |
| `src/osdagbridge/.../keyfile.py` | 115 | `DEFAULT_CONCRETE_DENSITY = 25.0` |

### 1.3 Repository State — VERIFIED ✓

| Item | Expected | Observed |
|:---|:---|:---|
| HEAD SHA | `eaba0763daaf` | `eaba0763daaf` ✓ |
| Branch | `fix/phase-3-engineering-remediation` | Confirmed ✓ |
| Working tree | Clean | Clean (no output from `git status --short`) ✓ |

---

## 2. Condition Resolution Assessment

### 2.1 Condition 1 — Deck Slab Oracle: **RESOLVED** ✓

**Prior Finding:** Oracle used $\rho_c = 24.5$ kN/m³ → $P = 1249.500$ kN, but application uses $\rho_c = 25.0$ kN/m³ → $P = 1275.000$ kN.

**Independent Verification:**
- Traced `DEFAULT_CONCRETE_DENSITY = 25.0` in `keyfile.py:115` → `WET_CONCRETE_DENSITY_kN_m3` in `geometry.py:7` → `analyser.py:466`. ✓
- `plategirderbridge.py` calls `create_deck_load(slab_thickness_m=deck_t_m)` without overriding `concrete_density_kN_m3`. ✓
- Application computes: $0.25 \times 25.0 = 6.25$ kN/m², $204.0 \times 6.25 = 1275.0$ kN. ✓
- Revised oracle in test matrix: $P = 1275.000$ kN. ✓
- Governance boundary: density propagation deferred to DEF-13 (Batch 5). Appropriate. ✓

### 2.2 Condition 2 — Wearing Course Geometry: **RESOLVED** ✓

**Prior Finding:** Ambiguous oracle with both $244.800$ kN and $216.000$ kN values.

**Independent Verification:**
- `OverlayLoad.to_global()` with `c = 0.0` creates patch over full width $z \in [0, 8.5]$. ✓
- $204.0 \times 1.20 = 244.800$ kN. ✓
- Revised oracle: single unambiguous value $P = 244.800$ kN for the full-bridge fixture. ✓
- $216.0$ kN retained only for separate partial-patch unit test. Appropriate. ✓

### 2.3 Condition 3 — Mechanism C Impact: **RESOLVED** ✓

**Prior Finding:** Impact overstated; zero functional effect on baseline evidence.

**Independent Verification of Revision 2 Reclassification:**
- Revision 2 formally acknowledges Mechanism C had zero functional impact. ✓
- Reclassified as "latent defect & defensive correction." ✓
- Narrative revised: "The $-37.50\%$ reaction deficit was caused exclusively by Mechanism A and Mechanism B." ✓
- Fix retained for correctness; no overclaim of impact. ✓

### 2.4 Condition 4 — Circular Test TC-B2-05: **PARTIALLY RESOLVED** ⚠️

**Prior Finding:** TC-B2-05 was an argument-inspection test, not a physical invariant test.

**Assessment of Redesigned TC-B2-05-LINE-SKEW-VARYING:**

The test is redesigned as a physical statics test on an oblique line load. This eliminates circularity. The force, $\bar{x}$ centroid, and $\bar{z}$ centroid are all verified against closed-form analytical oracles.

**However, there is one inaccuracy in the test matrix justification:**

> [!WARNING]
> **Independent Finding R2-01:** The test matrix (line 99 of `DEF_18_PROPOSED_TEST_MATRIX.md`) claims: *"Under Mechanism C, passing $y=0$ instead of $z$ evaluates intensities at $z=0$, distorting both $P$ and $\bar{z}$."*
>
> This claim is **incorrect** for the proposed TC-B2-05 fixture. The skew line from $(0, 0, 1)$ to $(20, 0, 5)$ has $v[0] = 20 \neq 0$, so `interpolate_udl_magnitude` takes the main path (line 721):
> ```python
> pp = (xp - self.load_point_1.x) / v[0] * v[1] + self.load_point_1.p
> ```
> This uses **only** `xp = point_coordinate[0]`. The z-coordinate in position 2 is never read. Therefore, the index swap (Mechanism C) has **no effect** on the computed intensities for this test fixture — just as it has no effect for the baseline crash barrier.
>
> TC-B2-05 **cannot detect Mechanism C.** It tests Mechanisms A and B and validates the vector centroid formula (including $\bar{z}$), which is valuable. But the claim that it exercises Mechanism C is false.

**Impact:** This does not invalidate the test — it is still an excellent physical statics test. But the justification text must be corrected to avoid false confidence. Mechanism C remains untestable with any non-vertical line load because `interpolate_udl_magnitude` only uses the x-coordinate for all non-vertical lines. Only a vertical line load ($x_1 = x_2$) would exercise the z-coordinate path — and even then, it would hit the separate `DEF-LATENT-ZP` bug.

**Severity:** LOW — the test itself is sound; only the narrative explanation is wrong. The fix for Mechanism C is still correct defensive engineering regardless of testability.

### 2.5 Condition 5 — Zero-Crossing and Signed Loads: **RESOLVED** ✓

**Prior Finding:** Centroid formula has division-by-zero risk when $w_1 + w_2 = 0$ and out-of-segment centroid when loads have opposite signs.

**Independent Mathematical Verification:**

**Zero-crossing location:**
For $w_1 \cdot w_2 < 0$, the zero crossing at parametric position:
$$s_0 = \frac{|w_1|}{|w_1| + |w_2|} \cdot L$$

Verification for $w_1 > 0, w_2 < 0$:
$$w(s_0) = w_1 + (w_2 - w_1) \frac{s_0}{L} = w_1 + (w_2 - w_1) \frac{w_1}{w_1 + (-w_2)} = w_1 - \frac{w_1(w_1 - w_2)}{w_1 - w_2} = 0 \quad \checkmark$$

Verification for $w_1 < 0, w_2 > 0$:
$$s_0 = \frac{-w_1}{-w_1 + w_2} L, \quad w(s_0) = w_1 + (w_2 - w_1) \frac{-w_1}{w_2 - w_1} = w_1 - w_1 = 0 \quad \checkmark$$

**Lobe force conservation:**

Sub-segment forces:
$$R_+ = \frac{w_1}{2} s_0, \quad R_- = \frac{w_2}{2}(L - s_0)$$

Total force: $R_+ + R_- = \frac{w_1 s_0}{2} + \frac{w_2(L - s_0)}{2}$

Substituting $s_0 = \frac{|w_1|}{|w_1| + |w_2|}L$ and simplifying (algebraically verified for both sign orientations):
$$R_+ + R_- = \frac{(w_1 + w_2)}{2} L \quad \checkmark$$

**Moment conservation** (verified for TC-B2-17 fixture $w_1 = +5, w_2 = -5, L = 10$):
- Original moment about $\mathbf{p}_1$: $\frac{L^2(w_1 + 2w_2)}{6} = \frac{100 \times (-5)}{6} = -83.333$ kN·m
- Partitioned: $12.5 \times \frac{5}{3} + (-12.5) \times \frac{25}{3} = \frac{-250}{3} = -83.333$ kN·m $\checkmark$

**Sub-segment centroid positions:**
- Lobe 1 centroid: $\mathbf{p}_1 + \frac{1}{3}(\mathbf{p}_0 - \mathbf{p}_1)$ — at $1/3$ from $\mathbf{p}_1$, inside $[\mathbf{p}_1, \mathbf{p}_0]$. ✓
- Lobe 2 centroid: $\mathbf{p}_0 + \frac{2}{3}(\mathbf{p}_2 - \mathbf{p}_0)$ — at $2/3$ from $\mathbf{p}_0$, inside $[\mathbf{p}_0, \mathbf{p}_2]$. ✓

**Edge cases verified:**

| Case | Behavior | Status |
|:---|:---|:---|
| $w_1 = +5, w_2 = -5$ ($R = 0$) | Two triangular lobes, equal and opposite | ✓ — no division by zero |
| $w_1 = +10, w_2 = -9$ ($R = 0.5L$) | Partitioned correctly, centroids inside | ✓ |
| $w_1 = -3, w_2 = +7$ | $s_0 = 3L/10$, lobes have opposite signs | ✓ |
| $|w_1| + |w_2| = 0$ (both zero) | Skipped by `abs(w1 + w2) < 1e-12` guard | ✓ |
| $w_1 = 0, w_2 > 0$ (no crossing) | No sign change → standard formula, $t = 2/3$ | ✓ |

> [!NOTE]
> The near-zero guard (`abs(w1 + w2) < 1e-12`) appears in the policy as a catch-all for both-zero endpoints. However, this condition is checked **after** the sign-crossing branch. If $w_1 = +\epsilon, w_2 = -\epsilon$ (both tiny but opposite), the sign-crossing branch fires first, correctly partitioning into two negligible lobes. The near-zero guard only catches the case where both endpoints are approximately zero **with the same sign**. This is correct behavior.

**Verdict: Mathematically sound. Force and moment conservation are preserved under partition.**

---

## 3. Mathematical & Engineering Verification

### 3.1 TC-B2-05-LINE-SKEW-VARYING Oracle

**Given:**
- $\mathbf{p}_1 = (0.0, 0.0, 1.0)$, $\mathbf{p}_2 = (20.0, 0.0, 5.0)$
- $w_1 = 4.0$ kN/m, $w_2 = 12.0$ kN/m

**Line length:**
$$L = \sqrt{20^2 + 4^2} = \sqrt{416} = 4\sqrt{26} \approx 20.396078\text{ m} \quad \checkmark$$

**Total force:**
$$P = \frac{w_1 + w_2}{2} \times L = \frac{16}{2} \times 20.396078 = 8 \times 20.396078 = 163.168624\text{ kN} \quad \checkmark$$

**Centroid parameter:**
$$t = \frac{w_1 + 2w_2}{3(w_1 + w_2)} = \frac{4 + 24}{3 \times 16} = \frac{28}{48} = \frac{7}{12} \approx 0.583333$$

**Longitudinal centroid:**
$$\bar{x} = 0.0 + \frac{7}{12} \times 20.0 = \frac{140}{12} = 11.6\overline{6}\text{ m} \quad \checkmark$$

**Transverse centroid:**
$$\bar{z} = 1.0 + \frac{7}{12} \times 4.0 = 1.0 + \frac{28}{12} = 1.0 + 2.3\overline{3} = 3.3\overline{3}\text{ m} \quad \checkmark$$

**All oracle values independently verified.** ✓

### 3.2 TC-B2-15-LINE-TRIANGLE Oracle

**Given:** $L = 15.0$ m, $w_1 = 0$, $w_2 = 12.0$ kN/m.

$$P = \frac{0 + 12}{2} \times 15 = 90.0\text{ kN} \quad \checkmark$$

$$t = \frac{0 + 24}{3(12)} = \frac{24}{36} = \frac{2}{3}$$

$$\bar{x} = \frac{2}{3} \times 15 = 10.0\text{ m from } \mathbf{p}_1 \quad \checkmark$$

### 3.3 TC-B2-17-ZERO-CROSSING-FAILSAFE Oracle

**Given:** $w_1 = +5.0$, $w_2 = -5.0$, $L = 10.0$ m.

$$s_0 = \frac{5}{5+5} \times 10 = 5.0\text{ m}$$

$$R_+ = \frac{5 \times 5}{2} = +12.5\text{ kN}, \quad R_- = \frac{-5 \times 5}{2} = -12.5\text{ kN} \quad \checkmark$$

$$R_{\text{total}} = 0\text{ kN} \quad \checkmark$$

Centroid of $R_+$: $\frac{5}{3} = 1.667$ m from $\mathbf{p}_1$. Inside $[0, 5]$. ✓
Centroid of $R_-$: $5 + \frac{2 \times 5}{3} = 8.333$ m from $\mathbf{p}_1$. Inside $[5, 10]$. ✓

### 3.4 TC-B2-16-PATCH-NONALIGNED Oracle

**Given:** Patch $x \in [3.7, 16.3]$, $z \in [1.2, 8.8]$, $p = 2.5$ kN/m².

$$A = (16.3 - 3.7) \times (8.8 - 1.2) = 12.6 \times 7.6 = 95.76\text{ m}^2 \quad \checkmark$$

$$P = 95.76 \times 2.5 = 239.4\text{ kN} \quad \checkmark$$

### 3.5 Remaining Oracles — Spot-Checked

| Test | Oracle | Verification |
|:---|:---|:---|
| TC-B2-01 | $P = 200.0$ kN ($10 \times 20$) | ✓ |
| TC-B2-02 | $P = 24.0$ N ($1.0 \times 24$) | ✓ |
| TC-B2-03 | $P = 60.0$ kN ($5 \times 12$), $\bar{x} = 10.0$ m | ✓ |
| TC-B2-04 | $P = 100.0$ kN, $\bar{x} = 12.0$ m | See note below |
| TC-B2-14 | $P = 240.0$ kN ($10 \times 24$), 16 bays | ✓ |

**TC-B2-04 note:** $w(x) = 2 + 0.3x$, $w_1 = 2$, $w_2 = 2 + 0.3 \times 20 = 8$.
$$P = \int_0^{20} (2 + 0.3x) dx = [2x + 0.15x^2]_0^{20} = 40 + 60 = 100\text{ kN} \quad \checkmark$$
$$\bar{x} = \frac{\int_0^{20} x(2+0.3x)dx}{100} = \frac{[x^2 + 0.1x^3]_0^{20}}{100} = \frac{400 + 800}{100} = 12.0\text{ m} \quad \checkmark$$

---

## 4. Test Independence Assessment

### 4.1 Overall Assessment

The Revision 2 test matrix is a substantial improvement over Revision 1. The elimination of argument-inspection (TC-B2-05 redesign) and the addition of 4 new tests (TC-B2-14 through TC-B2-17) strengthen coverage significantly.

### 4.2 Test-by-Test Independence Evaluation

| Test | Oracle Independence | Circular Risk | Verdict |
|:---|:---|:---|:---|
| TC-B2-01 | Closed-form: $w \times L$ | None | ✓ Independent |
| TC-B2-02 | Closed-form: $w \times L$ | None | ✓ Independent |
| TC-B2-03 | Closed-form: $w \times L_w$, $\bar{x} = (x_1 + x_2)/2$ | None | ✓ Independent |
| TC-B2-04 | Integral: $\int w(x) dx$ | None | ✓ Independent |
| TC-B2-05 | Integral: $\frac{w_1+w_2}{2} L_{\text{skew}}$, centroid formula | None — but see R2-01 | ✓ Independent (oracle correct, narrative wrong) |
| TC-B2-06 | Geometric: centroid at $x = 0.75$ m | Load command inspection, not solver result | ⚠️ Semi-independent |
| TC-B2-07 | Geometric: $A = 200$ m² | Cell area summation | ✓ Independent |
| TC-B2-08 | Closed-form: $p \times A$ | None | ✓ Independent |
| TC-B2-09 | Exception behavior | None | ✓ Independent |
| TC-B2-10 | Closed-form: $2 \times 6.54 \times 24$ | None | ✓ Independent |
| TC-B2-11 | Closed-form: $204 \times 6.25$ | None | ✓ Independent |
| TC-B2-12 | Closed-form: $204 \times 1.20$ | None | ✓ Independent |
| TC-B2-13 | Batch 1 regression | None | ✓ Independent |
| TC-B2-14 | Count + closed-form: 16 bays, $10 \times 24$ | None | ✓ Independent |
| TC-B2-15 | Triangle centroid: $P = wL/2$, $\bar{x} = 2L/3$ | None | ✓ Independent |
| TC-B2-16 | Closed-form: $12.6 \times 7.6 \times 2.5$ | None | ✓ Independent |
| TC-B2-17 | Partition algebra | None | ✓ Independent |

**TC-B2-06 note:** This test inspects "generated OpenSees load command coordinates" rather than solver reactions. It verifies that the centroid is placed at $x = 0.75$ m (not $x = -0.75$ m), which is a valid boundary check but operates at the implementation level rather than the physical invariant level. TC-B2-14 (all 16 bays contributing force) provides the equivalent physical-level verification. TC-B2-06 adds value as a diagnostic but is not strictly an invariant test.

### 4.3 Mechanism Coverage Matrix

| Mechanism | Tests that detect it | Coverage |
|:---|:---|:---|
| A — Line magnitude scaling | TC-B2-01, 02, 03, 04, 05, 10, 14, 15 | **STRONG** |
| B — End-bay drop | TC-B2-02, 06, 10, 14 | **STRONG** |
| C — Coordinate index swap | **None** (see R2-01) | **ZERO** — untestable with non-vertical lines |
| D — Patch corner overcount | TC-B2-07, 08, 11, 12, 16 | **STRONG** |
| D' — List mutation bug | TC-B2-07, 08, 16 | **ADEQUATE** |

> [!IMPORTANT]
> **Finding R2-02:** Mechanism C has zero test coverage in the revised matrix. No test can detect whether lines 1714–1715 pass `p1[1]` or `p1[2]`, because `interpolate_udl_magnitude` only uses `point_coordinate[0]` for all non-vertical lines. A test for Mechanism C would require either:
> - (a) A vertical line load ($x_1 = x_2$) — but this would hit `DEF-LATENT-ZP` simultaneously, conflating two defects.
> - (b) Modifying `interpolate_udl_magnitude` to actually use the z-coordinate — but this is out of scope for DEF-18.
>
> **Assessment:** Mechanism C is a pure code-correctness fix that is verified by inspection, not by functional testing. This is acceptable for a defensive correction with no functional impact. The fix should be verified by code review during implementation, not by a physical statics test.

---

## 5. Fail-Closed Load Placement Assessment

### 5.1 Proposed Policy

Replace silent `return []` in `_assign_load_to_four_node` (lines 1576–1579) with `raise ValueError(...)`.

### 5.2 Evaluation

| Criterion | Assessment |
|:---|:---|
| **Handling of fully out-of-mesh loads** | Explicit exception raised. ✓ |
| **Handling of partially out-of-mesh segments** | Not directly addressed. The vector centroid formula guarantees the centroid lies within $[p_1, p_2]$, which are intersection points within the mesh. For line loads within the mesh, no partially out-of-mesh centroid can occur. For patch loads, the centroid is computed from grid cell vertices, also within the mesh. **Implicitly safe.** ✓ |
| **Silent drop prevention** | The `return []` path is replaced with `raise ValueError`. No silent drop possible. ✓ |
| **Silent truncation** | No truncation occurs — loads are either fully assigned or raise an exception. ✓ |
| **Silent duplication** | Addressed by visited_grids set dedup for patches. ✓ |
| **Legitimate mesh-boundary cases** | The vector centroid formula places centroids within the segment $[p_1, p_2]$, where both $p_1$ and $p_2$ are known to lie on mesh boundaries or inside the mesh. Points exactly on mesh boundaries must be handled by `check_point_in_grid`. ✓ |
| **Impact on existing workflows** | The only current code path that hits `grid_nodes is None` is the Mechanism B out-of-mesh centroid ($x = -0.75$ m). After the vector centroid fix, this path should never be reached for valid loads. If it is reached, it indicates a genuine error. ✓ |
| **Testability** | TC-B2-09 tests `pytest.raises(ValueError)` for explicit out-of-mesh points. ✓ |

> [!NOTE]
> **Boundary tolerance concern:** When the centroid lands exactly on a mesh boundary (e.g., $x = 0.0$ or $x = L$), floating-point arithmetic could cause `check_point_in_grid` to return `False`. This is a pre-existing issue in `_get_point_load_nodes` (not introduced by DEF-18). The fail-closed exception would correctly surface this as an error rather than silently dropping the load. The implementation should consider a small epsilon tolerance in `check_point_in_grid` for boundary points, but this is a separate concern from DEF-18 scope.

### 5.3 Verdict

The fail-closed policy is well-defined, testable, and safe for existing workflows. ✓

---

## 6. Scope & Commit-Boundary Assessment

### 6.1 Commit 1: DEF-18-LINE

**Proposed contents:**
1. `_assign_line_to_four_node`: Magnitude scaling (`W → W*L`)
2. `_assign_line_to_four_node`: Vector centroid interpolation (replaces `get_point_given_distance`)
3. `_assign_line_to_four_node`: Zero-crossing segment partitioning
4. `_assign_line_to_four_node`: Coordinate index fix (`p1[1] → p1[2]`)
5. `_assign_load_to_four_node`: Fail-closed `ValueError`
6. `load.py:710`: Latent `zp` bug fix (optional)

**Assessment:**

Items 1–5 are tightly coupled within the line load assignment pathway. They share `_assign_line_to_four_node` and cannot be meaningfully separated. The fail-closed guard in `_assign_load_to_four_node` is a direct dependency (Mechanism B's silent drop is the trigger for the vector centroid fix). **Scope is appropriate.** ✓

**Item 6 — `DEF-LATENT-ZP`:**

> [!IMPORTANT]
> **Finding R2-03:** The Scope Boundary document (Section 1.1, item 4) lists the `zp = point_coordinate[0]` fix as "[Optional Defensive Item]" and the Commit 1 message includes "Fix latent zp coordinate bug in load.py:710." However, the Readiness Revision 2 document (Section 7) correctly identifies this as a **separate latent defect** (`DEF-LATENT-ZP`) requiring its own defect tracking and explicit authorization.
>
> These two documents are **inconsistent**. The Scope Boundary document bundles `DEF-LATENT-ZP` into the DEF-18-LINE commit, while the Readiness Revision 2 document treats it as a separate defect.
>
> **Recommendation:** `DEF-LATENT-ZP` should NOT be included in Commit 1. It is a separate defect in a separate function (`interpolate_udl_magnitude` vs. `_assign_line_to_four_node`) with a separate activation condition (vertical line loads vs. non-vertical line loads). Including it without its own defect ticket would constitute scope creep. If the Human Project Director wishes to fix it in the same batch, it should be explicitly authorized and documented as a separate scope item.

### 6.2 Commit 2: DEF-18-PATCH

**Proposed contents:**
1. `_assign_patch_load`: Corner cell deduplication via `visited_grids` set
2. `_assign_patch_load`: Non-mutating list deduplication

**Assessment:**

Both items are contained within `_assign_patch_load`. They address Mechanism D exclusively. The commit is cleanly scoped. ✓

### 6.3 Cross-Commit Dependencies

Commit 1 and Commit 2 operate on independent functions (`_assign_line_to_four_node` / `_assign_load_to_four_node` vs. `_assign_patch_load`). They can be independently validated:
- After Commit 1: Line load tests (TC-B2-01 through TC-B2-06, TC-B2-10, TC-B2-14, TC-B2-15, TC-B2-17) should pass. Patch tests may still fail.
- After Commit 2: All patch tests (TC-B2-07, TC-B2-08, TC-B2-11, TC-B2-12, TC-B2-16) should pass.
- TC-B2-09 (fail-closed) validates Commit 1.
- TC-B2-13 (Batch 1 regression) should pass after each commit.

**Independence confirmed.** ✓

### 6.4 Scope Creep Check

| Item | In Scope? | Assessment |
|:---|:---|:---|
| Load factor application | ✗ — Batch 3 | ✓ Not touched |
| Crash barrier ULS combination | ✗ — Batch 4 | ✓ Not touched |
| Density propagation | ✗ — Batch 5 | ✓ Not touched |
| Wearing course extent | ✗ — Not DEF-18 | ✓ Not touched |
| DEC items | ✗ — Frozen | ✓ Not touched |
| Batch 1 code | ✗ — Locked | ✓ Not touched |
| `DEF-LATENT-ZP` | ✗ — Separate defect | ⚠️ Inconsistently scoped (see R2-03) |

---

## 7. Acceptance Criteria Assessment

### 7.1 Quantitative Criteria Evaluation

| Criterion | Correctly Calculated | Reproducible | Strict Enough | Not Too Strict | Verdict |
|:---|:---:|:---:|:---:|:---:|:---|
| Line force $\leq 10^{-9} \cdot P$ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Centroid $\leq 10^{-5}$ m | ✓ | ✓ | ✓ | ✓ — well above FP noise | ✓ |
| End-bay 16/16 bays | ✓ | ✓ | ✓ | ✓ | ✓ |
| Out-of-mesh ValueError | ✓ | ✓ | ✓ | ✓ | ✓ |
| Patch area $\leq 10^{-9} \cdot A$ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Solver force $\leq 10^{-6} \cdot P$ | ✓ | ✓ | ✓ | See note | ⚠️ |
| Zero-crossing no div-by-zero | ✓ | ✓ | ✓ | ✓ | ✓ |
| Batch 1 100% PASS | ✓ | ✓ | ✓ | ✓ | ✓ |

**Solver tolerance note:** The $10^{-6}$ relative tolerance for full-bridge solver tests (TC-B2-10, TC-B2-11, TC-B2-12) is appropriate for a linear elastic FE solver with direct solution. OpenSees should achieve machine-precision equilibrium ($\sim 10^{-14}$), so $10^{-6}$ provides ample margin. However, if the solver uses iterative methods or the load distribution introduces discretization approximations (e.g., bilinear shape functions), the actual error might be larger. The $10^{-6}$ tolerance is a reasonable engineering choice but could potentially be tighter (e.g., $10^{-9}$) given the expected solver precision.

### 7.2 Missing Acceptance Criteria

| Gap | Recommendation | Priority |
|:---|:---|:---|
| **Mechanism C code-review verification** | Add a code-review checkpoint verifying `p1[2]` and `p2[2]` are passed (since no functional test can detect this) | SHOULD |
| **Solver centroid tolerance for TC-B2-05** | The skew line centroid tolerance is stated as $|dx| \leq 10^{-5}$ m, $|dz| \leq 10^{-5}$ m. For a full FE solver with bilinear shape functions, this may be tight for $\Delta x = 2.0$ m mesh. Consider whether discretization of a continuous skew line into cell-wise point loads introduces centroid error beyond $10^{-5}$ m. | SHOULD — verify during implementation |
| **Colinear loop validation** | The colinear loop (lines 1734–1752) already has `mag = W * L` correctly. No test specifically validates that the colinear path remains correct after the grid-intersection path is fixed. | LOW — colinear path is not being modified |

---

## 8. Unresolved Conditions

### 8.1 Findings Requiring Resolution

| ID | Finding | Severity | Required Action |
|:---|:---|:---|:---|
| **R2-01** | TC-B2-05 narrative incorrectly claims it exercises Mechanism C | LOW | Correct the "Why It Fails Under Original Defect" text. Remove the claim about Mechanism C distorting intensities. The test validly exercises Mechanisms A and B and validates the vector centroid. |
| **R2-03** | `DEF-LATENT-ZP` inconsistently scoped — bundled into Commit 1 message in Scope Boundary doc, but treated as separate in Readiness Revision 2 | MEDIUM | Either (a) remove `DEF-LATENT-ZP` from the DEF-18-LINE commit scope entirely, requiring separate authorization, or (b) explicitly register it as an in-scope optional item with a governance decision recorded. Do not silently include it. |

### 8.2 Findings Noted but Not Blocking

| ID | Finding | Severity | Note |
|:---|:---|:---|:---|
| **R2-02** | Mechanism C has zero test coverage | LOW | Acceptable for a defensive correction. Code review is sufficient. |
| **R2-04** | Solver centroid tolerance for skew line ($10^{-5}$ m) may need empirical validation | LOW | Verify during implementation; adjust if discretization error exceeds tolerance. |

---

## 9. Final Verdict

### **READY FOR HUMAN AUTHORIZATION**

All five conditions from the prior audit have been substantively resolved. The mathematical formulations are independently verified as correct. The test matrix is physically grounded, with independent analytical oracles. The scope boundaries are well-defined. The signed-load partitioning policy is mechanically sound and preserves both force and moment conservation.

**Two low-to-medium findings remain:**

1. **R2-01 (LOW):** The TC-B2-05 narrative incorrectly claims Mechanism C detectability. This is a documentation error only — the test itself is correct and valuable. **Does not block authorization.**

2. **R2-03 (MEDIUM):** The `DEF-LATENT-ZP` scoping is inconsistent across documents. The Human Project Director should make an explicit decision: include it with recorded authorization, or exclude it from Batch 2. **Does not block authorization** but requires a governance decision before implementation begins.

**Subject to:**
- The Human Project Director resolving R2-03 (DEF-LATENT-ZP scope decision) before implementation.
- R2-01 narrative correction being applied during implementation document finalization.

The engineering analysis, mathematical invariants, test design, and scope boundaries are **technically sound and ready for human authorization**.

---

**END OF REVISION 2 INDEPENDENT AUDIT**

*This audit was conducted under strictly read-only inspection boundaries. No source code, test scripts, governance configurations, or git state were modified. No previous audit documents were altered. The audit findings are advisory and do not authorize implementation.*

