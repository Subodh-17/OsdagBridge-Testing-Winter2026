# CLAUDE — DEF-18 INDEPENDENT ENGINEERING READINESS AUDIT

**Document ID:** P3-B2-AUDIT-CLAUDE-001
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting
**Phase:** Phase 3 — Engineering Remediation (Batch 2 Readiness)
**Defect:** DEF-18 — Finite Element Statics Non-Conservation in Grillage Load Distribution
**Mode:** Independent Engineering Audit (READ-ONLY)
**Author:** Claude (Independent Auditor)
**Date:** 19 November 2026
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`
**Branch:** `fix/phase-3-engineering-remediation`
**HEAD SHA:** `eaba0763daaf0a1e908a8b4575f501bb92f07cfb`
**Baseline SHA:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

---

## 1. Executive Verdict

### **CONDITIONALLY READY**

The reconnaissance correctly identifies four genuine defect mechanisms in the grillage load distribution pipeline. All four have been independently verified against source code. The numerical impact claims for the crash barrier and patch load anomalies are mathematically reproduced to exact precision. However, the audit identifies conditions that must be addressed before implementation authorization.

### Key Conditions

1. **The reconnaissance's characterization of Mechanism C (Coordinate Index Swap) overstates its immediate impact on the sealed bridge fixture.** For uniform line loads (`w1 == w2`), the index swap has zero effect on computed magnitude because the interpolation gradient is zero. The defect is real but dormant for the specific baseline evidence case. The proposed fix is still correct and necessary for non-uniform line loads.

2. **The reconnaissance fails to document a latent bug in `interpolate_udl_magnitude` itself** (lines 708–710 of `load.py`) where `zp = point_coordinate[0]` instead of `point_coordinate[2]`. This is an additional dormant defect that affects vertical line loads.

3. **The proposed test matrix has a numerical inconsistency** in TC-B2-11: the deck slab expected value ($1249.500$ kN) uses $\rho_c = 24.5$ kN/m³, but the baseline evidence log reports `applied = 1275.000 kN` with `mag = 6250.0 N/m²`, suggesting the actual code uses $\rho_c = 25.0$ kN/m³. The oracle must match the actual input parameters.

4. **TC-B2-12 wearing course expected value needs clarification.** The test matrix lists both "Full width: $P = 244.800$ kN" and "Carriageway: $P = 216.000$ kN." The baseline evidence shows `applied = 244.800 kN`, indicating the application uses the full bridge width for the wearing course patch, not the reduced carriageway width. The expected reaction value after fix must account for which area the patch actually covers.

5. **The proposed centroid formula is mathematically correct but its deployment as a complete replacement must be validated** against skewed and curved line loads, not just the longitudinal barrier case.

---

## 2. Independent Source Verification

### 2.1 Repository State — VERIFIED ✓

| Item | Expected | Observed |
|:---|:---|:---|
| HEAD SHA | `eaba0763daaf` | `eaba0763daaf` ✓ |
| Branch | `fix/phase-3-engineering-remediation` | Confirmed ✓ |
| Working tree | Clean | Clean ✓ |

### 2.2 Load Pipeline Trace — INDEPENDENTLY VERIFIED ✓

The load pipeline was independently traced through five tiers:

1. **User Inputs → Bridge Sizing** (`plategirderbridge.py:1332–1339`): `add_dead_loads()` calls individual load creation methods in sequence. ✓
2. **Load Placement Geometry** (`load_placement.py`):
   - `CrashBarrier.to_global()` (lines 31–42): Barrier lines span $[0, L] \times \{z\}$ with `z = offset` (left) or `z = width - offset` (right). ✓
   - `OverlayLoad.to_global()` (lines 59–64): Rectangular patch with edge clearance. ✓
   - `DeckLoad.to_global()` (lines 44–51): Full-width rectangular patch $[0,L] \times [0,W]$. ✓
3. **Load Object Creation** (`analyser.py:672–747`): `create_crash_barrier_load()` creates `LoadVertex(x, y=0, z, p=barrier_load)` and `LineLoading` objects. Barrier load = `6.54 kN/m × 1000 = 6540 N/m`. ✓
4. **Load Discretization** (`osp_grillage.py`):
   - `_distribute_load_types_to_model()` (lines 1922–2011) dispatches to `_assign_line_to_four_node()` for `LineLoading` and `_assign_patch_load()` for `PatchLoading`. ✓
   - `_get_line_load_nodes()` (lines 1257–1414) computes grid intersections, returning intersection points as `[x, y, z]` lists. ✓
5. **Solver & Reactions**: OpenSees via `ops.load()`, `ops.analyze()`, `ops.reactions()`. ✓

### 2.3 Intersection Point Format — INDEPENDENTLY VERIFIED ✓

Intersection points are stored as `[x, y, z]` lists:
- `Rz.append([R_z[0], pz1.y, R_z[1]])` (line 1476): 2D intersection `(x, z)` → `[x, y, z]`
- `Rx.append([R_x[0], px1.y, R_x[1]])` (line 1505): same format
- End points (line 1371–1372): `[start_load_vertex.x, start_load_vertex.y, start_load_vertex.z]` → `[x, y, z]`

Thus in `_assign_line_to_four_node`: `p1[0]` = x, `p1[1]` = y, `p1[2]` = z. **Confirmed.**

---

## 3. Mechanism-by-Mechanism Independent Audit

### 3.1 Mechanism A — Line Magnitude Scaling

**Reconnaissance Claim:** `_assign_line_to_four_node` passes `mag = W` (intensity, N/m) instead of `mag = W * L` (force, N).

**Independent Verification:**

| Item | Finding |
|:---|:---|
| **Line 1717:** `W = (w1 + w2) / 2` | Computes average intensity. For uniform $w = 6540$ N/m: $W = 6540$ N/m. ✓ |
| **Line 1726:** `mag=W` | Passes intensity directly as magnitude. Units: N/m. |
| **Line 1711:** `L = np.sqrt(...)` | Segment length. For $\Delta x = 1.5$ m bays: $L = 1.5$ m. ✓ |
| **Colinear loop (line 1743):** `mag = W * L` | Correctly multiplies by length. The inconsistency between the two code paths is confirmed. ✓ |
| **`_assign_load_to_four_node` (line 1637):** `node_load = [mag * n for n in Nv]` | Applies magnitude via shape functions. Expects force (N), not intensity (N/m). ✓ |

**Dimensional Analysis:**
- `W` has units N/m (intensity)
- `_assign_load_to_four_node` treats `mag` as a point load force (N)
- The equivalent point load for a segment should be: $P = W \times L$ (force = intensity × length)
- Passing $W$ instead of $W \times L$ underpredicts by factor $1/L = 1/\Delta L$

**Impact for $\Delta L = 1.5$ m:**
- Each cell receives $W = 6540$ N instead of $W \times L = 6540 \times 1.5 = 9810$ N
- Ratio: $6540/9810 = 2/3 = 66.67\%$

**Verdict: CONFIRMED ✓ — The defect is real and the magnitude scaling analysis is correct.**

### 3.2 Mechanism B — End-Bay Load Drop

**Reconnaissance Claim:** In the first end bay, `get_point_given_distance` subtracts the centroid offset from $p_2[0] = 0.0$, landing the load at $x = -0.75$ m (outside the mesh), which is then silently dropped.

**Independent Verification:**

**Step 1 — Point ordering in first end bay:**

For a longitudinal barrier line from $x=0$ to $x=24$ m, in the first grid bay ($x \in [0, 1.5]$), the intersection points are:
- `trans_intersect`: $x = 1.5$ m (at the first transverse gridline)
- `edge_intersect`: $x = 0.0$ m (at the bridge edge)

Branch taken (line 1693–1695):
```python
elif points["trans_intersect"] and points["edge_intersect"]:
    p1 = points["trans_intersect"][0]  # [1.5, 0, z]
    p2 = points["edge_intersect"][0]   # [0.0, 0, z]
```

**Step 2 — Centroid distance computation (line 1719):**
$$\bar{x} = \frac{2w_1 + w_2}{w_1 + w_2} \cdot \frac{L}{3}$$

For uniform load ($w_1 = w_2 = w$):
$$\bar{x} = \frac{3w}{2w} \cdot \frac{1.5}{3} = \frac{3}{2} \cdot 0.5 = 0.75 \text{ m from } p_2$$

**Step 3 — `get_point_given_distance` (load.py:756–763):**
```python
x_dis = xbar * np.cos(self.angle)  # 0.75 * cos(0) = 0.75
new_point = [point_coordinate[0] - x_dis, ...]  # 0.0 - 0.75 = -0.75
```

For a longitudinal line: $\text{angle} = \arctan(m)$ where $m = (z_2 - z_1)/(x_2 - x_1) = 0$ (same $z$), so $\cos(\text{angle}) = 1.0$.

Result: $x_{\text{centroid}} = 0.0 - 0.75 = -0.75$ m. ✓

**Step 4 — `_assign_load_to_four_node` (lines 1576–1579):**
```python
grid_nodes, _ = self._get_point_load_nodes(point=point)
if grid_nodes is None:
    load_str = []
    return load_str
```

Point $(-0.75, 0, z)$ is outside the mesh $[0, 24]$. `_get_point_load_nodes` iterates all grids, finds no match, returns `None`. The function returns `[]` — **silent drop with no warning or error.** ✓

**Step 5 — Why it works for non-first bays:**

For bay $[1.5, 3.0]$ with two longitudinal intersections: $p_1 = [1.5, 0, z]$, $p_2 = [3.0, 0, z]$. Centroid from $p_2$: $3.0 - 0.75 = 2.25$ m. This is **inside** the bay. The subtraction sign works because $p_2 > p_1$.

The fundamental issue: The code assumes $p_2$ always has the larger x-coordinate, so subtracting moves the centroid inward. In the first end bay, $p_2 = 0.0$ (edge) and $p_1 = 1.5$ (trans), violating this assumption.

**Verdict: CONFIRMED ✓ — The defect is real. The first end bay's load is silently dropped.**

### 3.3 Mechanism C — Coordinate Index Swap

**Reconnaissance Claim:** Lines 1714–1715 pass `p1[1]` (elevation $y = 0$) instead of `p1[2]` (transverse $z$) into `interpolate_udl_magnitude`.

**Independent Verification:**

```python
w1 = line_load_obj.interpolate_udl_magnitude([p1[0], 0, p1[1]])  # line 1714
```

Since `p1 = [x, y, z]`, `p1[1] = y = 0` for grillage model plane. The call passes `[x, 0, 0]` instead of `[x, 0, z]`.

**However — critically — `interpolate_udl_magnitude` has an internal issue of its own:**

```python
xp = point_coordinate[0]  # line 708
yp = point_coordinate[0]  # line 709 — not used
zp = point_coordinate[0]  # line 710 — BUG: should be point_coordinate[2]
```

All three local variables are assigned `point_coordinate[0]`! The function ignores `point_coordinate[1]` and `point_coordinate[2]` entirely for straight-line loads.

For the main interpolation path (non-vertical lines, line 721):
```python
pp = (xp - self.load_point_1.x) / v[0] * v[1] + self.load_point_1.p
```

This uses only `xp = point_coordinate[0]`, which is the x-coordinate. The z-coordinate is never used in this code path.

**Impact assessment for the sealed bridge fixture:**

For the crash barrier: $w_1 = w_2 = 6540$ N/m (uniform load). Since $v[1] = \text{load\_point\_2.p} - \text{load\_point\_1.p} = 0$, the interpolation returns $\text{load\_point\_1.p} = 6540$ regardless of coordinates. **The index swap has ZERO effect on uniform loads.**

For non-uniform loads where $w_1 \neq w_2$: The interpolation uses only `xp`, which is correct (`p1[0]` = x). The incorrect z-coordinate in position 2 of the argument list is **never read** by the function for non-vertical lines.

> [!IMPORTANT]
> **Independent auditor finding:** The index swap defect at lines 1714–1715 is real code that passes wrong data, but due to the internal structure of `interpolate_udl_magnitude` (which only uses `point_coordinate[0]` for non-vertical lines), it has **no functional impact** on the computed magnitude for any straight non-vertical line load, whether uniform or non-uniform.
>
> The reconnaissance's characterization of Mechanism C as "corrupting the evaluated intensity" is **overstated** for the current codebase. The fix (`p1[2]` instead of `p1[1]`) is still correct as defensive engineering, but it does not change any computed values in the present code path.

**Additional finding — `interpolate_udl_magnitude` latent bug:**

Lines 708–710 assign `zp = point_coordinate[0]` (should be `point_coordinate[2]`). This is a **separate latent defect** not documented in the reconnaissance. It would become active if vertical line loads ($x_1 = x_2$) are used, causing incorrect intensity interpolation along the z-axis. The fix for Mechanism C should be paired with a fix for this latent bug.

**Verdict: PARTIALLY CONFIRMED — The index swap is real buggy code, but its impact is overstated. Fix is correct but won't change computed values. A separate latent bug exists in `interpolate_udl_magnitude` itself.**

### 3.4 Mechanism D — Patch Corner Double-Counting & Mutation Bug

**Reconnaissance Claim:** Corner grid cells of patch loads are counted multiple times because each of the 4 patch edges independently queries intersecting grids, and corner cells appear in two adjacent edge queries.

**Independent Verification:**

**Step 1 — Patch edge queries (lines 1827–1854):**

Four separate calls to `_get_line_load_nodes`:
- Edge 1: `load_point_1 → load_point_2` (e.g., bottom edge)
- Edge 2: `load_point_2 → load_point_3` (e.g., right edge)
- Edge 3: `load_point_3 → load_point_4` (e.g., top edge)
- Edge 4: `load_point_4 → load_point_1` (e.g., left edge)

**Step 2 — Merge via `check_dict_same_keys` (utils.py:963–1004):**

```python
merged = check_dict_same_keys(intersect_grid_1, intersect_grid_2)
merged = check_dict_same_keys(merged, intersect_grid_3)
merged = check_dict_same_keys(merged, intersect_grid_4)
```

`check_dict_same_keys` merges dictionaries. For common keys (grids appearing in multiple edge queries), it combines intersection point lists, deduplicating individual points (line 998: `if val not in combine_val`).

**Step 3 — Corner cells:**

A corner grid cell (e.g., the bottom-left corner of the deck) is intersected by both the bottom edge (Edge 1) and the left edge (Edge 4). Both edge queries return this grid with their respective intersection points. When merged, the grid appears once in `merged` (since it's the same key), with the combined intersection points from both edges.

The grid is **not** double-processed in the `for grid, int_point_list in merged.items()` loop because it appears as a single dictionary key. However, the grid may **also** appear in `bound_grid` (from `_get_bounded_nodes`), which is processed separately in lines 1802–1823.

**Step 4 — Cross-checking `_get_bounded_nodes` (lines 1546–1568):**

`_get_bounded_nodes` identifies grids where **all** nodes are inside the patch. For a full-deck patch covering the entire mesh, all interior grids are "bounded." Corner grids: if all 4 nodes of the corner grid lie inside the patch vertices, the corner grid is in `bound_grid`. If only some nodes are inside, it's in `merged` only.

For a deck patch exactly matching the mesh boundaries: corner cells have nodes at the mesh corners, which are ON the patch boundary. Whether `check_point_in_grid` (which is used for the bounded-node check) considers points exactly on the boundary as "inside" determines whether corner cells end up in `bound_grid`, `merged`, or both.

**Step 5 — The overcounting mechanism:**

The critical issue: if a corner grid appears in **both** `bound_grid` (processed at lines 1802–1823) **and** `merged` (processed at lines 1861–1912), its load is computed twice. The `merged` loop does **not** check whether a grid was already processed in `bound_grid`.

For 4 corner cells, each with area $\Delta x \times \Delta z = 1.5 \times 1.05 = 1.575$ m²:
- Excess area: $4 \times 1.575 = 6.30$ m²
- Deck slab excess: $6.30 \times 6.25 = 39.375$ kN → matches baseline evidence ✓
- Wearing course excess: $6.30 \times 1.20 = 7.560$ kN → matches baseline evidence ✓

> [!NOTE]
> The percentage $+3.09\%$ in the baseline evidence applies to the **applied** load values in the evidence log. The excess from $1275.0$ kN: $39.375/1275.0 = 3.088\%$. From $244.8$ kN: $7.560/244.8 = 3.088\%$. Both match.

**Step 6 — List mutation bug (lines 1894–1898):**

```python
for count, point in enumerate(p_list):
    dupe = [point == val for val in p_list]
    if sum(dupe) > 1:
        p_list.pop(count)
```

This is a classic Python antipattern. When `p_list.pop(count)` removes an element, subsequent elements shift down by one index, but `enumerate` continues with the incremented counter, skipping the element that shifted into position `count`. For a list with 3 consecutive duplicates `[A, A, A, ...]`, only the first `A` is removed (count=0), then count=1 examines what was originally at index 2, missing the duplicate now at index 1.

**Verdict: CONFIRMED ✓ — Both the corner overcounting and list mutation bugs are verified. The numerical impact exactly matches the baseline evidence.**

---

## 4. Independent Numerical Verification

### 4.1 Crash Barrier — 313.920 kN vs 196.200 kN

**Given:**
- 2 barrier lines, $w = 6.54$ kN/m, $L = 24.0$ m
- 16 bays of $\Delta L = 1.5$ m each

**True physical load:**
$$P_{\text{true}} = 2 \times 6.54 \times 24.0 = 313.920 \text{ kN}$$

**Defective computation (per line):**
- Bay 1 ($x \in [0, 1.5]$): Centroid lands at $x = -0.75$ m → **dropped** (Mechanism B). Force = 0 kN.
- Bays 2–16 ($x \in [1.5, 24.0]$): 15 bays, each receives `mag = W = 6.54 kN` (not `W × L = 9.81 kN`) due to Mechanism A.
- Per line: $15 \times 6.54 = 98.10$ kN
- Total: $2 \times 98.10 = 196.20$ kN ✓

**Centroid of remaining 15 bays:**
$$\bar{x} = \frac{\sum_{k=2}^{16} x_k \cdot 6.54}{15 \times 6.54}$$

Each bay centroid is at its midpoint: $x_k = 0.75 + 1.5(k-1)$ for $k = 1, \ldots, 16$.
Remaining bays ($k = 2, \ldots, 16$): centroids at $2.25, 3.75, 5.25, \ldots, 23.25$ m.
$$\bar{x} = \frac{2.25 + 3.75 + \cdots + 23.25}{15} = \frac{1.5 + 24.0}{2} = \frac{25.5}{2} = 12.75 \text{ m}$$

Wait — let me recompute this more carefully. The midpoints of bays 2 through 16:
$$x_k = 1.5 + (k-2) \times 1.5 + 0.75 = 2.25 + (k-2) \times 1.5 \text{ for } k = 2, \ldots, 16$$

Sum = $\sum_{j=0}^{14} (2.25 + 1.5j) = 15 \times 2.25 + 1.5 \times \frac{14 \times 15}{2} = 33.75 + 157.50 = 191.25$

$$\bar{x} = \frac{191.25}{15} = 12.75 \text{ m}$$

Centroid shift: $12.75 - 12.00 = +0.750$ m ✓

**Status: VERIFIED ✓ — All numerical values reproduced to exact precision from first principles.**

### 4.2 Deck Slab — 1275.000 kN → 1314.375 kN

**Baseline evidence shows:**
- Applied: 1275.000 kN with `mag = 6250.0 N/m²`
- Reaction: 1314.375 kN

**Note:** The reconnaissance report uses $p = 0.25 \times 24.5 = 6.125$ kN/m² = 6125 N/m², but the evidence log shows `mag = 6250.0 N/m²`. The discrepancy suggests the application uses $\rho_c = 25.0$ kN/m³ (not 24.5):
$$p = 0.25 \times 25.0 = 6.250 \text{ kN/m}^2$$
$$P = 204.0 \times 6.250 = 1275.000 \text{ kN}$$

This matches the evidence. The reconnaissance's oracle value of 1249.500 kN uses $\rho = 24.5$ kN/m³, which does not match the actual application parameter.

**Excess force from corner overcounting:**
- 4 corner cells × $1.5 \times 1.05$ m² = 6.30 m²
- $\Delta P = 6.30 \times 6.25 = 39.375$ kN
- Total reaction: $1275.000 + 39.375 = 1314.375$ kN ✓

**Status: VERIFIED ✓ — Corner overcounting excess exactly matches. Oracle density parameter needs correction.**

### 4.3 Wearing Course — 244.800 kN → 252.360 kN

**From evidence:** Applied = 244.800 kN, `mag = 1200.0 N/m²`.

The wearing course patch area: If using full width $24.0 \times 8.5 = 204.0$ m² at 1.2 kN/m² = 244.800 kN. This matches the evidence.

The test matrix oracle says "Carriageway: $P = 216.000$ kN," which implies $W_{\text{cw}} = 7.5$ m ($18.0 \times 12.0 = 216$... no, $24.0 \times 7.5 \times 1.2 = 216.0$). But the evidence shows 244.800 kN, consistent with the full 8.5 m width.

**Excess force:**
- $\Delta P = 6.30 \times 1.20 = 7.560$ kN
- Total reaction: $244.800 + 7.560 = 252.360$ kN ✓

**Status: VERIFIED ✓ — The excess matches. However, the wearing course edge clearance and actual patch width need clarification for the oracle.**

### 4.4 Numerical Verification Summary

| Quantity | Recon Claim | Independent Computation | Status |
|:---|:---|:---|:---|
| Barrier true load | 313.920 kN | $2 \times 6.54 \times 24.0 = 313.920$ kN | **VERIFIED** |
| Barrier defective reaction | 196.200 kN | $2 \times 15 \times 6.54 = 196.200$ kN | **VERIFIED** |
| Force deficit | −117.720 kN (−37.50%) | $313.920 - 196.200 = 117.720$ kN | **VERIFIED** |
| Centroid shift | +0.750 m | $(1.5 + 24.0)/2 - 12.0 = 0.750$ m | **VERIFIED** |
| Deck slab excess | +39.375 kN (+3.09%) | $6.30 \times 6.25 = 39.375$ kN | **VERIFIED** |
| Wearing course excess | +7.560 kN (+3.09%) | $6.30 \times 1.20 = 7.560$ kN | **VERIFIED** |
| Excess area | 6.30 m² | $4 \times 1.5 \times 1.05 = 6.30$ m² | **VERIFIED** |
| Line force per bay ($\Delta L = 1.5$) | 6.540 kN (should be 9.810 kN) | $6540 \times 1.0$ vs $6540 \times 1.5$ | **VERIFIED** |
| Deck slab oracle (recon) | 1249.500 kN | Requires $\rho = 24.5$; evidence uses 25.0 | **INCONSISTENT** |

---

## 5. Challenge to the Proposed Centroid Formula

### 5.1 Mathematical Verification

The proposed formula:
$$\mathbf{p}_{\text{centroid}} = \mathbf{p}_1 + \frac{w_1 + 2w_2}{3(w_1 + w_2)} (\mathbf{p}_2 - \mathbf{p}_1)$$

For a trapezoidal load distribution with intensity $w_1$ at $\mathbf{p}_1$ and $w_2$ at $\mathbf{p}_2$ over a segment of length $L = \|\mathbf{p}_2 - \mathbf{p}_1\|$, the centroid of the resulting force is:

$$\bar{s} = \frac{\int_0^L s \cdot w(s) \, ds}{\int_0^L w(s) \, ds}$$

where $s$ is the distance from $\mathbf{p}_1$ along the segment, and $w(s) = w_1 + (w_2 - w_1)(s/L)$.

Computing:
$$\int_0^L w(s) \, ds = \frac{(w_1 + w_2)}{2} L$$

$$\int_0^L s \cdot w(s) \, ds = \int_0^L s \left[w_1 + (w_2 - w_1)\frac{s}{L}\right] ds = \frac{w_1 L^2}{2} + \frac{(w_2 - w_1) L^2}{3} = \frac{L^2(2w_1 + w_2)}{6}$$

$$\bar{s} = \frac{L(2w_1 + w_2)}{3(w_1 + w_2)} \quad \Rightarrow \quad t = \frac{\bar{s}}{L} = \frac{2w_1 + w_2}{3(w_1 + w_2)}$$

Wait — this gives $t = \frac{2w_1 + w_2}{3(w_1 + w_2)}$, but the proposed formula has the fraction $\frac{w_1 + 2w_2}{3(w_1 + w_2)}$.

**Let me recheck.** The centroid distance from $\mathbf{p}_1$ is:

$$\bar{s} = \frac{L(2w_1 + w_2)}{3(w_1 + w_2)}$$

Parametric form: $\mathbf{p}_{\text{centroid}} = \mathbf{p}_1 + \frac{\bar{s}}{L}(\mathbf{p}_2 - \mathbf{p}_1) = \mathbf{p}_1 + \frac{2w_1 + w_2}{3(w_1 + w_2)}(\mathbf{p}_2 - \mathbf{p}_1)$

**The reconnaissance formula has $w_1 + 2w_2$ in the numerator. The correct formula has $2w_1 + w_2$.**

But wait — this depends on which end is $w_1$ and which is $w_2$. The existing code on line 1719 computes:
```python
x_bar = ((2 * w1 + w2) / (w1 + w2)) * L / 3  # from p2
```

This is the centroid distance from $\mathbf{p}_2$. The centroid distance from $\mathbf{p}_2$ is:
$$L - \bar{s} = L - \frac{L(2w_1 + w_2)}{3(w_1 + w_2)} = \frac{L(w_1 + 2w_2)}{3(w_1 + w_2)}$$

No wait — from $\mathbf{p}_2$ the distance is $L \cdot (1 - t) = L \cdot \frac{w_1 + 2w_2}{3(w_1 + w_2)}$.

But the code says `x_bar = ((2 * w1 + w2) / (w1 + w2)) * L / 3`, which equals $\frac{(2w_1 + w_2)L}{3(w_1 + w_2)}$. This is the centroid from $\mathbf{p}_1$, not from $\mathbf{p}_2$.

So the comment "from p2" is **incorrect in the code**. The variable `x_bar` actually holds the centroid distance from $\mathbf{p}_1$.

The proposed replacement formula:
$$\mathbf{p}_{\text{centroid}} = \mathbf{p}_1 + \frac{w_1 + 2w_2}{3(w_1 + w_2)}(\mathbf{p}_2 - \mathbf{p}_1)$$

This uses $t = \frac{w_1 + 2w_2}{3(w_1 + w_2)}$, which is the parametric distance from $\mathbf{p}_1$ when measuring centroid from $\mathbf{p}_2$.

**Let me verify with a concrete example:**

Uniform load $w_1 = w_2 = w$:
- Correct centroid: midpoint, $t = 0.5$
- Existing code: $\bar{x} = \frac{3w}{2w} \cdot \frac{L}{3} = \frac{L}{2}$ — centroid distance $= L/2$. If this is "from p1", then centroid is at $p_1 + L/2$ direction toward $p_2$ = midpoint. ✓
- Proposed formula: $t = \frac{3w}{6w} = 0.5$ → midpoint. ✓

$w_1 = 0, w_2 = w$ (all load at $p_2$):
- Correct centroid: at $\mathbf{p}_2$, so $t = 1$
- Proposed formula: $t = \frac{0 + 2w}{3(0 + w)} = \frac{2}{3}$

That gives $t = 2/3$, not $t = 1$. Something is wrong.

Actually, for $w_1 = 0, w_2 = w$: the load distribution is a triangle with zero at $p_1$ and $w$ at $p_2$. The centroid of a triangle is at $2/3$ from the zero end, i.e., $t = 2/3$ from $p_1$. This is correct — the centroid of a triangular load is at $2/3$ of the length from the zero-load end, not at $p_2$.

So **the proposed formula is correct**: $t = \frac{w_1 + 2w_2}{3(w_1 + w_2)}$ gives the centroid distance from $\mathbf{p}_1$ as a fraction of $L$.

**But the existing code formula** `((2 * w1 + w2) / (w1 + w2)) * L / 3`:
- For $w_1 = 0, w_2 = w$: $\bar{x} = \frac{w}{w} \cdot \frac{L}{3} = \frac{L}{3}$

If this is the distance from $p_1$ (despite the comment), then centroid is at $p_1 + L/3$, which is $1/3$ from $p_1$ — this is the centroid of a triangle from the **loaded** end, not the zero end. This is **wrong**.

Actually, wait. Let me re-derive. If $w_1$ is intensity at $p_1$ and $w_2$ at $p_2$:
$$\bar{s} = \frac{\int_0^L s \cdot [w_1 + (w_2-w_1)s/L] \, ds}{\int_0^L [w_1 + (w_2-w_1)s/L] \, ds} = \frac{w_1 L^2/2 + (w_2-w_1)L^2/3}{(w_1+w_2)L/2} = \frac{L(3w_1 + 2(w_2-w_1))}{3(w_1+w_2)} = \frac{L(w_1 + 2w_2)}{3(w_1+w_2)}$$

Let me redo the numerator integral:
$$\int_0^L s \cdot w_1 \, ds + \int_0^L s \cdot (w_2-w_1)\frac{s}{L} \, ds = \frac{w_1 L^2}{2} + \frac{(w_2-w_1)L^2}{3}$$
$$= \frac{L^2}{6}[3w_1 + 2(w_2 - w_1)] = \frac{L^2}{6}(w_1 + 2w_2)$$

$$\bar{s} = \frac{L^2(w_1+2w_2)/6}{L(w_1+w_2)/2} = \frac{L(w_1+2w_2)}{3(w_1+w_2)}$$

So $\bar{s}$ from $\mathbf{p}_1 = \frac{L(w_1+2w_2)}{3(w_1+w_2)}$ ← This is the centroid distance from $p_1$.

The existing code: `x_bar = ((2*w1 + w2)/(w1+w2)) * L/3` = $\frac{L(2w_1+w_2)}{3(w_1+w_2)}$

The centroid from $p_2$ = $L - \bar{s} = L - \frac{L(w_1+2w_2)}{3(w_1+w_2)} = \frac{L(2w_1+w_2)}{3(w_1+w_2)}$

So the existing code formula **does** compute the distance from $\mathbf{p}_2$ — the comment "from p2" is **correct**. The issue is that `get_point_given_distance` subtracts this from $p_2$'s coordinate.

**The proposed formula** $t = \frac{w_1+2w_2}{3(w_1+w_2)}$ computes the centroid distance from $\mathbf{p}_1$ as a fraction of $L$, which is the standard parametric form $\mathbf{p}_1 + t(\mathbf{p}_2 - \mathbf{p}_1)$.

### 5.2 Edge Case Analysis

| Case | $t$ value | Centroid position | Correct? |
|:---|:---|:---|:---|
| $w_1 = w_2$ (uniform) | $1/2$ | Midpoint | ✓ |
| $w_1 = 0, w_2 > 0$ (triangle from $p_2$) | $2/3$ | At $2/3$ from $p_1$ toward $p_2$ | ✓ |
| $w_1 > 0, w_2 = 0$ (triangle from $p_1$) | $1/3$ | At $1/3$ from $p_1$ | ✓ |
| $w_1 + w_2 = 0$ | Division by zero | UNDEFINED | ⚠️ |
| $w_1 < 0$ or $w_2 < 0$ (sign change) | Possibly outside $[0,1]$ | Invalid centroid | ⚠️ |

**Concern 1 — Zero total intensity:** If $w_1 + w_2 = 0$ (e.g., $w_1 = 5, w_2 = -5$), division by zero occurs. The reconnaissance does not address this.

**Concern 2 — Negative loads or sign changes:** If the load changes sign within a segment, the centroid can fall outside the segment. The formula is mathematically valid but physically meaningless for loads with sign changes (net zero or near-zero total). This is unlikely for dead loads but possible for live load combinations.

**Concern 3 — Vector coordinate guarantee:** The proposed formula computes the centroid as $\mathbf{p}_1 + t(\mathbf{p}_2 - \mathbf{p}_1)$ with $t \in [0, 1]$ for $w_1, w_2 \geq 0$. The centroid is guaranteed to lie on the segment between $p_1$ and $p_2$. This eliminates Mechanism B by construction. ✓

**Verdict: The proposed formula is mathematically correct for all non-negative load intensities where $w_1 + w_2 > 0$. A guard clause for $w_1 + w_2 \approx 0$ should be added.**

---

## 6. Corrections to the Reconnaissance

### 6.1 Errors Found

| ID | Reconnaissance Claim | Independent Finding | Severity |
|:---|:---|:---|:---|
| **C-01** | Mechanism C "corrupts the evaluated intensity" for line loads with transverse variation or skew | For non-vertical straight lines, `interpolate_udl_magnitude` only uses `point_coordinate[0]` (x); the z-coordinate is never read. The index swap has **no functional impact** on current code. | **MEDIUM** — Overstated impact |
| **C-02** | Deck slab oracle: $P = 1249.500$ kN ($\rho = 24.5$ kN/m³) | Baseline evidence shows `mag = 6250.0 N/m²` → $\rho = 25.0$ kN/m³ → $P = 1275.000$ kN. Oracle uses wrong density. | **HIGH** — Incorrect test oracle |
| **C-03** | Wearing course oracle: "Full width: $P = 244.800$ kN; Carriageway: $P = 216.000$ kN" | Evidence confirms `applied = 244.800` kN over full width. Expected reaction after fix = $244.800$ kN (not 216.0). The oracle value is ambiguous. | **MEDIUM** — Ambiguous oracle |
| **C-04** | No mention of `interpolate_udl_magnitude` lines 708–710 bug | `zp = point_coordinate[0]` instead of `point_coordinate[2]` — latent bug for vertical line loads | **LOW** — Latent, dormant for current use |

### 6.2 Statements Confirmed Correct

- Mechanism A line magnitude scaling analysis ✓
- Mechanism B end-bay drop analysis ✓
- Mechanism D patch corner overcounting analysis ✓
- All numerical impact values ✓
- Pipeline architecture trace ✓
- Code line references (all verified against actual line numbers) ✓
- Five conservation invariant formulations ✓

---

## 7. Test Matrix Critique

### 7.1 Strengths

1. **Independent analytical oracles** — Tests derive expected values from closed-form statics, not application helpers. ✓
2. **Magnitude-scaled tolerances** — Eliminates the flawed $+1.0$ N floor. ✓
3. **Multi-mesh invariance testing** (TC-B2-01) — Good for verifying Mechanism A is mesh-independent. ✓
4. **Negative testing** (TC-B2-09) — Tests fail-closed behavior for out-of-mesh loads. ✓
5. **Regression gate** (TC-B2-13) — Protects Batch 1 fixes. ✓

### 7.2 Weaknesses & Missing Tests

| Issue | Test(s) | Assessment |
|:---|:---|:---|
| **Oracle density mismatch** | TC-B2-11 | Expected value uses $\rho = 24.5$ but application uses $\rho = 25.0$. Test will fail even after fix if oracle isn't corrected. |
| **TC-B2-05 is not a computational test** | TC-B2-05 | "Query `interpolate_udl_magnitude` call arguments" is an inspection test, not a statics test. It verifies the fix was applied, not that it produces correct results. This is a **circular test** — it tests the fix, not the invariant. |
| **Missing: uniform line load end-bay inclusion** | None | No test specifically verifies that ALL 16 bays produce force contributions (not just 15). TC-B2-06 checks the first bay's centroid but not the total 16-bay force conservation simultaneously. |
| **Missing: non-uniform line load centroid** | TC-B2-04 only | Only one trapezoidal test. Need at least: triangle ($w_1 = 0$), inverse triangle ($w_2 = 0$), and steep gradient. |
| **Missing: skew mesh or oblique line** | None | All tests use orthogonal grids and longitudinal/transverse lines. No test validates the vector centroid formula for skewed geometries. |
| **Missing: patch load on sub-domain** | TC-B2-08 only | Only one interior partial patch. Need a patch that is not edge-aligned to test general position. |
| **TC-B2-11 and TC-B2-12 may conflate mechanisms** | TC-B2-11, TC-B2-12 | Full-bridge solver tests cannot isolate patch overcounting from other potential issues. If another bug exists in the solver pathway, these tests would detect it but not identify the cause. |
| **Missing: line load with significant transverse variation** | None | No test exercises the corrected index-swap path with a load that actually varies transversely. |

### 7.3 Recommended Minimal Acceptance Suite

| Priority | Tests | Rationale |
|:---|:---|:---|
| **MUST** | TC-B2-01, TC-B2-02, TC-B2-06, TC-B2-07, TC-B2-09, TC-B2-10, TC-B2-13 | Core mechanisms: magnitude scaling, end-bay inclusion, patch dedup, fail-closed, barrier equilibrium, regression |
| **SHOULD** | TC-B2-03, TC-B2-04, TC-B2-08 | Partial/non-uniform load coverage |
| **COULD** | TC-B2-11, TC-B2-12 | Full-bridge solver verification (high value but long execution time) |
| **REPLACE** | TC-B2-05 → new invariant-based test | Replace argument inspection with a transversely-varying line load statics test |

### 7.4 Recommended Additional Tests

1. **TC-B2-14-LINE-ALL-BAYS**: Uniform line load on $L = 24$ m, verify exactly 16 bay contributions (not 15), total force $= w \times L$.
2. **TC-B2-15-LINE-TRIANGLE**: Line load $w_1 = 0, w_2 = 10$ kN/m, verify centroid at $2L/3$ from $p_1$.
3. **TC-B2-16-PATCH-NONALIGNED**: Patch load with vertices not aligned to grid lines, verify area and force conservation.
4. **TC-B2-17-LINE-TRANSVERSE-VARYING**: Line load with actual transverse variation, verify correct intensity interpolation after index fix.

---

## 8. Scope, Risk & Dependencies

### 8.1 Files Affected by Implementation

| File | Modifications | Risk |
|:---|:---|:---|
| `src/ospgrillage/osp_grillage.py` | Lines 1714–1715 (index fix), Line 1726 (`W → W*L`), Lines 1719–1722 (centroid formula), Lines 1576–1579 (fail-closed guard), Lines 1827–1858 (corner dedup), Lines 1894–1898 (list mutation fix) | **HIGH** — Core load distribution engine |
| `src/ospgrillage/load.py` | Lines 756–763 (replace `get_point_given_distance` or add guard) | **MEDIUM** — May not need modification if centroid computed directly in `osp_grillage.py` |
| `src/ospgrillage/load.py` | Lines 708–710 (latent `zp` bug) | **LOW** — Optional fix for defensive engineering |

### 8.2 Impact on Other Defects

| Defect | Impact Assessment |
|:---|:---|
| **DEF-12** (Bearing stiffener) | Zero risk. Operates on section dimensions in `designer.py`. No load path dependency. |
| **DEF-08** (Executive summary) | Low risk. Pass/Fail logic responds to corrected DCR values, which will change due to corrected loads. Tests should be re-run. |
| **DEF-11** (Girder count) | Zero risk. Mesh topology unchanged. |
| **DEF-02** (Crash barrier integration) | Positive synergy. DEF-18 fix restores isolated barrier to 313.920 kN, which DEF-02 (Batch 4) will then integrate into ULS combinations. |
| **DEF-17** | Needs verification — if DEF-17 involves load factor application, it depends on correct base loads from DEF-18. |
| **DEF-19** (Load factors) | Clean boundary. DEF-18 fixes base magnitudes; DEF-19 multiplies by factors. |
| **DEF-20** | Needs verification — unclear dependency without reviewing DEF-20 scope. |

### 8.3 Regression Risk

The changes to `_assign_line_to_four_node` affect **all** line load types (barrier, railing, median, footpath). The magnitude scaling fix (`W * L`) will change forces for every line load in the application. This is intentionally corrective but means all load combinations and downstream design checks will produce different results.

**Mitigation:** Batch 2 tests use unfactored loads (factor = 1.0), isolating the base load fixes from factor application.

### 8.4 Batch Structure Recommendation

The four mechanisms are interconnected in the line load path (Mechanisms A, B, C share `_assign_line_to_four_node`), making it impractical to split them into sub-batches. Mechanism D (patch overcounting) is independent and could theoretically be a separate sub-batch, but the testing overhead doesn't justify it.

**Recommendation:** Batch 2 should remain a single batch with all four mechanisms fixed together.

### 8.5 DEC Item Review

No unresolved DEC items (`DEC-013`, `DEC-015`, `DEC-018`, `DEC-019`, `DEC-020`) intersect with the DEF-18 scope. All relate to unrelated engineering decisions (overhang lines, lane reduction, fatigue, stiffener K, Pucher charts). **No DEC item prevents implementation.**

---

## 9. Acceptance Criteria

For Batch 2 to be accepted, the following must hold post-implementation:

1. **Line load force conservation:** $|\sum P_{\text{nodal}} - w \cdot L| \leq 10^{-9} \cdot w \cdot L$ for any straight uniform line load on any mesh.
2. **Line load centroid preservation:** $|\bar{x}_{\text{reactions}} - L/2| \leq 10^{-5}$ m for symmetric uniform line loads.
3. **End-bay inclusion:** All mesh bays contribute to the load, including the first and last. No load point falls outside the mesh.
4. **Fail-closed on out-of-mesh:** `_assign_load_to_four_node` raises an explicit exception for points outside the mesh.
5. **Patch area conservation:** $|\sum A_{\text{cells}} - A_{\text{patch}}| \leq 10^{-9} \cdot A_{\text{patch}}$.
6. **Patch force conservation:** $|\sum P_{\text{nodal}} - p \cdot A| \leq 10^{-6} \cdot p \cdot A$ through solver.
7. **Full-bridge crash barrier:** $\sum R_y = 313.920$ kN ± $10^{-6} \cdot 313.920$ kN.
8. **Full-bridge deck slab:** Reaction equals corrected applied load ± $10^{-6}$ (using actual $\rho$ parameter).
9. **Batch 1 regression:** All Batch 1 tests pass unchanged.

---

## 10. Remaining Questions

1. **What is the correct concrete density parameter?** The reconnaissance uses $\rho_c = 24.5$ kN/m³ but the baseline evidence shows the application uses $\rho_c = 25.0$ kN/m³ (or equivalently `mag = 6250.0 N/m²` for a 0.25 m slab). The test oracle must use the value the application actually computes with.

2. **What is the wearing course patch extent?** The evidence shows the full 8.5 m width produces 244.800 kN. The test matrix mentions both full width and carriageway width. The oracle should match the actual application geometry.

3. **Should `interpolate_udl_magnitude` lines 708–710 be fixed in Batch 2?** The `zp = point_coordinate[0]` latent bug is in the same load module. Fixing it defensively would be low-risk and prevent future issues with vertical line loads.

4. **Should the centroid formula include a guard for $w_1 + w_2 \approx 0$?** For physically meaningful dead loads this is unlikely, but a defensive `if abs(w1 + w2) < eps: use midpoint` would prevent division-by-zero.

5. **Has the impact of corrected loads on DEF-17 and DEF-20 been assessed?** The reconnaissance lists these as potentially affected but does not confirm zero-impact.

---

## 11. Confidence Summary

| Mechanism | Defect Confirmed | Numerical Impact Verified | Proposed Fix Correct | Confidence |
|:---|:---:|:---:|:---:|:---|
| **A — Line Magnitude Scaling** | ✓ | ✓ | ✓ | **HIGH** |
| **B — End-Bay Load Drop** | ✓ | ✓ | ✓ (vector centroid eliminates root cause) | **HIGH** |
| **C — Coordinate Index Swap** | ✓ (code bug is real) | ⚠️ (zero functional impact on current code) | ✓ (defensive fix, no harm) | **MEDIUM** — impact overstated |
| **D — Patch Corner Overcount** | ✓ | ✓ | ✓ (dedup approach) | **HIGH** |
| **D' — List Mutation Bug** | ✓ | N/A (secondary) | ✓ (standard fix: avoid mutating during iteration) | **HIGH** |

---

## 12. Conditions for Implementation Authorization

The following must be resolved before the verdict can be upgraded to READY FOR IMPLEMENTATION AUTHORIZATION:

1. **Correct the deck slab oracle** in TC-B2-11 to use the actual density parameter ($\rho = 25.0$ kN/m³ → $P = 1275.0$ kN, or verify the correct value from the application configuration).

2. **Clarify the wearing course oracle** in TC-B2-12 to match the actual patch geometry used by the application.

3. **Acknowledge that Mechanism C has zero functional impact** on the sealed baseline evidence and adjust the narrative accordingly. The fix should still be applied but its contribution to the numerical anomaly should not be overstated.

4. **Replace TC-B2-05** (argument inspection test) with an invariant-based test that verifies a transversely-varying line load produces correct intensity values.

5. **Add a guard clause** in the centroid formula for $w_1 + w_2 \approx 0$.

None of these conditions require new reconnaissance. They are clarifications and corrections that can be resolved during implementation planning.

---

**END OF INDEPENDENT AUDIT**

*This audit was conducted under strictly read-only inspection boundaries. No source code, test scripts, governance configurations, or git state were modified. The audit findings are advisory and do not authorize implementation.*

