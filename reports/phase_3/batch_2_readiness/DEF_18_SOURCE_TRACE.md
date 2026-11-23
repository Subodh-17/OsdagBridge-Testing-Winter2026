# DEF-18 Technical Source Trace

**Document ID:** P3-B2-TR-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation (Batch 2 Readiness)  
**Defect:** DEF-18 — Finite Element Statics Non-Conservation in Grillage Load Distribution  
**Mode:** READ-ONLY Architectural & Algorithmic Trace  
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`  
**Current HEAD:** `eaba0763daaf0a1e908a8b4575f501bb92f07cfb`  
**Baseline Anchor:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  

---

## 1. High-Level Pipeline Architecture

The path of physical structural loads from user input to finite element solver output and design reports flows through five major abstraction tiers across `osdagbridge` and `ospgrillage`:

```
┌────────────────────────────────────────────────────────┐
│ Tier 1: User & Project Inputs                          │
│ Bridge geometry (L, W), cross-section dimensions,      │
│ material densities, component loads (kN/m, kN/m²)      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Tier 2: Bridge Sizing & Placement Orchestration        │
│ plategirderbridge.py (lines 1311–1340, 1991–2065)      │
│ load_placement.py (lines 25–182)                       │
│ analyser.py: BridgeGrillageModel (lines 371–905)       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Tier 3: Load Discretization & Grid Mapping (DEF-18)    │
│ ospgrillage/load.py (lines 728–763)                    │
│ ospgrillage/osp_grillage.py:                           │
│   • _distribute_load_types_to_model (lines 1922–2011)  │
│   • _assign_line_to_four_node (lines 1663–1753)        │
│   • _assign_load_to_four_node (lines 1571–1660)        │
│   • _assign_patch_load (lines 1795–1915)               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Tier 4: OpenSees Solver Execution                      │
│ ospgrillage/osp_grillage.py:                           │
│   • Analysis.add_load_command (lines 2865–2890)        │
│   • Analysis.evaluate_analysis (lines 2891–2941)       │
│   • Results.extract_analysis (lines 3073–3188)         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Tier 5: Result Harvesting, Design & Reporting          │
│ analysis_results.py (lines 1211–1257)                  │
│ designer.py & executive_summary.py                     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Granular Code Path Trace

### Stage 1: Load Definition & Orchestration
- **[plategirderbridge.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py#L1311-L1340)**:
  - `add_dead_loads(self)`: Calls `self.grillage_model` methods in strict sequence:
    - Line 1332: `model.create_self_weight_load()`
    - Line 1333: `model.create_deck_load(slab_thickness_m=deck_t_m)`
    - Line 1334: `model.create_wearing_course_load(thickness_m=wc_t_m, density_kN_m3=wc_rho, partial_safety_factor=1.0)`
    - Line 1335: `model.create_footpath_load()`
    - Line 1336: `model.create_crash_barrier_load(barrier_load_kN_per_m=barrier_load_kN_m)`
    - Line 1337: `model.create_railing_load(railing_load_kN_per_m=railing_load_kN_m)`
    - Line 1338: `model.create_median_load()`
    - Line 1339: `model.create_dead_load_combination(partial_safety_factor=1.0)`
- **[analyser.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/osdagbridge/core/bridge_types/plate_girder/analyser.py)** (`BridgeGrillageModel`):
  - `create_crash_barrier_load()` (lines 672–748): Computes line load magnitude $w = \text{barrier\_load\_kN\_m} \times 1000\text{ N/m}$. Queries `self.load_manager.crash_barrier_load(side)` to obtain `geom.start` and `geom.end`. Creates `p1`, `p2` via `og.create_load_vertex(x, z, p)` and constructs `og.create_load(loadtype="line", point1=p1, point2=p2)`. Appends to `DL_barrier` load case and calls `model.add_load_case(DL_barrier)`.
  - `create_wearing_course_load()` (lines 519–592): Computes overlay intensity $p = t \times \rho \times 1000\text{ N/m}^2$. Queries `self.load_manager.overlay_load()`. Creates vertices $p_1, p_2, p_3, p_4$ and creates `og.create_load(loadtype="patch", ...)`. Appends to `DL_overlay` and calls `model.add_load_case(DL_overlay)`.
  - `create_deck_load()` (lines 435–518): Computes deck intensity $p = t_{\text{slab}} \times \rho_c \times 1000\text{ N/m}^2$. Creates 4-vertex patch over $[0, L] \times [0, W]$.

### Stage 2: Load Placement Geometry
- **[load_placement.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/osdagbridge/core/bridge_types/plate_girder/load_placement.py)**:
  - `CrashBarrier.to_global()` (lines 31–42):
    ```python
    z = self.offset if self.side == "left" else self.bridge.width - self.offset
    return LineLoadGeometry(start=Point(x=0.0, z=z), end=Point(x=self.bridge.span, z=z))
    ```
    Barrier lines span exactly from $x = 0.0$ to $x = L$.
  - `OverlayLoad.to_global()` (lines 55–65):
    Defines rectangular patch with $p_1 = (0.0, c), p_2 = (L, c), p_3 = (L, W-c), p_4 = (0.0, W-c)$.

### Stage 3: Load Discretization & Transformation Engine (DEF-18 Origin)
- **[ospgrillage/osp_grillage.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/ospgrillage/osp_grillage.py)**:
  - `_distribute_load_types_to_model(load_case)` (lines 1922–2011):
    Dispatches each load object in `load_case`:
    - `LineLoading`: calls `_get_line_load_nodes(load_obj)` (lines 1257–1416) then `_assign_line_to_four_node` (lines 1663–1753).
    - `PatchLoading`: calls `_assign_patch_load` (lines 1795–1915).
    - `PointLoad`: calls `_assign_load_to_four_node` (lines 1571–1660).
  
  #### Line Load Code Path & Defects
  - **`_assign_line_to_four_node` (lines 1663–1753)**:
    - Line 1711: Computes segment length $L = \sqrt{(p_1[0]-p_2[0])^2 + (p_1[2]-p_2[2])^2}$.
    - **Defect Line 1714–1715 (Index Swap):**
      ```python
      w1 = line_load_obj.interpolate_udl_magnitude([p1[0], 0, p1[1]])
      w2 = line_load_obj.interpolate_udl_magnitude([p2[0], 0, p2[1]])
      ```
      Passes `p1[1]` (elevation $y = 0$) into the transverse slot instead of `p1[2]` ($z$).
    - Line 1717: Computes average intensity $W = (w_1 + w_2) / 2$.
    - Line 1719: Computes $x_{\text{bar}} = \frac{2w_1 + w_2}{w_1 + w_2} \frac{L}{3}$ from $p_2$.
    - **Defect Lines 1720–1722 (Centroid Direction):**
      ```python
      load_point = line_load_obj.get_point_given_distance(
          xbar=x_bar, point_coordinate=[p2[0], self.y_elevation, p2[2]]
      )
      ```
      Calls `load.py:get_point_given_distance`.
    - **Defect Line 1726 (Magnitude Omission of Length):**
      ```python
      load_str = self._assign_load_to_four_node(
          point=load_point, mag=W, shape_func=line_load_obj.shape_function
      )
      ```
      Passes `mag=W` instead of `mag=W * L`!
    - Contrast with line 1743 in colinear loop:
      `mag = W * L` (colinear loop calculates force correctly, but grid-intersection loop omitted $\times L$).

  - **[ospgrillage/load.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/ospgrillage/load.py)**:
    - **Defect Lines 756–763 in `get_point_given_distance(xbar, point_coordinate)`:**
      ```python
      z_dis = xbar * np.sin(self.angle)
      x_dis = xbar * np.cos(self.angle)
      new_point = [
          point_coordinate[0] - x_dis,
          point_coordinate[1],
          point_coordinate[2] - z_dis,
      ]
      ```
      Subtracts $x_{\text{dis}}$ along $-\hat{x}$. In the first end-bay, $p_2 = 0.0$ and $p_1 = 1.5\text{ m}$. Subtracting $0.75\text{ m}$ from $p_2[0] = 0.0$ yields $x = -0.75\text{ m}$ (outside the mesh).

  - **`_assign_load_to_four_node` (lines 1571–1660)**:
    - **Defect Lines 1576–1579 (Silent Drop):**
      ```python
      grid_nodes, _ = self._get_point_load_nodes(point=point)
      if grid_nodes is None:
          load_str = []
          return load_str
      ```
      When `point` is $x = -0.75\text{ m}$, `grid_nodes` is `None`. The entire end-bay load is silently discarded with zero error or warning.
    - Lines 1614–1637: For points inside a grid, solves $(\eta, \zeta)$, evaluates shape functions $N_v$, and generates nodal load commands:
      `("load", (node_tag, 0, mag * Nv[count], 0, 0, 0, 0), {})`.

  #### Patch Load Code Path & Defects
  - **`_assign_patch_load` (lines 1795–1915)**:
    - Lines 1802–1824: Iterates over `bound_grid` (fully interior cells), computes $mag = A \cdot \bar{p}$, and calls `_assign_load_to_four_node`.
    - Lines 1827–1854: Queries 4 patch edges independently via `_get_line_load_nodes`, merging them into `merged`.
    - **Defect 1 (Corner Double-Counting):** Corner cells are intersected by two adjacent edges and added multiple times, causing $4 \times \Delta A$ excess load.
    - **Defect 2 (Mutation during Iteration, lines 1894–1898):**
      ```python
      for count, point in enumerate(p_list):
          dupe = [point == val for val in p_list]
          if sum(dupe) > 1:
              p_list.pop(count)
      ```
      Calling `p_list.pop(count)` inside an `enumerate` loop mutates the list length, skipping candidate duplicate checks.

### Stage 4: OpenSees Solver Execution
- **[ospgrillage/osp_grillage.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/ospgrillage/osp_grillage.py)**:
  - `Analysis.add_load_command()` (lines 2865–2890):
    Dispatches `ops.load(node_tag, fx, fy * load_factor, fz, mx * load_factor, my, mz * load_factor)`.
  - `Analysis.evaluate_analysis()` (lines 2891–2941):
    Calls `ops.analyze(step)`. Captures displacements (`ops.nodeDisp`) and element forces (`ops.eleForce`).
  - `Results.extract_analysis()` (lines 3073–3188):
    Gathers member end forces and nodal displacements, assembling them into an `xarray.Dataset`.

### Stage 5: Post-Processing & Reaction Harvesting
- **[analysis_results.py](file:///F:/FOSSEE%20internship/source/OsdagBridge/src/osdagbridge/core/bridge_types/plate_girder/analysis_results.py)**:
  - `_get_reactions_df(load_case)` (lines 1211–1241):
    Extracts end shears $V_y$ from the first and last elements of each girder:
    - $R_a = \text{forces}[\text{Element}=eid_s, \text{Component}=c_{ra}] / 1000$
    - $R_b = -\text{forces}[\text{Element}=eid_e, \text{Component}=c_{rb}] / 1000$
  - OpenSees solver global reactions can also be audited directly via `ops.reactions()` and `-float(ops.nodeReaction(node, 2))`.

---

## 3. Summary of Exact Failure Sites

| Component / Sub-Defect | File | Line Range | Exact Defect Mechanism |
|:---|:---|:---:|:---|
| **Line Magnitude Scaling** | `src/ospgrillage/osp_grillage.py` | 1717–1728 | Passes `mag=W` instead of `mag = W * L`, underpredicting line force by $1/\Delta L$. |
| **End-Bay Out-of-Mesh Drop** | `src/ospgrillage/load.py`<br>`src/ospgrillage/osp_grillage.py` | 756–763<br>1576–1579 | Subtracts $x_{\text{dis}}$ along $-\hat{x}$ causing point to land at $x = -0.75\text{ m}$; silently drops with `return []`. |
| **Coordinate Index Swap** | `src/ospgrillage/osp_grillage.py` | 1714–1715 | Passes `p1[1]` (elevation $y$) instead of `p1[2]` (transverse $z$) into `interpolate_udl_magnitude`. |
| **Patch Corner Overcount** | `src/ospgrillage/osp_grillage.py` | 1827–1858 | 4 corner cells double-counted across multiple edge intersection dicts ($+39.375\text{ kN}$ on deck slab). |
| **List Mutation Bug** | `src/ospgrillage/osp_grillage.py` | 1894–1898 | Calls `p_list.pop(count)` while iterating `enumerate(p_list)`, corrupting deduplication. |
