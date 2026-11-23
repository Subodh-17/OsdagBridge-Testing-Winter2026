# Live GUI verification on the final code (bbfe14c), Windows, 23 Nov 2026

These screenshots come from the OsdagBridge desktop GUI (conda env `osdagbridge-py312`), running on the `bbfe14c` source after the Design button was pressed.

| File | Configuration |
|:--|:--|
| `live_gui_config_a_main_window.png` | Span 30 m, carriageway 7.5 m, skew 10°, no median, no footpath |
| `live_gui_config_a_cad_3d.png` | Same run, CAD viewport capture |
| `live_gui_config_b_main_window.png` | Span 25 m, carriageway 7.5 m, skew 10°, median, single-side footpath |
| `live_gui_config_b_cad_3d.png` | Same run, CAD viewport capture |

**What these images show:**

- The inputs are locked, which happens after Design completes.
- The geometry overlay is populated: overall width 8.40 m / 17.68 m and span 30.00 m / 25.00 m.

On `f555075`, the same Design action stops with `ValueError: Point load coordinate ... does not lie within any mesh grid cell` (report §5.1).

**What they do not show:**

- **A rendered 3D model.** The OpenGL viewport is black because the window-grab method cannot capture the OpenGL surface; the same limitation affects Figure 1 of the report.
- **The Output Dock.** It is collapsed.
- **Load-case counts.** None are recorded here.

For a reproducible, non-GUI check of the full design pipeline, see `testing/evidence/phase_3/full_design_check/`.
