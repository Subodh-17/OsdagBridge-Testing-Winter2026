**Base:** `Nidhikhare12/OsdagBridge`, branch `dev`, commit `d74f56d`
**Module:** plate girder, `src/osdagbridge/core/bridge_types/plate_girder/designer.py` (bearing-stiffener web buckling, about lines 1645–1690)

### What is wrong

The web buckling capacity in the bearing-stiffener check (row "Brg.Stiff: Web Buckling") is far too high. There are three causes:

1. The radius of gyration is computed from the **stiffener** moment of inertia `Iys`, instead of the web strip (`r = tw/√12`).
2. The Euler stress `fcc` is used directly as the design stress. The IS 800 column curve (Cl. 7.1.2.1) is never applied.
3. The result is not capped at `fy/γm0`.

As a result the row reports PASS ("stiffener not needed") from an inflated capacity.

### How to reproduce

Use the snapped section of a 24 m, 4-girder default design: `tw = 8 mm`, `d = 1304 mm`, `b1 = 101.81 mm`, `fy = 350 MPa`.

| | Value |
|---|---|
| Capacity computed by the code | **214,533.2 kN** |
| Squash load of the same web strip, `A·fy` | 1,918.8 kN |
| Hand calculation, IS 800 Cl. 8.7.3.1 / 7.1.2.1 (KL = 0.7d, r = tw/√12, curve c, α = 0.49, γm0 = 1.10) | **63.40 kN** |

The hand calculation steps are: KL/r = 395.25, λ̄ = 5.263, χ = 0.03304, fcd = 10.51 MPa, A = (b1 + d/2)·tw = 6,030.5 mm².

A second geometry (`tw = 10`, `d = 1000`, `b1 = 100`) gives 370,184 kN, against 158.5 kN expected.

### Suggested fix

```text
r   = tw / sqrt(12)
KL  = 0.7 * d
fcd = chi(curve c, KL/r, fy) * fy / gamma_m0      # IS 800 Cl. 7.1.2.1
A   = (b1 + d/2) * tw
Fcdw = fcd * A
```

A patch implementing this (with a regression test, which then returns 63.40 kN and 158.5 kN) is available as commit `418fd75` in my submission repository, `patches/0001-*.patch`.
