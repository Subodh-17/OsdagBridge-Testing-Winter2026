# Full design pipeline check: same input on three code versions

**Command** (from the package root):

```
python testing/scripts/run_full_design_from_osi.py --src <source>/src --out full_design_<commit>.json
```

- **Input:** `submission/osi/sample_24m_composite_plate_girder.osi` (24 m span, 7.5 m carriageway, 0° skew, E 350A girders, M40 deck).
- **Pipeline:** `PlateGirderBridge.design()` runs every stage the GUI Design button runs: layout, grillage, dead/live/wind/seismic loads, analysis, design checks.
- **Environment:** Linux x86_64, Python 3.12.16, OpenSeesPy 3.8.0.0, with the `osdag` conda package for the material and section database.
- **Date run:** 23 Nov 2026.

| Code | Result | Mu applied (kNm) | Vu applied (kN) | Bearing-stiffener web buckling Fcdw (kN) | n_girders |
|:--|:--|--:|--:|--:|:-:|
| `d74f56d` (upstream baseline) | completed | 1521.32 | 225.34 | 134,083.23 | 6 |
| `f555075` (Batches 1–3) | **failed** in live-load generation (out-of-mesh `ValueError`) | – | – | – | – |
| `bbfe14c` (final, packaged) | completed | 2136.30 | 314.42 | 67.22 | 4 |

The differences between baseline and final are the expected effects of the fixes:

| Change | Cause |
|:--|:--|
| Mu and Vu up about 40% | Load factors now reach the solver (DEF-01) and the full barrier load is applied (DEF-18) |
| Fcdw reduced to a physical value | DEF-12 |
| Girder count 6 → 4 | DEF-11 |

Two smaller changes are **not** attributed to a specific fix: fatigue utilisation (196.76 % → 181.56 %) and deflection (22.15 → 22.10 mm).

The `.txt` files hold the console output. The `.json` files hold the complete output dictionaries.
