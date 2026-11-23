# DEF-18 Proposed Verification & Validation Test Matrix (Revision 2.0)

**Document ID:** P3-B2-TM-002 (Supersedes P3-B2-TM-001)  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation (Batch 2 Readiness)  
**Defect:** DEF-18 — Finite Element Statics Non-Conservation in Grillage Load Distribution  
**Mode:** READ-ONLY Technical Specification (Pre-Implementation Revision 2.0)  
**Audit Reconciliation:** Resolves Conditions 1, 2, 4, and 5 of [CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_2_readiness/CLAUDE_DEF_18_INDEPENDENT_READINESS_AUDIT.md)  

---

## 1. Test Architecture & Governing Principles

To guarantee that Batch 2 remediation eliminates all statics non-conservation anomalies without masking defects through circular helpers, inspection-only assertions, or artificial tolerances, this revised test suite adheres to five governing principles:

1. **Independent Analytical Oracles:** All expected forces, moments, and centroids are derived from closed-form Newtonian statics and integral calculus, completely independent of application helper functions.
2. **Magnitude-Scaled Relative Tolerances:** Relative force tolerance is strictly gated at $\le 10^{-9} \cdot P_{\text{total}}$ for clean discretization schemes, with a strict absolute limit of $10^{-6} \cdot P_{\text{total}}$ across full grillage OpenSees solver executions. The unscaled $+1.0\text{ N}$ constant floor (Claude finding R2-07) is strictly prohibited.
3. **Multi-Mesh & Multi-Discretization Invariance:** Tests evaluate multiple longitudinal and transverse mesh densities ($\Delta x = 1.0\text{ m}, 1.5\text{ m}, 2.0\text{ m}$) to verify that force conservation is invariant under mesh refinement.
4. **Boundary Condition & Discretization Robustness:** Checks encompass symmetric, asymmetric, partial, triangular, trapezoidal, and skewed loads, boundary bays, and interior grids.
5. **Fail-Closed Negative Testing:** Out-of-mesh load placement must raise explicit exceptions rather than silently dropping load vectors.

---

## 2. Revised Batch 2 Test Matrix

| Test Identifier | Category | Structural Invariant | Test Fixture & Parameters | Expected Analytical Value | Validation Method | Failure Criteria (Baseline / Anomaly) |
|:---|:---|:---|:---|:---|:---|:---|
| **`TC-B2-01-LINE-SCALE-UNIFORM`** | Unit / Statics | Force Conservation across Mesh Densities | 1D/2D Grillage ($L=20\text{ m}$), $w = 10\text{ kN/m}$ across $\Delta x = 1.0, 1.5, 2.0\text{ m}$ | $P_{\text{total}} = 200.000\text{ kN}$ identically on all meshes | Sum of distributed nodal forces $\sum P_i$ | Fails if $P \ne 200\text{ kN}$ (baseline evaluated $P = 200/\Delta x\text{ kN}$) |
| **`TC-B2-02-LINE-SMALL-MAG`** | Unit / Boundary | Force Conservation at Micro-Loads | $L=24\text{ m}$, $w = 1.0\text{ N/m}$ ($16 \times 1.5\text{ m}$ bays) | $P_{\text{total}} = 24.000000\text{ N}$, $\bar{x} = 12.000\text{ m}$ | Direct summation with magnitude-scaled tolerance $\le 10^{-9} \cdot P$ | Fails if $P = 23\text{ N}$ (baseline dropped first bay, masked by $+1\text{ N}$ floor) |
| **`TC-B2-03-LINE-ASYMMETRIC-PARTIAL`** | Unit / Statics | Equilibrium & Longitudinal Centroid | $L=24\text{ m}$, partial line $w = 5\text{ kN/m}$ from $x = 4\text{ m}$ to $16\text{ m}$ ($L_w = 12\text{ m}$) | $P = 60.000\text{ kN}$, $\bar{x} = 10.000\text{ m}$ | Reaction sum $\sum R_y$ and first moment $\sum (x_i R_{y,i})/P$ | Fails if $R_y \ne 60\text{ kN}$ or $|\bar{x} - 10| > 10^{-6} \cdot L$ |
| **`TC-B2-04-LINE-TRAPEZOIDAL`** | Unit / Statics | Non-Uniform Intensity Integration | $L=20\text{ m}$, $w(x) = 2.0 + 0.3x\text{ kN/m}$ ($w_1 = 2, w_2 = 8\text{ kN/m}$) | $P = \int_0^{20} w(x)dx = 100.000\text{ kN}$, $\bar{x} = 12.000\text{ m}$ | Discretized point load sum and centroid | Fails if $P \ne 100\text{ kN}$ or $\bar{x} \ne 12.000\text{ m}$ |
| **`TC-B2-05-LINE-SKEW-VARYING`** *(Redesigned)* | Unit / Geometry & Statics | Skew Line Force & Vector Centroid Conservation | Skew line from $(0.0, 0.0, 1.0\text{ m})$ to $(20.0, 0.0, 5.0\text{ m})$, $w_1 = 4.0, w_2 = 12.0\text{ kN/m}$, $L_{\text{skew}} = 20.396078\text{ m}$ | $P = 163.168624\text{ kN}$, $\bar{x} = 11.666667\text{ m}$, $\bar{z} = 3.333333\text{ m}$ | Sum of nodal forces $\sum P_i$ and reaction centroid $(\bar{x}, \bar{z})$ | Fails if $P \ne 163.169\text{ kN}$ or $\bar{z} \ne 3.333\text{ m}$ (exposes magnitude scaling and centroid errors; replaces circular argument inspection) |
| **`TC-B2-06-LINE-FIRST-BAY-OFFSET`** | Unit / Boundary | Boundary Cell Centroid Placement | First end bay $x \in [0.0, 1.5\text{ m}]$, $w = 6.54\text{ kN/m}$ | $P_{\text{bay}} = 9.810\text{ kN}$, load point at $x = 0.750\text{ m}$ (inside cell) | Inspect generated OpenSees load command coordinates | Fails if point lands at $x = -0.75\text{ m}$ and returns `[]` |
| **`TC-B2-07-PATCH-CORNER-DEDUP`** | Unit / Integration | Patch Area Conservation (No Overcounting) | Rectangular deck $20\text{ m} \times 10\text{ m}$, uniform patch $p = 2.0\text{ kN/m}^2$ | $P_{\text{total}} = 400.000\text{ kN}$, evaluated cell area $\sum A_k = 200.0\text{ m}^2$ | Sum of cell areas and total patch load commands | Fails if area $> 200\text{ m}^2$ due to corner cell duplication |
| **`TC-B2-08-PATCH-INTERIOR-PARTIAL`** | Unit / Integration | Interior Patch Boundedness | Partial patch $x \in [6, 18\text{ m}], z \in [2, 6.5\text{ m}]$ ($A = 54\text{ m}^2$), $p = 1.5\text{ kN/m}^2$ | $P = 81.000\text{ kN}$, $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$ | Nodal force summation and centroid | Fails if $P \ne 81\text{ kN}$ or corner cells double counted |
| **`TC-B2-09-NEGATIVE-OUT-OF-MESH`** | Unit / Robustness | Fail-Closed Exception on Out-of-Mesh Load | Point load applied at $x = -1.0\text{ m}$ or line load ending at $x = 26.0\text{ m}$ ($L=24\text{ m}$) | Explicit `ValueError` or `RuntimeError` raised | `pytest.raises(ValueError)` | Fails if function silently returns `[]` without error |
| **`TC-B2-10-FE-BARRIER-EQUILIBRIUM`** | Integration / Solver | Full-Bridge Crash Barrier Static Equilibrium | Sealed bridge ($24\text{ m} \times 8.5\text{ m}$), 2 barrier lines ($2 \times 6.54\text{ kN/m}$) | $\sum R_y = 313.920\text{ kN}$, $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$ | OpenSees FE solve: `ops.reactions()`, sum node reactions | Baseline gave $196.200\text{ kN}$ ($-37.5\%$) and $\bar{x} = 12.750\text{ m}$ |
| **`TC-B2-11-FE-DECK-SLAB-EQUIL`** *(Reconciled)* | Integration / Solver | Full-Bridge Deck Slab Static Equilibrium | Sealed bridge ($24\text{ m} \times 8.5\text{ m}$), $t = 0.25\text{ m}$, application default $\rho_c = 25.0\text{ kN/m}^3$ | $\sum R_y = \mathbf{1275.000\text{ kN}}$, $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$ | OpenSees FE solve: `ops.reactions()` | Baseline gave $1314.375\text{ kN}$ ($+3.09\%$ overcount). Reconciled from $1249.5\text{ kN}$. |
| **`TC-B2-12-FE-OVERLAY-EQUIL`** *(Reconciled)* | Integration / Solver | Full-Bridge Wearing Course Static Equilibrium | Sealed bridge ($24\text{ m} \times 8.5\text{ m}$), $t = 0.05\text{ m}$, $\rho_{\text{wc}} = 24.0\text{ kN/m}^3$, full deck width ($c = 0.0\text{ m}$) | $\sum R_y = \mathbf{244.800\text{ kN}}$, $\bar{x} = 12.000\text{ m}$, $\bar{z} = 4.250\text{ m}$ | OpenSees FE solve: `ops.reactions()` | Baseline gave $252.360\text{ kN}$ ($+3.09\%$ overcount). Reconciled from $216.0\text{ kN}$. |
| **`TC-B2-13-REGRESSION-BATCH1`** | Regression / Governance | Batch 1 Acceptance Invariance | Current committed codebase on branch `fix/phase-3-engineering-remediation` | DEF-12: PASS ($63.4\text{ kN}$), DEF-08: PASS (74/74), DEF-11: PASS (4 girders) | Run Batch 1 test suite | Any regression or status change from PASS fails the batch |
| **`TC-B2-14-LINE-ALL-BAYS`** *(New)* | Unit / Coverage | Complete Longitudinal Bay Contribution | $L = 24.0\text{ m}$, 16 bays of $1.5\text{ m}$, uniform line $w = 10\text{ kN/m}$ | Exactly 16 discrete bay force contributions; total $P = 240.000\text{ kN}$ | Count discrete cell assignments and sum force | Fails if bay count $< 16$ (e.g. 15 bays in baseline) |
| **`TC-B2-15-LINE-TRIANGLE`** *(New)* | Unit / Statics | Triangular Load Centroid Mechanics | $L = 15.0\text{ m}$, $w_1 = 0.0, w_2 = 12.0\text{ kN/m}$ (peak at $\mathbf{p}_2$) | $P = 90.000\text{ kN}$, $\bar{x} = \frac{2}{3} L = 10.000\text{ m}$ from $\mathbf{p}_1$ | Discretized point load sum and centroid | Fails if $\bar{x} \ne 10.000\text{ m}$ ($t \ne 2/3$) |
| **`TC-B2-16-PATCH-NONALIGNED`** *(New)* | Unit / Integration | Arbitrary Boundary Patch Conservation | Deck $20\text{ m} \times 10\text{ m}$, non-grid-aligned patch $x \in [3.7, 16.3\text{ m}], z \in [1.2, 8.8\text{ m}]$, $p = 2.5\text{ kN/m}^2$ | Area $A = 12.6 \times 7.6 = 95.760\text{ m}^2$, $P = 239.400\text{ kN}$ | Discretized patch force sum | Fails if $|P - 239.4| > 10^{-6} \cdot P$ |
| **`TC-B2-17-ZERO-CROSSING-FAILSAFE`** *(New)* | Unit / Kinematics | Singularity & Zero-Crossing Handling | Line segment $L = 10\text{ m}$, opposing signs $w_1 = +5.0, w_2 = -5.0\text{ kN/m}$ | Subdivided at $s_0 = 5.0\text{ m}$ into two lobes ($R_+ = +12.5\text{ kN}, R_- = -12.5\text{ kN}$) | Check sub-segment generation without division by zero | Fails if zero division occurs or centroid placed outside segment |

---

## 3. Mathematical Oracle Derivations (Reconciled)

### 3.1 Reconciled Concrete Deck Slab Oracle (`TC-B2-11`)
- **Physical Material Assumption:**
  In the baseline application, `BridgeGrillageModel.create_deck_load()` (in `src/osdagbridge/core/bridge_types/plate_girder/analyser.py`, line 466) defines:
  $$\rho_c = \text{WET\_CONCRETE\_DENSITY\_kN\_m3} = \mathbf{25.0\text{ kN/m}^3}$$
  This represents standard wet reinforced concrete per IRC 6:2017 Table 1 (25 kN/m³ for RCC including 1–2% steel).
  `PlateGirderBridge.add_dead_loads()` invokes `model.create_deck_load(slab_thickness_m=deck_t_m)` without overriding `concrete_density_kN_m3`, thereby selecting the application default of $25.0\text{ kN/m}^3$.
  *(Note: Dynamic propagation of user-configured `material.deck.density = 24.5 kN/m³` is the designated scope of DEF-13 in Batch 5. Prior to Batch 5, Batch 2 must test the active application default parameter without conflating Batch 5 scope).*
- **Closed-Form Physical Load:**
  $$\text{Span } L = 24.0\text{ m}, \quad \text{Width } W = 8.5\text{ m} \implies \text{Area } A = 204.0\text{ m}^2$$
  $$\text{Slab Thickness } t = 0.25\text{ m}$$
  $$\text{Surface Pressure } p = t \times \rho_c = 0.25\text{ m} \times 25.0\text{ kN/m}^3 = 6.250\text{ kN/m}^2 = 6250.0\text{ N/m}^2$$
  $$P_{\text{DD}} = A \times p = 204.0\text{ m}^2 \times 6.250\text{ kN/m}^2 = \mathbf{1275.000\text{ kN}}$$
  $$\bar{x} = 12.000\text{ m}, \quad \bar{z} = 4.250\text{ m}$$
- **Reconciled Acceptance Gate:**
  $$|\sum R_y - 1275.000\text{ kN}| \le 10^{-6} \times 1275.000\text{ kN} \approx 0.001275\text{ kN}$$
  $$(1249.500\text{ kN}\text{ from Revision 1 is formally retired for the Batch 2 default fixture}).$$

### 3.2 Reconciled Wearing Course Oracle (`TC-B2-12`)
- **Physical Geometry Assumption:**
  In `PlateGirderBridge.add_dead_loads()` (line 1334), `create_wearing_course_load()` is invoked without `edge_clearance`, defaulting to `edge_clearance = 0.0`.
  In `load_placement.py:OverlayLoad.to_global()` (lines 60–65), setting `c = 0.0` extends the rectangular patch across the **entire deck width of 8.5 m** ($z \in [0.0, 8.5\text{ m}]$).
  *(Note: Restricting wearing course to the carriageway width of 7.5 m would require an application geometry code change that is not part of DEF-18. DEF-18 evaluates statics conservation over whatever geometry the application defines).*
- **Closed-Form Physical Load:**
  $$\text{Span } L = 24.0\text{ m}, \quad \text{Deck Width } W = 8.5\text{ m} \implies \text{Area } A = 204.0\text{ m}^2$$
  $$\text{Thickness } t = 0.05\text{ m}, \quad \text{Bituminous Density } \rho_{\text{wc}} = 24.0\text{ kN/m}^3$$
  $$\text{Surface Pressure } p = 0.05\text{ m} \times 24.0\text{ kN/m}^3 = 1.200\text{ kN/m}^2 = 1200.0\text{ N/m}^2$$
  $$P_{\text{DW}} = A \times p = 204.0\text{ m}^2 \times 1.200\text{ kN/m}^2 = \mathbf{244.800\text{ kN}}$$
  $$\bar{x} = 12.000\text{ m}, \quad \bar{z} = 4.250\text{ m}$$
- **Reconciled Acceptance Gate:**
  $$|\sum R_y - 244.800\text{ kN}| \le 10^{-6} \times 244.800\text{ kN} \approx 0.000245\text{ kN}$$
  $$(216.000\text{ kN}\text{ is retained only as an independent partial-patch unit test with explicit } z \in [0.5, 8.0\text{ m}]).$$

### 3.3 Redesigned Independent Skew Line Oracle (`TC-B2-05`)
- **Test Fixture:**
  Non-orthogonal line load spanning from $\mathbf{p}_1 = (0.0, 0.0, 1.0\text{ m})$ to $\mathbf{p}_2 = (20.0, 0.0, 5.0\text{ m})$ across an orthogonal grillage mesh ($20\text{ m} \times 8\text{ m}$, grid spacing $\Delta x = 2.0\text{ m}, \Delta z = 1.0\text{ m}$).
  Line length:
  $$L_{\text{skew}} = \sqrt{(20.0 - 0.0)^2 + (5.0 - 1.0)^2} = \sqrt{400 + 16} = \sqrt{416} \approx 20.396078\text{ m}$$
  Linear intensity gradient: $w_1 = 4.0\text{ kN/m} = 4000\text{ N/m}$ at $\mathbf{p}_1$, increasing to $w_2 = 12.0\text{ kN/m} = 12000\text{ N/m}$ at $\mathbf{p}_2$.
- **Analytical Integral Derivations:**
  $$P_{\text{analytical}} = \int_0^{L_{\text{skew}}} \left(w_1 + \frac{w_2 - w_1}{L_{\text{skew}}} s\right) ds = \left(\frac{w_1 + w_2}{2}\right) L_{\text{skew}} = 8.0\text{ kN/m} \times 20.396078\text{ m} = \mathbf{163.168624\text{ kN}}$$
  Longitudinal centroid from moment of area:
  $$\bar{x} = x_1 + \left(\frac{w_1 + 2w_2}{3(w_1 + w_2)}\right) (x_2 - x_1) = 0.0 + \left(\frac{4.0 + 24.0}{3(16.0)}\right) (20.0) = \frac{28}{48} \times 20.0 = \frac{7}{12} \times 20.0 = \mathbf{11.666667\text{ m}}$$
  Transverse centroid from moment of area:
  $$\bar{z} = z_1 + \left(\frac{w_1 + 2w_2}{3(w_1 + w_2)}\right) (z_2 - z_1) = 1.0 + \left(\frac{7}{12}\right) (4.0) = 1.0 + 2.333333 = \mathbf{3.333333\text{ m}}$$
- **Why This Test Eliminates Circularity:**
  The test solves the grillage finite element model and verifies that the sum of support reactions equals $163.168624\text{ kN}$ ($\text{tol} \le 10^{-6}$) and reaction moments balance about both axes ($|dx| \le 10^{-5}\text{ m}, |dz| \le 10^{-5}\text{ m}$). It inspects zero application functions or internals.
- **Why It Fails Under Original Defect:**
  1. Under Mechanism A, intensity $W$ is assigned without $\times \Delta L_k$, reducing total reaction by $\approx 50\%$.
  2. Under Mechanism B, boundary point subtraction shifts the centroid and risks out-of-mesh coordinate drop.
- **Scope of Validation & Mechanism C Boundary:**
  - `TC-B2-05` validates physical line-load force and centroid conservation for its specified fixture.
  - It validates the direct vector centroid behavior (including transverse centroid $\bar{z} = 3.333\text{ m}$).
  - It exposes relevant magnitude scaling and centroid-placement errors within its fixture.
  - **No claim to detect Mechanism C:** `TC-B2-05` does **NOT** detect Mechanism C because `interpolate_udl_magnitude` uses strictly `xp = point_coordinate[0]` for all non-vertical lines ($v[0] \ne 0$). Coordinate-slot discrepancies (index 1 vs 2) have no functional effect in this test. Mechanism C is a defensive code-correctness fix verified via inspection, not functional statics testing.
