# PHASE 2.5 — Defect Register Update

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`)  
**Controlling Document:** `reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`  

---

## 1. Executive Summary

This document updates the OsdagBridge Defect Register based on the findings, empirical measurements, and mathematical validations established during Phase 2.5. Three major defects received critical mechanical refinements during this phase:
1. **DEF-18 (Grillage Load Distribution, Force Imbalance, and Centroid Displacement):** Detailed accounting of cell-intersection bilinear distribution, crash barrier load shortfall ($-37.5\%$), and longitudinal centroid displacement ($+0.750\text{ m}$).
2. **DEF-17 (IRC 6 Cl. 204.6 Fatigue Vehicle Analysis & Utilization Pipeline):** Separated from DEF-08; classified as an Architectural Gap / Feature Omission, and preserved as formally BLOCKED under DEC-018 pending Phase 3 specification sign-off.
3. **DEF-10 (Filesystem / Packaging / Working Tree Pollution):** Comprehensive definition of user-data path anchoring, default constructor behavior, package directory immutability, and resilience to read-only environments.

---

## 2. Updated Defect Summaries

### DEF-18: Grillage Load Allocation Inconsistency, Force Shortfall, and Centroid Displacement
- **Component:** `PlateGirderBridge.create_grillage()` / `plategirderbridge.py`
- **Severity:** High / Safety-Critical
- **Classification:** Computational Defect (Finite Element Grillage Mechanics)
- **Detailed Mechanics:**
  - When distributing static loads across the grillage mesh:
    1. **Deck Slab (DD):** Assigned $1314.375\text{ kN}$ instead of genuine input resultant $1275.000\text{ kN}$ ($+3.09\%$ surplus).
    2. **Wearing Course (DW):** Assigned $252.360\text{ kN}$ instead of genuine input resultant $244.800\text{ kN}$ ($+3.09\%$ surplus).
    3. **Crash Barrier:** Assigned $196.200\text{ kN}$ instead of genuine declared resultant $313.920\text{ kN}$ ($-37.50\%$ shortfall, deficit of $-117.720\text{ kN}$).
    4. **Centroid Displacement:** The crash barrier load distribution in OpenSees grillage places line load centroids at $x = 12.750\text{ m}$ instead of the bridge span midpoint $x = 12.000\text{ m}$, introducing a $+0.750\text{ m}$ longitudinal centroid shift.
- **Verification Criterion:** Bilinear cell-intersection distribution conserving 100% force (within 0.05%) and centroid coordinates (within 0.05 m).
- **Associated Test:** `TC-REG-EQ-LOAD-CONSERVATION` (Verified in Phase 2.5).

### DEF-17: Omission of IRC 6 Cl. 204.6 Fatigue Vehicle Moving Load Analysis
- **Component:** `designer.py` / `analyser.py` / `plategirderbridge.py`
- **Severity:** High / Compliance-Critical
- **Classification:** Architectural Gap / Feature Omission
- **Status:** **BLOCKED under DEC-018**
- **Detailed Mechanics:**
  - IRC 6:2017 Cl. 204.6 mandates evaluation of fatigue damage using a dedicated 40-tonne 4-axle Fatigue Vehicle with specified wheel spacing, axle loads, and dynamic amplification factors.
  - OsdagBridge currently lacks any code linking the moving fatigue vehicle to grillage moving load analysis, envelope generation, and cyclic stress range extraction in `designer.py`.
  - While static envelope stress ranges were erroneously computed (DEF-07), genuine fatigue verification cannot be completed without implementing the moving vehicle analysis pipeline.
- **Associated Test:** `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS`.

### DEF-10: Filesystem Pollution, Packaging Tree Mutation, and Read-Only Failure
- **Component:** `ui_fields_project_location.py` / `database.py`
- **Severity:** Medium / Usability & Packaging
- **Classification:** Packaging Architecture Defect
- **Detailed Mechanics:**
  - `ui_loc.DB_PATH` is hardcoded as `os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "project_location", "weather.sqlite"))`, resolving directly inside the installed package tree.
  - In a clean checkout or standard wheel installation where `weather.sqlite` is not bundled, calling `@_with_db` creates `weather.sqlite` inside the package directory.
  - The default constructor `Database()` defaults to `weather.sqlite` without directory anchoring, creating database files in `os.getcwd()`.
  - In a system-wide or read-only package installation, write operations trigger fatal `sqlite3.OperationalError` exceptions.
- **Remediation Specification:** Anchor `ui_loc.DB_PATH` and `Database.__init__` default to user app data (`%LOCALAPPDATA%\OsdagBridge` on Windows, `~/.local/share/osdagbridge` or `~/.osdagbridge` on Linux/macOS).
- **Associated Test:** `TC-REG-FS-CLEAN-WORKING-TREE` (Verified in Phase 2.5).

---

## 3. Master Defect Register Summary Table

| Defect ID | Title | Module / Source Location | Severity | Category | Phase 2.5 Status |
|:---|:---|:---|:---:|:---:|:---:|
| **DEF-01** | Upstream `ospgrillage` Load Factor Scaling Ignored | `ospgrillage` wrapper / `analyser.py` | Critical | Computational | Confirmed (TC-REG-A01) |
| **DEF-02** | ULS Load Combinations Unfactored & Missing Crash Barrier | `analyser.py:create_uls_combinations` | Critical | Engineering Logic | Confirmed (TC-REG-A02) |
| **DEF-03** | Section Property Desynchronization & Deflection Discrepancy | `plategirderbridge.py` / `designer.py` | High | Structural Sizing | Confirmed (TC-REG-B01) |
| **DEF-05** | Wind Load Parameter Propagation Loss | `analyser.py:add_wind_load` | High | Parameter Binding | Confirmed (TC-REG-D01) |
| **DEF-06** | Thermal Load Modeling Omission (IRC 6 Cl. 215) | `analyser.py:add_temperature_load` | High | Feature Omission | Blocked (DEC-015) |
| **DEF-07** | False Static Cyclic Stress Ranges from Opposing End Signs | `designer.py:465-485` | High | Engineering Logic | Confirmed (TC-REG-C01) |
| **DEF-08** | Executive Summary Emits Unconditional Pass Narrative | `executive_summary.py:220` | Medium | Reporting Logic | Confirmed (TC-REG-RPT) |
| **DEF-09** | Offscreen OCC CAD Rendering Pipeline Verification | Test Environment Harness | Low | Verification | PASS (TC-REG-CAD) |
| **DEF-10** | Filesystem Tree Pollution & Read-Only Packaging Failure | `ui_fields_project_location.py` / `database.py` | Medium | Packaging | Confirmed (TC-REG-FS) |
| **DEF-11** | Girder Count Geometry Misalignment (Overhang Lines Counted) | `designer.py:401` | High | Geometry | Confirmed (TC-REG-GEO-COUNT) |
| **DEF-12** | Bearing Stiffener Buckling Capacity Evaluation Discrepancy | `designer.py:compute_bearing_stiffener` | Critical | Capacity Formula | Confirmed (TC-REG-CAP) |
| **DEF-13** | Hardcoded Structural Steel Density Overriding User Input | `plategirderbridge.py:add_dead_loads` | Medium | Material Property | Confirmed (TC-REG-MAT) |
| **DEF-14** | Transverse Concrete Deck Slab Representation Model | `plategirderbridge.py` | High | Structural Modeling | Blocked (DEC-013) |
| **DEF-17** | IRC 6 Cl. 204.6 Fatigue Vehicle Analysis Pipeline Omission | `designer.py` / `analyser.py` | High | Feature Omission | Blocked (DEC-018) |
| **DEF-18** | Grillage Load Inconsistency, Barrier Shortfall & Centroid Shift | `plategirderbridge.py:create_grillage` | High | FE Modeling | Confirmed (TC-REG-EQ) |
