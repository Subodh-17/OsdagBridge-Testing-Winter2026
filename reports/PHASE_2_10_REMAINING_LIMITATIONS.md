# PHASE 2.10 — Remaining Limitations and Phase 3 Engineering Prerequisites

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_9_FINAL_INDEPENDENT_GATE_AUDIT.md`  

---

## 1. Overview & Purpose

Phase 2.10 has completed comprehensive remediation of all P0, P1, and P2 findings identified in Claude's Phase 2.9 Final Independent Gate Audit (§13):
1. **P0 (Evidence Governance & Process Containment):**
   - Implemented fail-closed evidence validation in `evidence_guard.py` resolving canonical `os.path.realpath`, case-insensitivity across Windows, directory traversal rejection (`..`), and mandatory refusal of populated target directories by default (`allow_existing=False`).
   - Removed silent `ImportError` fallbacks from `run_all_baseline_tests.py`, enforcing hard abort on missing governance symbols.
   - Built OS-level `ProcessLifetimeJob` with Win32 Job Objects (`CREATE_SUSPENDED`, `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, breakaway disallowed) and process accounting querying active process counts.
   - Restored all 4 overwritten Phase 2.8 candidate logs from uncorrupted `_c_naive.log` twins to 100% bit-exact SHA-256 parity, archived overwritten versions, and updated all provenance disclosures.
   - Verified fail-closed behavior with 10 adversarial unit tests in `test_evidence_governance.py` (10/10 PASSED).
2. **P1 (Engineering Physical Oracles):**
   - Reconciled EQ and A02 physical oracles on single engineering values ($\rho_{\text{concrete}} = 24.5\text{ kN/m}^3, W_{\text{cw}} = 7.5\text{ m}, W_{\text{deck}} = 8.5\text{ m}$).
   - Decomposed A02 ULS load assertions into individual component reaction gates (SW: 165.28 kN, DD: 1249.50 kN, DW: 216.00 kN, CB: 313.92 kN), completely eliminating multi-component error cancellation.
   - Tightened EQ load definition and line distribution tolerances to 0.5% (`rel_tol=0.005`) and eliminated production helpers.
   - Derived exact wearing course patch transverse line shares via analytical cell integration: `{0.0: 1.92%, 1.05: 19.63%, 3.183: 28.44%, 5.317: 28.44%, 7.45: 19.63%, 8.5: 1.92%}`.
   - Added independent fixed-input section property cross-check and general asymmetric-flange section oracle fixture to B01.
3. **P2 (Discrimination & Integrity Upgrades):**
   - Upgraded C01 cyclic history to 5 load cases with non-adjacent extrema (+200, +1200 MAX in LC2, +300, -1500 MIN in LC4, +100 kNm) across 3 elements along G1, with asymmetric end moments.
   - Expanded RPT boundary coverage to cross-bracing and end-diaphragms at 0.999 / 1.000 / 1.001 DCR thresholds, and added narrative independence scenarios.
   - Implemented post-manifest verification in both runners, ensuring zero disk drift during execution.

This document records the **formal architectural, specification, and environment limitations** that remain intentionally blocked or constrained prior to Phase 3 application source remediation.

---

## 2. Formally Blocked Specifications (Architectural Blockers)

Three regression tests remain **unconditionally BLOCKED** on the baseline and **BLOCKED / NOT DEMONSTRATED** in the sensitivity matrix. These tests reflect fundamental deficits in upstream engineering specifications that must not be unilaterally invented during test harness construction:

### 2.1 TC-REG-D02-TEMPERATURE-PROPAGATION (DEC-015 / DEF-06)
- **Current Baseline Defect:** `PlateGirder.add_temperature_load()` attempts to read `input_dict.get("temperature_load_kN_m2")`, a key unpopulated by the UI or project setup. Consequently, `temperature_load_case` remains `None`, and thermal effects are completely omitted from finite-element analysis.
- **Specification Deficit:** IRC 6:2017 Clause 215 defines two distinct thermal actions:
  1. *Overall Temperature Rise and Fall (Cl. 215.2):* Uniform axial expansion/contraction strains governed by regional isotherms ($T_{\text{max}}, T_{\text{min}}$) and expansion joint boundary conditions.
  2. *Vertical Temperature Differential / Gradient (Cl. 215.3, Table 10):* Non-linear positive and reverse vertical temperature gradients across the composite steel-concrete cross section.
- **Phase 3 Prerequisite:**
  - Formal ratification by the OsdagBridge technical committee specifying whether thermal analysis models uniform elongation, vertical gradient, or both.
  - Architectural specification of grillage representation: equivalent thermal nodal forces/moments applied to standard beam-column elements versus OpenSees thermal beam-column fiber formulations.

### 2.2 TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS (DEC-018 / DEF-17)
- **Current Baseline Defect:** UI loading options expose `KEY_LL_IRC_CLASS_FATIGUE`, and vendored `ospgrillage` defines `create_fatigue_vehicle()`. However, `vehicle_lane_coordinates()` only routes standard `ClassA` and `Class70R` vehicles. The fatigue vehicle is never analyzed as a moving load, and `PlateGirderAnalysisResults` lacks fatigue load extraction, resulting in placeholder values.
- **Specification Deficit:** IRC 6:2017 Clause 204.6 specifies a single 400 kN fatigue vehicle (4 axles: 60 kN, 120 kN, 110 kN, 110 kN) with fixed axle spacings moving along the centerline of an effective traffic lane, unaccompanied by other live vehicles.
- **Phase 3 Prerequisite:**
  - Implementation specification for an independent single-vehicle fatigue moving-load analysis pass.
  - Formal definition of the fatigue stress extraction interface feeding into `designer.py`'s `stress_range_MPa` demand structure.

### 2.3 TC-REG-GEO-SLAB-SECTION-PROPERTIES (DEC-013 / DEF-14)
- **Current Baseline Defect:** In `BridgeGrillageModel.create_grillage()`, transverse deck slab members are assigned properties of the longitudinal steel girder divided by 2 (`girder/2`, $I_z \approx 0.00367\text{ m}^4$).
- **Specification Deficit:** Transverse grillage members represent physical reinforced concrete deck slab strips whose width corresponds to the longitudinal node spacing ($s \approx 1.5\text{ m}$). Assigning halved steel plate-girder properties is physically ungrounded.
- **Phase 3 Prerequisite:**
  - Engineering decision on transverse member property formulation:
    - *Option A:* Uncracked transformed gross concrete section ($I_{\text{trans}} = b \cdot d_s^3 / (12 \cdot m)$).
    - *Option B:* Cracked concrete section with torsional inertia reduction ($J \approx 0.1 \cdot J_{\text{uncracked}}$).
  - Specification of whether transverse members are defined with concrete Young's modulus $E_{cm}$ or steel-equivalent modular ratio $m = E_s / E_{cm}$.

---

## 3. Platform & Environment Governance Boundaries

### 3.1 POSIX Root Execution Boundary (DEC-023)
- In Unix/Linux containerized environments running as `root` (`UID == 0` or `euid == 0`), the Linux kernel bypasses standard filesystem read-only permissions (`chmod 0555` or `chmod 0444`), allowing root processes to modify files despite read-only mode bits.
- `TC-REG-FS-CLEAN-WORKING-TREE` detects `os.geteuid() == 0` and reports Check 4 and the overall test result as `BLOCKED (DEC-023)`.
- **Phase 3 Prerequisite:** CI/CD runners must execute under a non-root standard user account (e.g. `runner` or `developer`) to ensure OS-level file permission containment.

### 3.2 Win32 Job Object vs POSIX Process Groups
- On Windows, `ProcessLifetimeJob` uses native Win32 Job Objects (`CREATE_SUSPENDED`, `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, breakaway disallowed) and process accounting (`JobObjectBasicAccountingInformation`) to guarantee that all child, grandchild, and detached processes are terminated upon context exit.
- On POSIX, process lifetime containment is managed via `start_new_session=True` with `os.killpg(pgid, signal.SIGKILL)` and subreaper registration where supported.
- Bounded polling (5.0s window, 0.5s intervals) ensures late filesystem mutations are detected before declaring a sandbox clean.

### 3.3 OpenCASCADE Offscreen 3D Viewport
- `TC-REG-CAD-EXPORT-VS-SCREENSHOT` verifies native OpenCASCADE `Viewer3d.ExportToImage` using the local hardware graphic driver.
- In headless CI/CD environments without physical display adapters, a software OpenGL rasterizer (such as Mesa `llvmpipe` or `Xvfb`) must be initialized.

---

## 4. Workstream-Specific Scope Boundaries

| Workstream / Test | Verified Capability | Remaining Physical/Harness Limitation |
|---|---|---|
| **TC-REG-EQ-LOAD-CONSERVATION** | Independent load definition and line distribution verified directly from input keys within 0.5% tolerance across multi-span geometries ($12\text{ m}, 24\text{ m}, 30\text{ m}$). | Solver nodal reactions on baseline grillage model exhibit known FEM discretization errors; input-level and line-level oracles are verified, while solver remediation belongs to Phase 3. |
| **TC-REG-A02-ULS-COMBINATION-SUM** | Component reactions individually asserted (SW, DD, DW, CB) preventing error cancellation; theoretical applied ULS resultant gated within 0.5%. | Baseline OpenSees solver distributes dead loads with component errors (+2.7% SW, +5.2% DD, -37.5% CB, +16.8% DW) netting to -0.06%; baseline correctly reports `BASELINE_FAIL`. |
| **TC-REG-B01-SECTION-PROPERTY-SYNC** | Independent fixed-input cross-check and general asymmetric-flange section oracle fixture added; runtime plate derivation verified within 0.5% / 1.0%. | Plate dimension snapping logic in production (`_girder_section`) remains flawed and must be remediated in Phase 3. |
| **TC-REG-C01-SECTIONAL-STRESS-RANGE** | 5-state cyclic load history with non-adjacent extrema (+200, +1200 MAX in LC2, +300, -1500 MIN in LC4, +100 kNm) across 3 elements along G1, with asymmetric end moments. | Baseline stress extraction subtracts global max/min envelopes instead of element-specific concurrent load case extremes; baseline correctly reports `BASELINE_FAIL`. |
| **TC-REG-RPT-EXEC-SUMMARY-STATUS** | Exact DCR boundaries at 0.999, 1.000, 1.001 across all girders, cross-bracing, and end-diaphragms; narrative independence verified. | Baseline hardcodes "Pass" in `generate_latex_report()`; baseline correctly reports `BASELINE_FAIL`. |
| **TC-REG-FS-CLEAN-WORKING-TREE** | Full repository and cwd snapshotting; kernel-level Win32 Job Object containment; read-only denial verification; 10 adversarial unit tests pass. | POSIX root environment bypasses read-only bit enforcement by kernel design, requiring non-root execution. |

---

## 5. Phase 3 Remediation Roadmap

When authorized to transition to Phase 3 (Application Source Remediation), changes must be executed on a dedicated git branch (`fix/phase-3-remediation`) following a strict single-defect-per-commit discipline:

1. **Commit 1 — Upstream `ospgrillage` Load Scaling (`DEF-01`):** Scale loads properly in `LoadCase.add_load()` and ensure compound load factors are applied to grillage node vectors.
2. **Commit 2 — Grillage Load Distribution Algorithm (`DEF-18`):** Replace discontinuous point projection with exact cell-intersection bilinear distribution for patch and line loads.
3. **Commit 3 — Path Anchoring & Database Isolation (`DEF-10`):** Relocate `weather.sqlite` and user cache writes to OS standard User AppData via `platformdirs`, ensuring repository tree immutability.
4. **Commit 4 — Girder Count Alignment (`DEF-11`):** Update `designer.py` loop bound to use `bridge._girder_count()` instead of `geom.n_l`, eliminating out-of-bounds crashes on skewed bridges.
5. **Commit 5 — Snapped Section Property Synchronization (`DEF-03`):** Synchronize `_girder_section` with snapped plate dimensions and align `dw` in `input_dict`.
6. **Commit 6 — Dynamic Report Executive Summary (`DEF-08`):** Dynamically iterate over `output_dict` component statuses rather than hardcoding "Pass".
7. **Commit 7 — Bearing Stiffener Buckling Slenderness (`DEF-12`):** Compute stiffener buckling slenderness using web tributary strip $r_y = t_w / \sqrt{12}$ and column curve c per IRC 24:2010.
8. **Commit 8 — Structural Steel Density Propagation (`DEF-13`):** Pass `material.girder.density` to line load generation instead of defaulting to hardcoded constants.
9. **Commit 9 — Multi-Point Stress Verification (`DEF-09`):** Evaluate longitudinal bending stresses at both flange tips and web junctions across all critical cross-sections.
10. **Commit 10 — Cyclic Fatigue Stress Range Tracking (`DEF-07`):** Track true concurrent peak-to-peak fatigue stress ranges across all moving load positions.
11. **Commit 11 — Ratified Architectural Blockers (`DEF-06`, `DEF-14`, `DEF-17`):** Implement approved solutions for temperature loads, transverse slab properties, and fatigue vehicle analysis once formally ratified.

---

*Authored by Senior Structural-Engineering QA & Test-Infrastructure Specialist.*  
*Preserved under immutable Phase 2.10 Evidence Governance.*
