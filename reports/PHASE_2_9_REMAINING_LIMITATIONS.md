# PHASE 2.9 — Remaining Limitations and Phase 3 Engineering Prerequisites

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_8_FINAL_INDEPENDENT_GATE_AUDIT.md`  

---

## 1. Overview & Purpose

Phase 2.9 has hardened the test harness, closed all circularity escapes, established strict fail-closed evidence governance, and verified 12 out of 12 actionable defect regression tests against plausible mutation candidates.

This document explicitly identifies the **remaining architectural, specification, and environment limitations** that must NOT be unilaterally decided during testing and require formal engineering ratification prior to Phase 3 application remediation.

---

## 2. Formally Blocked Specifications (Architectural Blockers)

Three regression tests remain **unconditionally BLOCKED** on the baseline and **BLOCKED / NOT DEMONSTRATED** in the sensitivity matrix. These tests reflect genuine gaps in project design specifications rather than test-harness deficiencies:

### 2.1 TC-REG-D02-TEMPERATURE-PROPAGATION (DEC-015 / DEF-06)
- **Current Baseline Behavior:** `add_temperature_load()` attempts to read `temperature_load_kN_m2` from `input_dict` (which is unpopulated by the UI), resulting in `temperature_load_case` remaining `None`.
- **Engineering Specification Deficit:** IRC 6:2017 Cl. 215 specifies two distinct temperature load components:
  1. **Overall Temperature Rise and Fall (Cl. 215.2):** Uniform temperature strain causing longitudinal expansion/contraction at expansion joints and bearing forces.
  2. **Temperature Differential / Gradient (Cl. 215.3, Table 10):** Non-linear vertical temperature gradient across the composite deck depth (positive gradient with top slab warmer than bottom flange, and reverse gradient).
- **Prerequisite for Phase 3 Remediation:**
  - The project team must ratify whether OsdagBridge models uniform thermal strain, vertical differential gradient, or both.
  - The grillage representation (equivalent thermal nodal loads vs OpenSees thermal beam-column elements) must be architecturally approved.

### 2.2 TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS (DEC-018 / DEF-17)
- **Current Baseline Behavior:** UI defaults include toggle `KEY_LL_IRC_CLASS_FATIGUE`, and vendored `ospgrillage` contains `create_fatigue_vehicle()`. However, `vehicle_lane_coordinates()` only routes standard `ClassA` and `Class70R` vehicles. The fatigue vehicle is never analyzed as a moving load, and `PlateGirderAnalysisResults` lacks fatigue load extraction.
- **Engineering Specification Deficit:** IRC 6:2017 Cl. 204.6 specifies a single 400 kN fatigue vehicle with fixed axle spacing (4 axles: 60 kN, 120 kN, 110 kN, 110 kN) centered in an effective lane without concurrent vehicles.
- **Prerequisite for Phase 3 Remediation:**
  - Specification of the fatigue moving-load analysis pass: how the moving load envelope is extracted and combined.
  - Mapping into `designer.py`'s fatigue demand structure (`stress_range_MPa`), replacing placeholder extraction.

### 2.3 TC-REG-GEO-SLAB-SECTION-PROPERTIES (DEC-013 / DEF-14)
- **Current Baseline Behavior:** `BridgeGrillageModel.create_grillage()` assigns steel girder section properties divided by 2 (`girder/2`, $I_z = 0.00367\text{ m}^4$) to transverse deck slab members.
- **Engineering Specification Deficit:** Transverse grillage members represent concrete slab strips of width equal to grillage longitudinal node spacing ($s \approx 1.5\text{ m}$). Assigning halved steel girder properties is mechanically unphysical.
- **Prerequisite for Phase 3 Remediation:**
  - Engineering decision on transverse member formulation:
    - Option A: Transformed uncracked concrete slab strip ($I_{\text{trans}} = b \cdot d_s^3 / (12 \cdot m)$).
    - Option B: Cracked concrete section with torsional reduction factor ($J \approx 0.1 \cdot J_{\text{uncracked}}$).
  - Material properties mapping: whether transverse members use concrete modulus $E_{cm}$ or modular-ratio transformed steel properties.

---

## 3. Platform & Environment Considerations

### 3.1 POSIX Root Execution Boundary (DEC-023)
- In containerized CI/CD environments running as `root` (`UID == 0`), OS-level read-only file permissions (e.g., `chmod 0555`) are bypassed by the kernel for write operations.
- The `TC-REG-FS-CLEAN-WORKING-TREE` harness explicitly checks `os.geteuid() == 0` on POSIX systems. If running as root, Check 4 and the overall test result report `BLOCKED` with code `DEC-023` to prevent false passing.
- **Phase 3 Recommendation:** CI/CD runners must execute test suites under a non-root standard user account (e.g., `runner` or `developer`).

### 3.2 Win32 Job Object vs POSIX Process Groups
- On Windows, `ProcessLifetimeJob` utilizes native Win32 Job Objects (`CreateJobObjectW`, `SetInformationJobObject`, `AssignProcessToJobObject`) with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`.
- On POSIX systems, `ProcessLifetimeJob` utilizes process groups (`os.setsid` and `os.killpg`).
- Both boundaries guarantee child process cleanup, but Windows Job Objects offer true kernel-level enforcement even across process detachment (`CREATE_NEW_PROCESS_GROUP`).

### 3.3 OCC 3D Offscreen Rendering Environment
- `TC-REG-CAD-EXPORT-VS-SCREENSHOT` relies on native `pythonocc-core` 7.8.1 `Viewer3d.ExportToImage` using the local OpenGL graphic driver.
- In headless CI/CD environments without physical display adapters, a software OpenGL rasterizer (such as Mesa `llvmpipe` or Xvfb) must be configured.

---

## 4. Phase 3 Remediation Recommendations

When authorized to transition to Phase 3 (Application Source Remediation):
1. **Upstream Fixes:** Address `DEF-01` (`LoadCase.add_load` factor scaling) and `DEF-18` (cell-intersection bilinear load distribution) cleanly within `ospgrillage` or wrapped bridge grillage routines.
2. **Path Anchoring:** Update `ui_fields_project_location.py` and `database.py` to use `platformdirs` / User AppData for `weather.sqlite`, resolving `DEF-10`.
3. **Girder Alignment:** Update `designer.py:401` to use `bridge._girder_count()` instead of `geom.n_l`, resolving `DEF-11`.
4. **Section Snapping:** Synchronize `_girder_section` with snapped plate dimensions and align `dw` in `input_dict`, resolving `DEF-03`.
5. **Report Executive Summary:** Dynamically iterate over `output_dict` component checks rather than writing hardcoded "Pass", resolving `DEF-08`.
6. **Bearing Stiffener Buckling:** Replace stiffener $I_{ys}$ with web strip $r_y = t_w / \sqrt{12}$ and column curve c, resolving `DEF-12`.
7. **Steel Density Propagation:** Pass `material.girder.density` to line load generation, resolving `DEF-13`.
