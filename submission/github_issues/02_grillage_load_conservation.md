**Base:** `Nidhikhare12/OsdagBridge`, branch `dev`, commit `d74f56d`
**Module:** vendored `src/ospgrillage/osp_grillage.py`

### What is wrong

Line and patch loads applied to the grillage do not add up to the load that was defined.

**Line loads** (`_assign_line_to_four_node`, about lines 1674–1729):

- The equivalent force of each grid segment is not multiplied by the segment length.
- The equivalent point is placed at `get_point_given_distance(xbar, point_coordinate=p2)`, which always offsets in −x from `p2`. In the first bay (`p1 = 1.5`, `p2 = 0`) the point lands at **x = −0.75 m**, outside the mesh.
- `_assign_load_to_four_node` then finds no grid and silently returns `[]`, so that load is dropped without any error.
- Intensity interpolation uses `[p1[0], 0, p1[1]]`, which is the y index; it should be z (`p1[2]`).

**Patch loads** (`_assign_patch_load`, about lines 1795–1858):

- Cells cut by the patch edges are collected separately from the fully bounded cells, so the **4 corner cells are counted twice**. On a 7×17 mesh: 210 m² is loaded instead of 204 m².
- The duplicate-removal loop pops items from the list it is iterating over.

### How to reproduce

Default 24 m bridge. The two crash barriers are line loads of 6.54 kN/m each, so the expected total is 313.92 kN.

- The force assigned to the grillage and the sum of support reactions are both **196.2 kN, which is 117.72 kN (37.5 %) short**.
- A standalone check with a uniform 1 kN/m line load over 24 m on a 7×13 mesh assigns 45.8 % of the load, and the centroid is shifted by about 1 m.

### Suggested fix

- Use force = mean intensity × segment length.
- Place the resultant along the segment, from `p1` towards `p2`.
- Use the z coordinate for interpolation.
- Raise an error instead of returning `[]` when a load point falls outside the mesh.
- For patches, track visited cells in a set so each cell is integrated once, and do not mutate the list while iterating.

Patches with 17 equilibrium tests are in my submission repository: commits `34cd4bf` and `9e0b588`, files `patches/0004-*` and `0005-*`. The tests cover uniform, partial, trapezoidal, skewed and zero-crossing line loads, patches, the out-of-mesh error, and the full-bridge barrier at 313.920 kN. Reaction residuals are ≤ 1.2e-10 N.
