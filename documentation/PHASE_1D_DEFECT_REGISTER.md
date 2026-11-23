# PHASE 1D DEFECT REGISTER — OSDAGBRIDGE

**Workspace:** `F:\FOSSEE internship`  
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`  
**Baseline Git Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Branch:** `dev`  
**Date:** 2026-11-16 (Updated with Reconciled Evidence)  
**Status:** **FROZEN — BASELINE REGRESSION HARNESS ESTABLISHED**  

---

## Document Purpose

This document provides a comprehensive, verified register of all defects, calculation inaccuracies, and architectural anomalies identified during the Phase 1D computational readiness run, the independent technical audit (`PHASE_1D_INDEPENDENT_AUDIT.md`), and the subsequent conflict reconciliation (`PHASE_2_REVIEW_RECONCILIATION.md`).

Per project instructions:
- No source code has been patched.
- No inputs or tolerances have been altered to force a passing result.
- All previously cited fabricated numbers and phantom log lines have been expunged and replaced with authentic values from the raw output dictionary and physical source files.
- Seven additional defects (DEF-11 through DEF-17) identified during independent review have been formally added.
- Source-level mechanism evidence is strictly distinguished from observed behavioral evidence.

---

## Defect Inventory Overview

| ID | Title | Severity | Module / Location | Defect Category | Upstream Dependency? | Status |
| :--- | :--- | :---: | :--- | :--- | :---: | :---: |
| **DEF-01** | Load factors omitted in `ospgrillage` combination solve | **Critical** | `ospgrillage/osp_grillage.py:1934-2010` | FEA / Structural | **Yes** (Joint: `ospgrillage` & OsdagBridge) | **CONFIRMED** |
| **DEF-02** | Crash barrier SIDL omitted from combinations | **High** | `analyser.py:1516-1551`, `plategirderbridge.py:1331` | Load Formulation | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-03** | Grillage analysis section differs from designed section | **Critical** | `plategirderbridge.py:497-535`, `1107-1118` | Section Sizing | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-04** | Grillage mesh geometry & edge beam stiffness discrepancy | **High** | `plategirderbridge.py:1018-1024`, `1115` | Grillage Mesh | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-05** | Wind parameters ignored (hardcoded 33 m/s fallback + 4 keys) | **High** | `plategirderbridge.py:1381-1392` | Input Wiring | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-06** | Temperature load input key missing (silent combination skip) | **High** | `plategirderbridge.py:1858-1875` | Load Formulation | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-07** | Fatigue stress range doubled via member-end sign flip | **Critical** | `designer.py:2983-2985` | Code Compliance | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-08** | LaTeX / PDF report hardcoded outcomes & figure setup gap | **Medium** | `executive_summary.py:233-236`, `output_dock.py` | Reporting | **No** (OsdagBridge / Harness) | **CONFIRMED** |
| **DEF-09** | Blank CAD screenshot generated via Qt OpenGL buffer grab | **Medium** | GUI / `execute_phase_1d_e2e.py` | Test Harness / GUI | **No** (Test Harness Implementation) | **RECLASSIFIED** |
| **DEF-10** | Untracked `weather.sqlite` created in source tree | **Low** | `database.py:21-30`, `.gitignore:257` | Architecture | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-11** | Grillage edge lines included in girder design loop | **High** | `designer.py:401` | Sizing Pipeline | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-12** | Bearing stiffener web buckling capacity anomaly | **Medium** | `designer.py`, `output_dict` | Design Capacity | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-13** | Hardcoded material density and barrier load conflicts | **Medium** | `analyser.py:374, 681, 1866` | Physical Constants | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-14** | Deck slab transverse members take steel girder properties | **High** | `plategirderbridge.py:1279-1306` | Grillage Modeling | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-15** | Report Table 5.12 girder labels mapped to grillage lines | **Medium** | Report Table 5.12 | Reporting | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-16** | Live load combination term discrepancy | **Medium** | `analyser.py`, `output_dict` | Combination Math | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-17** | Fatigue vehicle defined but never analysed in grillage | **Critical** | `irc6_2017.py:371-413` | Code Compliance | **No** (OsdagBridge) | **CONFIRMED** |
| **DEF-18** | Non-conservation of static load equilibrium in FE load distribution | **Critical** | `ospgrillage/osp_grillage.py:910-1080` | FEA / Load Distribution | **Yes** (`ospgrillage`) | **CONFIRMED** |

---

## Detailed Defect Records

### DEF-01: Load factors omitted in `ospgrillage` combination solve
- **Severity:** **Critical**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `ospgrillage.osp_grillage.OspGrillage._distribute_load_types_to_model` and `analyser.py:_copy_loads`
- **Source Location:** `src/ospgrillage/load.py:1166–1168`, `src/ospgrillage/osp_grillage.py:1934–2010`, `analyser.py:2344–2349`
- **Source-Level Mechanism Evidence:**
  In `load.py:1167`, `load_dict.setdefault("factor", load_factor)` stores the factor in the dictionary. However, in `osp_grillage.py:1944–1948`:
  ```python
  mag = nested_list_of_load.load_point_1.p  # Never multiplied by load_dict["factor"]
  ```
  `_distribute_load_types_to_model` traverses `load_groups`, extracts `load_obj`, and passes raw unscaled magnitudes to OpenSees. Simultaneously, in `analyser.py:2344–2349`, OsdagBridge bypassed `ospgrillage`'s native `add_load_combination` API and relied on `_copy_loads` with `add_load(..., load_factor=factor)`, assuming that `add_load` mutates load magnitudes.
- **Behavioral Evidence:**
  Internal member force envelopes for combinations (e.g., `COMB_ULS_BASIC_1`) match the raw unfactored sum of cases. Dead load alone has moment $M_{dead}$, and factored combination $1.35 DL + 1.5 LL$ has moments that are identical to $1.0 DL + 1.0 LL$ (or DL alone when LL is missing).
- **Upstream vs. OsdagBridge Origin:** Joint architectural defect: upstream `ospgrillage` ignores `factor` in `add_load`, while OsdagBridge made an invalid assumption regarding `_copy_loads`.

---

### DEF-02: Crash-barrier SIDL omitted from combinations
- **Severity:** **High**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `BridgeGrillageModel.create_dead_load_combination` / `PlateGirderBridge.create_dead_load_combination`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/analyser.py:1516–1551`, `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1331–1339`
- **Source-Level Mechanism Evidence:**
  In `analyser.py:1536`, `_DL_ATTRS` lists `["self_weight", "wearing_course", "sidl_combination"]`. In `plategirderbridge.py:1331–1339`, `create_crash_barrier_load()` and `create_railing_load()` are called, but `create_sidl_combination()` is **never invoked**. Consequently, `self.sidl_combination` remains `None`. In `create_dead_load_combination()`, lines 1542–1548 skip `sidl_combination`.
- **Behavioral Evidence:**
  In `output_dictionary_snapshot.json`, crash barrier, railing, and median line loads are completely absent from all dead load and ULS combination matrices.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-03: Analysis section differs from designed section
- **Severity:** **Critical**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderBridge._resolve_optimized_bounds_to_mm` and `PlateGirderBridge.create_sections`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:497–535, 1107–1118`
- **Source-Level Mechanism Evidence:**
  In `plategirderbridge.py:523–535`, `_resolve_optimized_bounds_to_mm()` snaps plate thicknesses up to standard SAIL commercial increments ($t_f: 17.08 \to 18\text{ mm}$, $t_w: 6.53 \to 8\text{ mm}$). However, it never updates `KEY_MP_GIRDER_SECTIONAL_AREA`, `KEY_MP_GIRDER_SECTIONAL_IZ`, `KEY_MP_GIRDER_SECTIONAL_IY`, or `KEY_MP_GIRDER_TORSION_CONSTANT_IT`. OpenSees executes grillage analysis using the preliminary un-snapped properties, while `designer.py` checks capacities using snapped plate geometry.
- **Behavioral Evidence:**
  In `output_dictionary_snapshot.json`:
  - Preliminary FE model section: $A = 0.022534\text{ m}^2$, $I_z = 0.0073409\text{ m}^4$.
  - Designed snapped section: $A = 0.025192\text{ m}^2$, $I_z = 0.0079276\text{ m}^4$ ($1340 \times 410 \times 18\text{ mm}$, $d_w = 1304\text{ mm}, t_w = 8\text{ mm}$).
  - Grillage analysis was conducted on a section that was 7.4% more flexible in $I_z$ and 10.6% smaller in area than the fabricated section.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-04: Grillage mesh geometry & edge beam stiffness discrepancy
- **Severity:** **High**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderBridge.deck_layout` and `PlateGirderBridge.create_sections`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1018–1024, 1115`, `core/utils/common.py:1474`
- **Source-Level Mechanism Evidence:**
  1. `common.py:1474` defines `DEFAULT_CRASH_BARRIER_WIDTH = 0.5`. In `plategirderbridge.py:1019`, this constant overrides the user-input barrier width ($0.45\text{ m}$), yielding a grillage width of $7.5 + 2 \times 0.5 = 8.5\text{ m}$ and girder spacing of $2.133\text{ m}$ instead of the design layout of $8.4\text{ m}$ and $2.10\text{ m}$.
  2. In `plategirderbridge.py:1115`, `edge_longitudinal=self._girder_section()` assigns the full steel plate girder stiffness ($I_z \approx 0.00734\text{ m}^4$) to the exterior slab overhang edge lines.
- **Behavioral Evidence:**
  Exterior slab overhangs draw approximately one-third of the total gravity bending moment, distorting girder distribution factors.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-05: Wind parameters ignored (hardcoded 33 m/s fallback + 4 keys)
- **Severity:** **High**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderBridge.add_wind_load`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1381–1392`
- **Source-Level Mechanism Evidence:**
  Lines 1381–1392 read bare un-prefixed keys from `ai`:
  - `ai.get("basic_wind_speed") or 33.0`
  - `ai.get("avg_exposed_height") or 10.0`
  - `ai.get("terrain_type") or "Plain Terrain"`
  - `ai.get("railing_height") or 0.0`
  - `ai.get("crash_barrier_height") or 0.0`
  In `input_configuration.json`, these keys are stored under prefixes (`loading.wind_load.*`, `typical_section.*`, `project.location.weather_data.wind_speed`).
- **Behavioral Evidence:**
  All five lookups evaluate to `None`. Wind speed silently falls back to 33.0 m/s for all sites; railing and barrier exposed heights fall back to 0.0 m, completely omitting barriers from exposed wind drag calculations.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-06: Temperature load input key missing (silent combination skip)
- **Severity:** **High**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderBridge.add_temperature_load`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1858–1875`
- **Source-Level Mechanism Evidence:**
  Line 1869 reads `tl_raw = self.input_dict.get("temperature_load_kN_m2")`. This key is never populated by any dialog, solver, or database routine. The function docstring notes "silently skipped" if absent.
- **Behavioral Evidence:**
  `tl_raw` evaluates to `0.0`, and temperature load cases are silently skipped. All 27 temperature-inclusive ULS/SLS combinations execute with zero thermal stress.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-07: Fatigue stress range doubled via member-end sign flip
- **Severity:** **Critical**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderDesigner.check_fatigue`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/designer.py:2983–2985`
- **Source-Level Mechanism Evidence:**
  Lines 2976–2985 flatten bending moments across all elements, member ends (`Mz_i`, `Mz_j`), and SLS Frequent combinations into a single array `mz_all`. In OpenSees, member ends $i$ and $j$ have opposite local sign conventions ($+M$ at $i$ and $-M$ at $j$ under sagging). Computing `max(mz_all.max(), 0.0) - min(mz_all.min(), 0.0)` doubles the moment to $2 \times M_{sls}$.
- **Behavioral Evidence:**
  In `output_dictionary_snapshot.json`, $M_{sls} = 1,455.73\text{ kNm}$. The stress range evaluates to $\Delta \sigma = 2 \times 1,455.73 \times 10^6 / 15.94 \times 10^6 = 182.633\text{ MPa}$, and shear range evaluates to $2 \times 215.25\text{ kN} / (1304 \times 8) = 41.268\text{ MPa}$. Against $f_{fd} = 92.491\text{ MPa}$, this yields a governing DCR of **1.9746 (FAIL)**.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-08: LaTeX / PDF report hardcoded outcomes & figure setup gap
- **Severity:** **Medium**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `executive_summary.py:233-236`, `output_dock.py:763`, `plategirderbridge.py:989`
- **Source-Level Mechanism Evidence:**
  1. `executive_summary.py:233–236` hardcodes literal text: `\noindent Girder design pass \\ Cross bracing design pass \\ End Diaphragm design pass \\ Deck design pass`, unconditionally printing "pass".
  2. `plategirderbridge.py:989` checks `if isinstance(cad_generator, dict): figure_data.update(...)`. In `execute_phase_1d_e2e.py:278`, the test script passed a raw `PlateGirderCADGenerator` object instead of the dict `{'generator': ..., 'figure_data': ...}` that `output_dock.py:763` passes, leaving `figure_data` empty.
- **Behavioral Evidence:**
  The PDF executive summary displays hardcoded "pass" text for failed checks, and all 13 report figures fell back to placeholders due to test script invocation mismatch.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect (hardcoded outcomes) + Test Harness defect (figure dict packaging).

---

### DEF-09: Blank CAD screenshot generated via Qt OpenGL buffer grab
- **Severity:** **Medium**
- **Classification:** **RECLASSIFIED AS TEST HARNESS IMPLEMENTATION DEFECT**
- **Relevant Module / Function:** `execute_phase_1d_e2e.py:220–226`
- **Source-Level Mechanism Evidence:**
  `execute_phase_1d_e2e.py` called Qt's `widget.grab()` on `cad_w`. On Windows, OpenCASCADE (`pythonocc-core` / OCCT 8.0.1) renders directly to hardware OpenGL swap chains. `widget.grab()` reads Qt's software `QPaintDevice` backing store, which remains transparent.
- **Behavioral Evidence:**
  `02_3d_cad_bridge_model.png` is an RGBA PNG with 92.95% transparent pixels ($\alpha = 0$). In-memory inspection confirmed all 83 3D solid shapes were successfully generated; calling OpenCASCADE native `View.Dump()` or `ExportToImage()` produces a fully rendered 3D image.
- **Upstream vs. OsdagBridge Origin:** Test Harness defect.

---

### DEF-10: Untracked `weather.sqlite` created in source tree
- **Severity:** **Low**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `Database.connect`
- **Source Location:** `src/osdagbridge/core/data/project_location/database.py:21–30`, `.gitignore:257`
- **Source-Level Mechanism Evidence:**
  Callers in `zone_lookup.py:183`, `ui_fields_project_location.py:16`, and `report_generator.py:666` pass absolute paths anchored on `__file__`. When absent, `Database.connect()` creates `weather.sqlite` inside `core/data/project_location/` and runs `schema.sql`. Line 257 of `.gitignore` masks `*.sqlite`.
- **Behavioral Evidence:**
  A 180,224-byte uncommitted binary file exists inside the tracked source tree.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-11: Grillage edge lines included in girder design loop
- **Severity:** **High**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderDesigner.from_plate_girder_bridge`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/designer.py:401`
- **Source-Level Mechanism Evidence:**
  `designer.py:401` sets `n_girders = geom.n_l`. `geom.n_l` counts all longitudinal grid lines in OpenSees, which includes the 2 slab cantilever edge lines ($4\text{ girders} + 2\text{ edge lines} = 6$).
- **Behavioral Evidence:**
  In `output_dictionary_snapshot.json`, `design_results.n_girders` is 6 for a 4-girder bridge, and girder capacity loops evaluate the exterior slab edge overhang lines as structural steel girders.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-12: Bearing stiffener web buckling capacity anomaly
- **Severity:** **Medium**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderDesigner._design_bearing_stiffeners`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/designer.py`, `output_dict`
- **Source-Level Mechanism Evidence:**
  Bearing stiffener web buckling capacity `bs_Fcdw_wb_kN` is evaluated without effective web strip limits, resulting in a raw value of $134,083.2\text{ kN}$.
- **Behavioral Evidence:**
  In `output_dictionary_snapshot.json`, `bs_Fcdw_wb_kN: 134083.225` wildly exceeds the stiffener's column squash capacity `bs_Fcd_kN: 2087.273`.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-13: Hardcoded material density and barrier load conflicts
- **Severity:** **Medium**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `BridgeGrillageModel.create_model`, `create_dead_load_cases`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/analyser.py:374, 681, 1866`
- **Source-Level Mechanism Evidence:**
  In `analyser.py:374`, steel density is hardcoded as $78.5\text{ kN/m}^3$ (database specifies $76.4\text{ kN/m}^3$). In line 1866, concrete density is hardcoded as $25.0\text{ kN/m}^3$ (database specifies $24.5\text{ kN/m}^3$). In line 681, crash barrier load is hardcoded as $6.54\text{ kN/m}$ (geometry specifies $0.30228\text{ m}^2 \times 25.0 = 7.56\text{ kN/m}$).
- **Behavioral Evidence:**
  Discrepancy between input database properties and applied OpenSees line loads.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-14: Deck slab transverse members take steel girder properties
- **Severity:** **High**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderBridge._transverse_section`, `_end_transverse_section`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py:1279–1306`
- **Source-Level Mechanism Evidence:**
  ```python
  # Transverse section
  A = g(KEY_MP_GIRDER_SECTIONAL_AREA) / 2
  Iz = g(KEY_MP_GIRDER_SECTIONAL_IZ) / 2
  # End transverse section
  A = g(KEY_MP_GIRDER_SECTIONAL_AREA) / 4
  Iz = g(KEY_MP_GIRDER_SECTIONAL_IZ) / 4
  ```
  Transverse grillage members represent concrete deck slab strips, but are assigned half and one-quarter of the fabricated steel girder's cross-sectional area and moment of inertia.
- **Behavioral Evidence:**
  Grillage transverse stiffness reflects steel plate girder proportions rather than concrete slab flexural rigidity ($E_c I_{slab}$).
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-15: Report Table 5.12 girder labels mapped to grillage lines
- **Severity:** **Medium**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** Report Generator Table 5.12 Compiler
- **Source Location:** `src/osdagbridge/core/reports/`, Table 5.12
- **Source-Level Mechanism Evidence:**
  Table 5.12 queries results across longitudinal grillage indices 1–4 and labels them "G1–G4".
- **Behavioral Evidence:**
  Line 1 is the exterior slab edge overhang line. Consequently, "G1" reports edge line forces, G2 represents main Girder 1, G3 represents main Girder 2, G4 represents main Girder 3, and main Girder 4 (line 5) is omitted from the report table.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-16: Live load combination term discrepancy
- **Severity:** **Medium**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `BridgeGrillageModel.create_uls_combinations`
- **Source Location:** `src/osdagbridge/core/bridge_types/plate_girder/analyser.py`
- **Source-Level Mechanism Evidence:**
  The unfactored live load term extracted inside combinations ($675.7\text{ kNm}$ on G3) matches neither 1.0 LL ($683.5\text{ kNm}$) nor governing 70R ($751.9\text{ kNm}$).
- **Behavioral Evidence:**
  Inconsistency in live load envelope component extraction during combination assembly.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-17: Fatigue vehicle defined but never analysed in grillage
- **Severity:** **Critical**
- **Classification:** **CONFIRMED**
- **Relevant Module / Function:** `PlateGirderBridge.run_moving_load_analysis`
- **Source Location:** `src/osdagbridge/core/utils/codes/irc6_2017.py:371–413`, `plategirderbridge.py:2020–2045`
- **Source-Level Mechanism Evidence:**
  `irc6_2017.py:371` defines `cl_204_6_fatigue_load()` (40-tonne 3-axle vehicle). However, `PlateGirderBridge` moving load analysis only iterates over standard Class A and Class 70R vehicles. The fatigue vehicle is never analyzed as a moving load case.
- **Behavioral Evidence:**
  In `output_dictionary_snapshot.json`, fatigue checks are evaluated on SLS Frequent combinations rather than the discrete transit of the IRC 6 fatigue vehicle.
- **Upstream vs. OsdagBridge Origin:** OsdagBridge application defect.

---

### DEF-18: Non-Conservation of Static Load Equilibrium in FE Grillage Load Distribution
- **Severity:** **Critical**
- **Classification:** **CONFIRMED** (Discovered in independent audit `PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md` §1 & §2, verified empirically via OpenSees reaction extraction)
- **Relevant Module / Function:** `ospgrillage.osp_grillage.OspGrillage._assign_line_to_four_node` and `_assign_patch_load`
- **Source Location:** `src/ospgrillage/osp_grillage.py:910–1080`
- **Source-Level Mechanism Evidence:**
  1. In `_assign_line_to_four_node`: For line loads not colinear with longitudinal grid elements (such as crash barrier line loads at $z = 0.25\text{ m}$ and $z = 8.25\text{ m}$), line segments crossing grid cells assign `mag = W` (force per unit length in N/m) instead of multiplying by segment length $L$ ($W \times L$). Furthermore, end points are assigned with an offset calculation placing coordinates outside the mesh grid ($x = -0.75\text{ m}$), dropping end segments. For two crash barriers of $6.54\text{ kN/m}$ across $24\text{ m}$ ($313.92\text{ kN}$ applied), only $196.20\text{ kN}$ is assigned to OpenSees nodes (support reaction shortfall of $-117.72\text{ kN}$ or $-37.5\%$).
  2. In `_assign_patch_load`: Bounded and intersecting polygon area integration computes an effective deck area of $210.3\text{ m}^2$ instead of the true geometric area $204.0\text{ m}^2$ ($24.0 \times 8.5\text{ m}$), scaling deck slab ($1275.0\text{ kN}$ applied) and wearing course ($244.80\text{ kN}$ applied) reactions upwards by exactly $+3.088\%$ ($1314.38\text{ kN}$ and $252.36\text{ kN}$).
- **Behavioral Evidence:**
  Total dead load applied across SW, DD, DW, and Crash Barrier is $2003.54\text{ kN}$. The total support reaction in the finite element grillage is $1932.76\text{ kN}$. Static equilibrium is violated ($\sum R_y \ne \sum P_{applied}$, net shortfall of $70.78\text{ kN}$).
- **Upstream vs. OsdagBridge Origin:** Upstream `ospgrillage` core library defect (present in vendored fork).

---

## Historical Notes & Defect Register Errata

Earlier versions of this register contained several incorrect claims that have been formally corrected:
1. **DEF-03 Dimensions:** Expunged fabricated numbers ($B_f=500, t_f=40, d_w=1800, t_w=16, I_z=0.0278\text{ m}^4$). Replaced with verified dimensions ($1340 \times 410 \times 18\text{ mm}$, $d_w=1304\text{ mm}, t_w=8\text{ mm}, I_z=0.0073409\text{ m}^4$ preliminary vs $0.0079276\text{ m}^4$ snapped).
2. **DEF-04 Constant:** Corrected barrier width constant from 0.45 m to **0.5 m** (defined in `common.py:1474`).
3. **DEF-06 Warnings:** Removed claim of 27 log warnings. The temperature skip was completely silent.
4. **DEF-07 Stress Numbers:** Expunged fabricated figures ($\Delta M = 1,489,692\text{ N}\cdot\text{m}$, $\Delta \sigma = 163.7\text{ MPa}$, $\sigma_c = 82.9\text{ MPa}$). Replaced with verified output dictionary values ($M_{sls} = 1455.73\text{ kNm}$, $\Delta \sigma = 182.633\text{ MPa}$, $f_{fd} = 92.491\text{ MPa}$, $\text{DCR} = 1.9746$).
5. **DEF-08 Status:** Corrected claim of a green PASS banner. The LaTeX report explicitly outputs `Overall Design Status & Fail`.
6. **DEF-09 Reclassification:** Reclassified from an upstream OpenCASCADE/Qt defect to a **test harness implementation error**.
7. **DEF-10 Path & Ignore Rule:** Corrected from relative path to absolute path anchored on `__file__`, and `.gitignore` line from 17 to **257**.
