# Sample project file

`sample_24m_composite_plate_girder.osi` is an OsdagBridge project file in YAML, with 572 keys. It was saved from the GUI. It is the input used for the report's end-to-end run and for the full-pipeline checks.

| Parameter | Value |
|:--|:--|
| Span | 24.0 m |
| Carriageway | 7.5 m |
| Skew | 0° |
| Median | none |
| Footpath | none |
| Structure type | Highway Bridge |
| Design type | Optimized |
| Girder steel | E 350A (fy 350, fu 490 MPa, E 200 GPa, G 76.9 GPa) |
| Deck concrete | M40 |
| Location | Ahmednagar, Maharashtra |

**To use it:**

- **In the GUI:** File → Load Input, choose this file, then Design.
- **Headless:** `python testing/scripts/run_full_design_from_osi.py`. On the packaged source, design completes; see `testing/evidence/phase_3/full_design_check/`.
