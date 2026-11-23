# Existing Issues Register: Nidhikhare12/OsdagBridge

This register catalogs all 40+ existing issues on the upstream repository `https://github.com/Nidhikhare12/OsdagBridge.git`. It serves as our mandatory **de-duplication database** to ensure that any bugs reported during the internship represent genuinely novel findings or provide valuable new evidence on existing issues without duplicating them.

---

## 1. Deep-Dive Analysis on Critical Focus Issues

### Issue #19: OSI load does not restore `_material_custom_fields`
- **Issue ID:** #19
- **State:** OPEN | **Author:** Harshdeep-creator
- **Summary:** Custom material property maps are kept only in the in-memory dict `InputDock._material_custom_fields`. Saving an `.osi` file persists the grade name (e.g., `custom_steel_350_490`), but loading via `loadOSI_inputs()` does not rebuild `_material_custom_fields`. Clicking Design invokes `_prime_material_inputs()`, which overwrites the loaded values with default/parsed values.
- **Affected Files:**
  - `src/osdagbridge/desktop/ui/docks/input_dock.py` (`_material_custom_fields`, `_prime_material_inputs`)
  - `src/osdagbridge/desktop/ui/template_page.py` (`loadOSI_inputs`)
- **Trigger Condition:** Save `.osi` with custom materials $\rightarrow$ Restart/Reload $\rightarrow$ Run Design without reopening dialog.
- **Test Matrix Mapping:** Covered in Test Suite 2 (Custom Materials & Persistence).

---

### Issue #20: Custom steel density from UI/input_dict is ignored in `_build_material_props`
- **Issue ID:** #20
- **State:** OPEN | **Author:** Harshdeep-creator
- **Summary:** In `PlateGirderBridge._build_material_props()`, when a custom steel grade is selected, the code extracts $f_y, f_u, E, \nu$ from `input_dict`, but hardcodes density to `_DEFAULT_DENSITY = 78500.0` $\text{N/m}^3$ and completely ignores `KEY_MATERIAL_GIRDER_DENSITY` (`material.girder.density`).
- **Affected Files:**
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` (`_build_material_props`)
- **Code Trace:**
  ```python
  rho = self._lookup_material(steel_grade, "Density")
  if rho is None:
      rho = _DEFAULT_DENSITY  # Ignores input_dict[KEY_MATERIAL_GIRDER_DENSITY]
  ```
- **Trigger Condition:** Enter custom steel density (e.g. $80.0\text{ kN/m}^3$); dead load still uses $78.5\text{ kN/m}^3$.

---

### Issue #41: Custom deck density never reaches `create_deck_load` (always $25\text{ kN/m}^3$)
- **Issue ID:** #41
- **State:** OPEN | **Author:** Harshdeep-creator
- **Summary:** Custom deck concrete density is entered in UI and saved in `input_dict` as `material.deck.density`, but `ConcreteProperties` DTO lacks a density attribute, and `add_dead_loads()` invokes `create_deck_load()` without passing density, defaulting to $25.0\text{ kN/m}^3$.
- **Affected Files:**
  - `src/osdagbridge/core/bridge_types/plate_girder/dto.py` (`ConcreteProperties`)
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` (`_build_material_props`, `add_dead_loads`)
  - `src/osdagbridge/core/bridge_types/plate_girder/analyser.py` (`create_deck_load`)
- **Trigger Condition:** Enter custom concrete density (e.g. $26.0\text{ kN/m}^3$); self-weight calculation continues using $25.0\text{ kN/m}^3$.

---

### Issue #43: Cross-bracing and end-diaphragm custom grades are stored but unused in design
- **Issue ID:** #43
- **State:** OPEN | **Author:** Harshdeep-creator
- **Summary:** The UI allows selecting distinct custom steel grades for the Girder, Cross Bracing, and End Diaphragm. All three are stored in dictionaries. However, `_build_material_props` only creates a single `SteelProperties` object from the girder grade, so cross-bracing and diaphragm designs reuse the main girder material properties.
- **Affected Files:**
  - `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` (`_build_material_props`, `_design_cross_bracing_members`, `_design_end_diaphragm_members`)
- **Trigger Condition:** Assign different steel grades to Girders, Cross Bracing, and End Diaphragms; analysis executes with identical steel properties for all.

---

### Issue #72: End Diaphragm tab displays cross-bracing results instead of its own output dictionary
- **Issue ID:** #72
- **State:** OPEN | **Author:** HR5206 (Harish Raghav)
- **Summary:** In the Output Dock under the Transverse Member tabs, selecting the End Diaphragm tab with G1–G2 / Envelope selected displays the Cross-bracing utilization results instead of reading from the end-diaphragm output dictionary.
- **Affected Files:**
  - `src/osdagbridge/desktop/ui/dialogs/transverse_member_design.py`
  - `src/osdagbridge/desktop/ui/docks/output_dock.py`
- **Trigger Condition:** Complete a design run and inspect the End Diaphragm tab in the Transverse Member design dock.

---

### Issue #76: Custom material dialog restricts inputs to 1 decimal place
- **Issue ID:** #76
- **State:** OPEN | **Author:** Hardik200424
- **Summary:** In the Material Properties dialog (`material_properties.py`), numeric spinboxes/line-edits are configured with a single decimal place format (`0.0`), preventing engineers from entering standard engineering constants such as steel Poisson's ratio ($\nu = 0.31$ or $0.28$) or precise modulus values.
- **Affected Files:**
  - `src/osdagbridge/desktop/ui/dialogs/material_properties.py`
- **Trigger Condition:** Open Material Properties $\rightarrow$ Attempt to type `0.31` for Poisson's ratio; UI truncates or rounds to `0.3`.

---

### Issue #85: 3D CAD model not displayed after unlock and redesign (second run in the same session)
- **Issue ID:** #85
- **State:** OPEN | **Author:** Subodh-17 / Community Report
- **Summary:** In a single GUI session, the first Design run renders the 3D OpenCASCADE model correctly. Clicking the Padlock (Unlock) and running Design a second time results in an empty 3D CAD viewport, even though the info box updates and calculations succeed.
- **Affected Files:**
  - `src/osdagbridge/desktop/ui/docks/input_dock.py` (`toggle_lock`)
  - `src/osdagbridge/desktop/ui/cad_3d.py` (`clear_3d_cad`, `render_3d_cad`)
  - `src/osdagbridge/desktop/ui/utils/cad_safety.py` (`safety.clear`)
- **Trigger Condition:** Complete Run 1 (CAD renders) $\rightarrow$ Unlock $\rightarrow$ Modify any parameter $\rightarrow$ Complete Run 2 (Viewport blank).
- **Test Matrix Mapping:** Primary target for Requirement 2 (Multi-Run Testing) and Requirement 3 (CAD Verification).

---

### Issue #96: Loading a `.osi` file skips all custom-material validation
- **Issue ID:** #96
- **State:** OPEN | **Author:** amit-sarkar-svg
- **Summary:** `osi_validator.py` loops over `_BASIC_KEYS` and `_ADDITIONAL_KEYS`, but lacks all `material.*` keys. Consequently, invalid, negative, or physically impossible custom material values (e.g., $f_y = 99999\text{ MPa}$, $\rho = -5\text{ kN/m}^3$) loaded from a hand-edited `.osi` file pass validation unchallenged and trigger calculation blowups.
- **Affected Files:**
  - `src/osdagbridge/core/utils/osi_validator.py` (`_ADDITIONAL_KEYS`, `validate`)
  - `src/osdagbridge/desktop/ui/template_page.py` (`loadOSI_inputs`)
- **Trigger Condition:** Load an `.osi` file containing out-of-range material parameters.

---

### Issue #97: Toggling input lock can crash when Additional Inputs dialog was never opened
- **Issue ID:** #97
- **State:** OPEN | **Author:** amit-sarkar-svg
- **Summary:** `InputDock.toggle_lock()` calls `self.parent._additional_inputs_dialog.lock(lock=self.is_locked)` unconditionally. Because `_additional_inputs_dialog` is initialized lazily as `None`, clicking the padlock before ever opening Additional Inputs can raise `AttributeError: 'NoneType' object has no attribute 'lock'`.
- **Affected Files:**
  - `src/osdagbridge/desktop/ui/docks/input_dock.py` (lines 856–859)
- **Code Trace:**
  ```python
  self.is_locked = not self.is_locked
  # Raises AttributeError if dialog has not been opened yet:
  self.parent._additional_inputs_dialog.lock(lock=self.is_locked)
  ```
- **Trigger Condition:** Launch app $\rightarrow$ Do not open Additional Inputs dialog $\rightarrow$ Toggle padlock.

---

### Issue #98: `osdag_core` dependency metadata declares bogus `sqlite` package
- **Issue ID:** #98
- **State:** OPEN | **Author:** amit-sarkar-svg
- **Summary:** The installed `osdag_core 0.0.0` distribution metadata lists `sqlite` in `Requires-Dist`. Since Python incorporates `sqlite3` in its standard library and no package named `sqlite` exists on PyPI, package managers (like pip) can fail during clean dependency resolution.
- **Affected Area:** Ecosystem / Package Metadata (`osdag_core`).
- **Trigger Condition:** Clean environment pip dependency resolution.

---

## 2. Complete Upstream Issues Inventory (Issues #18 through #95)

| Issue # | State | Title | Category / Affected Subsystem |
| :---: | :---: | :--- | :--- |
| **#18** | CLOSED | permission check ignore | CI / Permissions |
| **#25** | OPEN | Declared font "Ubuntu Sans" is neither bundled nor given a fallback | GUI Typography |
| **#42** | OPEN | Default steel grade E 350A cannot complete design — Gs not set | Material Database |
| **#44** | OPEN | `design()` completes and builds CAD when util.fatigue exceeds 100% | Design Checks / IRC Code |
| **#45** | OPEN | Missing DCR categories are written as 0.0 on the output dock | Output Dock Display |
| **#48** | OPEN | Generated report contains placeholder sections and missing visualizations | Report Generation |
| **#53** | OPEN | Graphics, Database, and Help menu dropdowns open but options are unresponsive | Menu Actions |
| **#56** | OPEN | Location Bug | Project Location Dialog |
| **#61** | OPEN | Fx plot titled "Shear Force Diagram" and Tx plot titled "Bending Moment Diagram" | Graph Engine |
| **#64** | OPEN | Default RCC railing load is 1.4715 kN/m in input dict but 6.806 kN/m in design | Dead Load Calculations |
| **#65** | OPEN | Executive Summary says "design pass" for every component even when Overall Status is Fail | Summary Dock / Report |
| **#66** | OPEN | Report "Girder Section Dimensions" table prints metres labelled as mm | Report Formatting |
| **#67** | OPEN | An .osi file with an empty Span passes validation, then raises ValueError | OSI Validation |
| **#68** | OPEN | Report shows blank or N/A for No. of Traffic Lanes, Braking Load, wind/seismic | Report Formatting |
| **#69** | OPEN | `design()` accepts out-of-range Span (19.9 m, 45.1 m) and completes without error | Input Validation Bounds |
| **#70** | OPEN | Executive Summary: Girder Spacing and Deck Thickness have no units | Output Dock Display |
| **#71** | OPEN | Save Input overwrites committed deck and wearing-course thicknesses with defaults | Project Save (.osi) |
| **#73** | OPEN | Girder support-reaction fields disagree with reaction labels in the same plot | Output Dock Plots |
| **#74** | OPEN | Runtime deck layout uses fixed 0.5 m crash-barrier width instead of input's 0.45 m | Deck Design / CAD |
| **#81** | OPEN | PDF includes Material Take-off and References even when unchecked | Report Options Dialog |
| **#82** | OPEN | Incorrect MPa unit labels for steel elastic and shear modulus in exported Excel | Excel Export |
| **#84** | OPEN | Crash barrier area is mm² in defaults but m² in dialog, causing 0.00 MT in BOQ | BOQ Take-Off Engine |
| **#86** | OPEN | Selected wind speed, exposed height and terrain are replaced by defaults | Wind Load Analysis |
| **#87** | OPEN | Seismic load generation runs before governing vehicle selection and uses zero LL mass | Seismic Analysis |
| **#88** | OPEN | OSI validation accepts NaN physical inputs before layout and model construction | OSI Validation |
| **#89** | OPEN | Skewed four-girder bridges retain only one per-girder design result | Skew Bridge Analysis |
| **#90** | OPEN | Optimized custom section choices are ignored and continuous bounds fail | Section Optimizer |
| **#91** | OPEN | Zero-overhang models omit the two outer physical girders from self-weight loading | Dead Load Geometry |
| **#92** | OPEN | Canonical temperature inputs do not create thermal load cases in design pipeline | Thermal Load Analysis |
| **#93** | OPEN | CAD uses fixed 3 m cross-bracing spacing despite 13 m in design output | CAD Generator |
| **#94** | OPEN | Girder Design Check summary reports 8 checks but displays only 6 check cards | Check Cards UI |
| **#95** | OPEN | Clarification: Stress Limitation displays 0.9 × Fy instead of stated Fy / γM0 | Design Code Equations |

---

## 3. De-Duplication Protocol for Phase 2–4 Testing

To prevent filing duplicate issues:
1. **Pre-Check:** Before logging any anomaly, search this register using keywords from the traceback, affected variable names, or UI labels.
2. **Classification:**
   - If identical to an open issue: Log finding in `evidence/` as an **Independent Verification of Issue #X**, detailing additional trigger conditions or system nuances.
   - If a distinct root cause in a different file/method: Formulate a new code-level bug report with clear distinction.
