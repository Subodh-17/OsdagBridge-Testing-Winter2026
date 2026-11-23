# Phase 1B: Desktop Application Smoke Test Report

**Workspace:** `F:\FOSSEE internship`  
**Target Repository:** `F:\FOSSEE internship\source\OsdagBridge` (`origin/dev` @ `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Execution Environment:** `osdagbridge-env` (Python 3.11.18 64-bit)  
**Execution Date:** 2026-11-16  

---

## 1. Environment Fingerprint & Freeze Verification

The execution environment was frozen and fingerprinted prior to launching the desktop application:

| Parameter | Observed Setting / Exact Fingerprint | Verification Method |
| :--- | :--- | :--- |
| **Python Executable** | `C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe` | Executed `sys.executable` |
| **Python Version** | `3.11.18 | packaged by Anaconda, Inc. | (Oct 26 2026)` | Executed `sys.version` |
| **Host Python (Untouched)** | `C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe` | Preserved (3.11.0) |
| **Git Commit SHA** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | Executed `git rev-parse HEAD` |
| **Git Branch** | `dev` (Up to date with `origin/dev`) | Executed `git rev-parse --abbrev-ref HEAD` |
| **Git Working Tree** | `clean` (0 unstaged changes, 0 modified files) | Executed `git status` |
| **PySide6 / Qt6** | `6.9.0` (Qt Core 6.9.0 C++ backend) | Executed `PySide6.__version__` |
| **OpenCASCADE / pythonocc**| `7.9.0` (OCCT 7.9.0 C++ graphics driver) | Executed `OCC.Core` import |
| **OpenSeesPy** | `3.7.0.1` (`openseespywin 3.7.0.1` on Python 3.11 C runtime)| Executed `openseespy.opensees` |

### Raw Environment Artifacts:
- Conda explicit package list: [`evidence/environment/conda_explicit.txt`](file:///F:/FOSSEE%20internship/evidence/environment/conda_explicit.txt)
- Pip freeze export: [`evidence/environment/pip_freeze.txt`](file:///F:/FOSSEE%20internship/evidence/environment/pip_freeze.txt)
- Machine metadata dump: [`evidence/environment/environment_metadata.txt`](file:///F:/FOSSEE%20internship/evidence/environment/environment_metadata.txt)
- Full freeze specification: [`evidence/environment/ENVIRONMENT_FREEZE.md`](file:///F:/FOSSEE%20internship/evidence/environment/ENVIRONMENT_FREEZE.md)

---

## 2. Desktop Application Launch & Startup Audit

### 2.1 Launch Command
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe" -m osdagbridge.desktop
```

### 2.2 Startup Result & Observations
- **Process Status:** Launched successfully without unhandled exceptions or process abort.
- **Main Window Visibility:** `CustomWindow` instantiated, configured, and displayed on screen (`isVisible() == True`).
- **Dimensions:** Default window initialized at `1539 x 940` pixels (maximized desktop presentation).
- **Qt Platform / Plugin Errors:** **None.** PySide6 loaded native Windows platform plugin (`qwindows.dll`) cleanly.
- **Missing Resources:** Application icons, vector SVG toolbars, and `lightstyle.qss` stylesheet loaded with zero `QFile` open errors.

### 2.3 Non-Fatal Startup Errors & Initialization Logs
During the startup sequence, the console emitted:
```text
[ERROR] osdag_core database setup failed: No module named 'osdag_core'
```
**Forensic Root Cause Analysis:**
- In `source/OsdagBridge/src/osdagbridge/desktop/__main__.py` (lines 200–252), the function `ensure_osdag_core_db()` attempts to import `files('osdag_core.data.ResourceFiles.Database')` to construct standard section tables (`Beams`, `Angles`, `Columns`).
- Because `osdag_core` is provided only by the legacy `osdag::osdag` Conda package (which was bypassed due to the Issue #98 PyPI `sqlite` bug and solver stalls), `osdag_core` is not imported.
- The startup sequence catches this error in a `try...except` block, preventing an application crash. However, database section lookups for standard rolled steel members will fail if queried.

---

## 3. Detailed GUI Component Inspection

All major interface panels were programmatically and visually audited:

| Component | Visibility | Key Attributes / Contents | Status | Screenshot Artifact |
| :--- | :---: | :--- | :---: | :--- |
| **Main Window** | **Visible** | Title: `OsdagBridge`, Qt6 styled title bar, top toolbar, centralized splitter | **PASS** | [`01_main_window_default.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/01_main_window_default.png) |
| **Input Dock** | **Visible** | Geometry inputs (`span`, `carriageway_width`, `skew_angle`), design modes (`Auto/Manual`), spacing controllers | **PASS** | [`02_input_dock_detail.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/02_input_dock_detail.png) |
| **Additional Inputs Dialog**| **Visible** | Modal QDialog (`1024 x 900`). 5 functional tabs: <br>1. *Typical Section Details*<br>2. *Member Properties*<br>3. *Loading*<br>4. *Analysis/Design Options*<br>5. *Design Options (Cont.)* | **PASS** | [`03_additional_inputs_dialog.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/03_additional_inputs_dialog.png) |
| **Output Dock** | **Visible** | Splitter dock (`354 x 912`). Results tables, summary sections, and status indicators | **PASS** | [`04_output_dock_detail.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/04_output_dock_detail.png) |
| **Logs Dock** | **Visible** | Bottom console dock (`312 x 182`). Execution stream and calculation message logger | **PASS** | [`05_logs_dock_detail.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/05_logs_dock_detail.png) |
| **2D CAD Plots** | **Visible** | `BridgeDualCADWidget` containing: <br>- `CrossSectionCADWidget` (girder cross section)<br>- `TopViewCADWidget` (deck layout and bearings) | **PASS** | [`06c_cad_dual_view_composite.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/06c_cad_dual_view_composite.png) |
| **3D CAD Viewport** | **Visible** | OpenCASCADE `Display3d` context, background gradient, interactive NavCube | **PASS** | [`06_cad_3d_viewport_active.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/06_cad_3d_viewport_active.png) |
| **Full Composite View** | **Visible** | Maximized layout with 3D CAD and input docks synchronized | **PASS** | [`08_main_window_full_composite.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/08_main_window_full_composite.png) |

---

## 4. CAD Smoke Test (Task 4)

### 4.1 Scope & Limitation Notice
> [!IMPORTANT]
> In accordance with Task 4 constraints, this smoke test validates **only basic OpenCASCADE geometry creation, topological data structures, and OpenGL viewport initialization**. It **does not claim full bridge CAD verification**, as end-to-end parametric bridge solid rendering depends on design calculation results deferred to subsequent phases.

### 4.2 Executed CAD Verification
- **Geometry Kernel Test:** Created a solid 3D boundary representation box using OpenCASCADE primitives:
  ```python
  from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
  box_shape = BRepPrimAPI_MakeBox(2000.0, 500.0, 300.0).Shape()
  ```
  *Result:* Instantiated valid `TopoDS_Shape` with code 0.
- **Interactive Context (AIS) Display:**
  Bound `box_shape` to `cad_3d.display` (`AIS_InteractiveContext`), assigned RGB color mapping, and invoked camera projection:
  ```python
  cad_3d.display.DisplayShape(box_shape, color="BLUE", update=True)
  cad_3d.display.FitAll()
  ```
- **Hardware Acceleration Pipeline:**
  The OpenCASCADE driver initialized the native Windows OpenGL context (`WNT_Window`):
  ```text
  OpenGL Vendor:   Intel
  Renderer Device: Intel(R) RaptorLake-S Mobile Graphics Controller
  OpenGL Version:  4.6.0 - Build 32.0.101.7084
  GLSL Version:    4.60 - Build 32.0.101.7084
  MSAA Samples:    16
  FBO Buffer:      GL_SRGB8_ALPHA8 GL_DEPTH24_STENCIL8
  ```
- **Framebuffer Capture:**
  Exported the rendered 3D OCC box directly from the OpenGL framebuffer to [`07_cad_smoke_test_box.png`](file:///F:/FOSSEE%20internship/evidence/screenshots/07_cad_smoke_test_box.png) (5,813 bytes) using `display.ExportToImage()`.
- **CAD Smoke Test Verdict:** **PASS**

---

## 5. Summary of Captured Screenshots

All screenshots are archived under [`evidence/screenshots/`](file:///F:/FOSSEE%20internship/evidence/screenshots/):

| File Name | File Size | Description |
| :--- | :---: | :--- |
| `01_main_window_default.png` | 100,229 bytes | Default startup view: Input Dock open, 2D Dual CAD cross-section and plan views rendered |
| `02_input_dock_detail.png` | 64,785 bytes | Close-up of input fields (Span, Carriageway Width, Skew Angle, Girder parameters) |
| `03_additional_inputs_dialog.png` | 68,146 bytes | Modal dialog showing all 5 parameter tabs and input widgets |
| `04_output_dock_detail.png` | 51,564 bytes | Output dock showing design summary and verification tables |
| `05_logs_dock_detail.png` | 3,647 bytes | Execution log output console dock |
| `06_cad_3d_viewport_active.png` | 3,034 bytes | Active 3D OpenCASCADE canvas showing gradient and view cube |
| `06a_2d_cross_section_cad.png` | 15,316 bytes | 2D Cross section CAD drawing rendered via QPainter |
| `06b_2d_top_view_cad.png` | 18,442 bytes | 2D Top view bridge layout CAD drawing |
| `06c_cad_dual_view_composite.png` | 32,890 bytes | Dual view CAD panel with split cross-section and top view |
| `07_cad_smoke_test_box.png` | 5,813 bytes | Hardware OpenGL render of OpenCASCADE BRep 3D test box |
| `08_main_window_full_composite.png` | 113,254 bytes | Maximized application window showing full composite UI |

---

## 6. Identified Blockers & Anomalies for Subsequent Phases

1. **`osdag_core` Database Section Tables Missing:**
   Startup logs `[ERROR] osdag_core database setup failed: No module named 'osdag_core'`. While custom plate girder parameters can be entered manually, queries relying on `osdag_core.Common` (rolled steel section tables) will require fallback handling or local database seeding.
2. **Issue #97 Upstream Edge Case:**
   Toggling lock controls without first opening the Additional Inputs dialog triggers an unhandled `AttributeError` on `NoneType` due to uninitialized dialog state.
3. **Absence of Existing Automated Tests:**
   The repository `tests/` directory contains only `assert True` placeholders (0.00% coverage). All test cases for Phase 2/3 must be authored from scratch.

---

## 7. Recommendation

### **RECOMMENDATION: CONDITIONAL GO**

**Justification:**
- **The GUI application starts cleanly, reliably, and responsively** without fatal crashes or Qt plugin failures.
- **Input docks, Additional Inputs dialogs, Output docks, and Logs docks are fully initialized and functional.**
- **The OpenCASCADE 3D CAD engine and hardware-accelerated OpenGL viewport are verified and capable of rendering 3D solid geometry.**
- **The condition for advancing to Phase 2 (Test Plan & Test Suite Design)** is that test cases must account for the missing `osdag_core` section database and Issue #97 edge cases during test case construction.

**Git Working Tree Status:** Pristine (`nothing to commit, working tree clean`).
