# PHASE 2.11 — Remaining Limitations and Phase 3 Engineering Prerequisites

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md` (by Claude)  

---

## 1. Overview & Remediation Status

Phase 2.11 has resolved all actionable test harness, evidence governance, process containment, and engineering oracle findings raised in Claude's Phase 2.10 Final Independent Gate Audit:
1. **Historical Evidence Overwrite Resolved:** All four Phase 2.9 candidate logs were restored to bit-exact SHA-256 parity from original twins; overwritten versions were preserved in `preservation/overwritten_phase_2_9_versions/`; forensic incident report published.
2. **Centralized Evidence Write Gateway:** Implemented `safe_open_evidence`, `safe_write_evidence`, and `safe_copy_evidence` in `evidence_guard.py` enforcing write-time canonical realpath validation, TOCTOU symlink/junction defense, traversal checks, and refusal of all historical phase directories (`phase_1d`, `phase_2_baseline`, `phase_2_repaired`, `phase_2_1` through `phase_2_10`).
3. **Cryptographic Manifest & External Run Seal:** File hashes are generated and sealed into `manifest_hashes.json`, and the manifest hash itself is registered externally in `reports/PHASE_2_11_RUN_SEALS.json`. Standalone verification CLI `verify_manifest.py` verifies on-disk files and seals with zero drift.
4. **Kernel-Level Process Containment:** On Windows, enforced assign-before-execute via `CREATE_SUSPENDED` + `AssignProcessToJobObject` with 64-bit ctypes declarations, resuming thread only after assignment. On Linux, enforced session isolation (`start_new_session=True`), process group tracking, and subreaper registration. Extended delayed write probes (3s, 8s, 15s) are cleanly contained.
5. **Engineering Oracles Hardened:**
   - **EQ (DEF-18):** Barrier magnitude and position dynamically derived from `input_dict` (`loading.crash_barrier_load`, `typical_section.barrier_width`); eliminated hardcoded 6.54 kN/m and 0.25 m literals.
   - **A02 (DEF-01 / DEF-02):** Barrier reaction oracle derived directly from raw input keys without production helper dependency.
   - **B01 (DEF-03):** Bottom flange width verified against $b_{fb} = 410.0\text{ mm}$; supported by general asymmetric section formulation.
   - **C01 (DEF-07):** Balanced multi-girder fixture (G1 governing at End $i$ with $2900\text{ kNm}$, G2 governing at End $j$ with $2700\text{ kNm}$) evaluates both element ends, catching both j-end-only (C10) and i-end-only (C11) candidate escapes.
   - **RPT (DEF-08):** Strict boundary checks ($0.999$, $1.000$, $1.001$) and narrative independence.
6. **Adversarial Unit Test Suite:** 22/22 adversarial unit tests pass cleanly in `test_evidence_governance.py`.

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

### 3.3 OpenCASCADE Offscreen 3D Viewport
- `TC-REG-CAD-EXPORT-VS-SCREENSHOT` verifies native OpenCASCADE `Viewer3d.ExportToImage` using the local hardware graphic driver.
- In headless CI/CD environments without physical display adapters, a software OpenGL rasterizer (such as Mesa `llvmpipe` or `Xvfb`) must be initialized.

---

## 4. Workstream-Specific Scope Boundaries

| Workstream / Test | Verified Capability | Remaining Physical/Harness Limitation |
|---|---|---|
| **TC-REG-EQ-LOAD-CONSERVATION** | Independent load definition and line distribution verified directly from input keys within 0.5% tolerance across multi-span geometries ($12\text{ m}, 24\text{ m}, 30\text{ m}$). Dynamic barrier magnitude and position verified. | Solver nodal reactions on baseline grillage model exhibit known FEM discretization errors; input-level and line-level oracles are verified, while solver remediation belongs to Phase 3. |
| **TC-REG-A02-ULS-COMBINATION-SUM** | Component reactions individually asserted (SW, DD, DW, CB) preventing error cancellation; theoretical applied ULS resultant gated within 0.5%; barrier reaction independent from production helpers. | Baseline OpenSees solver distributes dead loads with component errors (+2.7% SW, +5.2% DD, -37.5% CB, +16.8% DW) netting to -0.06%; baseline correctly reports `BASELINE_FAIL`. |
| **TC-REG-B01-SECTION-PROPERTY-SYNC** | Bottom flange width verified against 410 mm; general asymmetric section property formulas verified; independent fixed-input cross-check verified within 0.5% / 1.0%. | Plate dimension snapping logic in production (`_girder_section`) remains flawed and must be remediated in Phase 3. |
| **TC-REG-C01-SECTIONAL-STRESS-RANGE** | Balanced multi-girder fixture (G1 governing at End $i$ with 2900 kNm, G2 governing at End $j$ with 2700 kNm) evaluated across 5 non-adjacent load cases. Catches j-end-only (C10) and i-end-only (C11) candidates. | Baseline stress extraction subtracts global max/min envelopes instead of element-specific concurrent load case extremes; baseline correctly reports `BASELINE_FAIL`. |
| **TC-REG-RPT-EXEC-SUMMARY-STATUS** | Exact DCR boundaries at 0.999, 1.000, 1.001 across all girders, cross-bracing, and end-diaphragms; narrative independence verified. | Baseline hardcodes "Pass" in `generate_latex_report()`; baseline correctly reports `BASELINE_FAIL`. |
| **TC-REG-FS-CLEAN-WORKING-TREE** | Full repository and cwd snapshotting; kernel-level Win32 Job Object containment (`CREATE_SUSPENDED`); read-only denial verification; 22 adversarial unit tests pass. | POSIX root environment bypasses read-only bit enforcement by kernel design, requiring non-root execution. |

---

## 5. Phase 3 Remediation Roadmap

When authorized to transition to Phase 3 (Application Source Remediation), changes must be executed on a dedicated git branch (`fix/phase-3-remediation`) following a strict single-defect-per-commit discipline:
1. **DEF-01 / DEF-02:** Fix upstream `ospgrillage` load factoring and SIDL combination ordering.
2. **DEF-03:** Remediate `PlateGirderBridge._validate_inputs` and synchronize solver section dimensions.
3. **DEF-07:** Implement concurrent load case cyclic stress range extraction evaluating both element ends with consistent sign convention.
4. **DEF-08:** Dynamically link LaTeX report summary narrative and table overall design status to component outputs.
5. **DEF-10:** Anchor database connections to AppData/temp directory and prevent cwd creation.
6. **DEF-11:** Set structural girder count equal to `bridge._girder_count()`.
7. **DEF-12:** Implement web strip column buckling per IS 800:2007 Cl. 8.7.3.1.
8. **DEF-13:** Propagate user-configured steel density to all self-weight line loads.
9. **DEF-18:** Implement bilinear patch integration and non-collinear line load distribution in FEM solver.
