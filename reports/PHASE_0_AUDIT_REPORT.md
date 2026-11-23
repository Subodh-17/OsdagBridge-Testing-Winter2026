# PHASE 0 AUDIT REPORT: REPOSITORY FORENSICS & PRE-INSTALLATION READINESS

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Target Repository:** `https://github.com/Nidhikhare12/OsdagBridge.git`  
**Target Branch:** `dev`  
**HEAD Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Workspace Root:** `F:\FOSSEE internship`  
**Date of Audit:** 2026-11-15  
**Auditor / Candidate:** Subodh Bansode (`Subodh-17`)  
**Methodological Standard:** Strict empirical separation between **[EXECUTED]** runtime verification and **[STATIC]** code inspection.

---

## 1. Executive Summary

This Phase 0 Audit Report establishes the empirical and forensic baseline for testing the **OsdagBridge** short-span steel girder bridge module under the FOSSEE Winter Internship 2026. 

Our investigation confirms that the host machine possesses top-tier computational hardware (Intel Core i9-14900HX, 32 GB RAM, NVIDIA RTX 5070 Laptop GPU), making it an ideal testing ground for OpenCASCADE 3D CAD rendering, OpenSees FEM grillage analysis, and high-definition video demonstration capture. 

However, runtime verification confirms that **the desktop application cannot execute in the current host environment** due to missing dependencies (`PySide6`, `pythonocc-core`, `openseespy`). Furthermore, Conda is absent from the host system PATH. 

The repository's actual codebase exhibits notable divergences from its documented architecture: while advertised as a multi-interface (Desktop, CLI, Web), multi-bridge system (Plate Girder, Box Girder, Truss), the code on `dev` is exclusively a **Desktop PySide6 application for Plate Girder Bridges**, with CLI, Web, Box Girder, and Truss modules existing solely as 1-line stubs. The repository contains **0.00% real automated test coverage** (all 6 existing test files contain only `assert True`), and the GitHub Actions CI pipeline referenced in `README.md` (`.github/workflows/ci.yml`) does not exist.

A **CONDITIONAL GO** recommendation is issued: proceed to **Phase 1 (Environment Provisioning)** according to our proposed step-by-step installation plan, which mitigates known ecosystem blockers including the `osdag_core 0.0.0` bogus `sqlite` package declaration (Issue #98).

---

## 2. Environment Readiness Audit

### 2.1 Hardware Specifications [EXECUTED]
Verified via native Windows CIM (`Get-CimInstance`) queries:

| Metric | Measured Specification | Evaluation |
| :--- | :--- | :---: |
| **System Model** | HP OMEN Gaming Laptop 16-am0xxx | Production-Grade Workstation |
| **Operating System** | Microsoft Windows 11 Home Single Language (64-bit) | Fully Compatible |
| **OS Version / Build** | Version 10.0.26300, Build 26300 | Fully Compatible |
| **Processor (CPU)** | Intel(R) Core(TM) i9-14900HX (24 Cores / 32 Threads) | Optimal for Grillage Solvers |
| **System Memory (RAM)**| 33,970,475,008 bytes (~31.63 GB usable) | Abundant for FEM Analysis |
| **Discrete GPU** | NVIDIA GeForce RTX 5070 Laptop GPU (4 GB VRAM) | Optimal for 3D CAD (`pythonocc`) |
| **Integrated GPU** | Intel(R) UHD Graphics (Driver 32.0.101.7084) | Active Secondary Display |
| **Drive F: Free Space** | 135.38 GB free (Total 245.00 GB, NTFS) | Dedicated Project Workspace |
| **Drive C: Free Space** | 28.42 GB free (Total 190.14 GB, NTFS) | Sufficient for Conda Installation |

### 2.2 Host Toolchain Profile [EXECUTED]
- **Git:** `git version 2.55.0.windows.3` (Installed and active in system PATH).
- **GitHub CLI:** `gh version 2.102.0 (2026-09-30)` (Installed and active).
- **GitHub Authentication:** Authenticated as user `Subodh-17` with token scopes `gist`, `read:org`, `repo`, `workflow`.
- **System Python:** Python 3.11.0 located at `C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe`.
- **Windows Package Manager:** `winget v1.29.380` (Ready for automated package deployment).
- **Conda / Miniconda:** **NOT DETECTED** in system PATH or standard system directories.

### 2.3 Preserved Filesystem Integrity [EXECUTED]
A recursive search across all local drives (`C:`, `D:`, `E:`, `F:`) confirmed that no previous OsdagBridge installation existed. Existing user files were safely identified in `C:\Users\Subodh\Downloads`:
- `Testing of OsdagBridge - Non Civil.docx.pdf` (Official internship brief).
- `Subodh_Resume.pdf` and `Subodh_Resume.docx` (Candidate resume for final packaging).

---

## 3. Repository Status & Git Topology

### 3.1 Repository Identity & Commit Baseline [EXECUTED]
- **Upstream Git URL:** `https://github.com/Nidhikhare12/OsdagBridge.git`
- **Local Clone Location:** `F:\FOSSEE internship\source\OsdagBridge`
- **Checked-Out Branch:** `dev` (tracking `origin/dev`)
- **HEAD Commit Hash:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
- **Commit Date & Author:** Sun Jul 26 13:56:10 2026 +0530, `mhsuhail00 <mhsuhail00@gmail.com>`
- **Commit Summary:** `fix: Z,Sa/g,Ah,Av in Report`
- **Working Tree Cleanliness:** Clean (`nothing to commit, working tree clean`). Zero uncommitted changes.

### 3.2 Remote Branch Hierarchy [EXECUTED]
Querying `git ls-remote --heads` revealed 10 remote branches:
- `dev` (`d74f56d`): Official development and testing branch.
- `main` (`2cb7ddc`): Release trunk.
- Feature/Task branches: `deck_design`, `nidhi-temp`, `optimization`, `report`, `screening-task-plot`, `screening-task-ui`, `temp`, `test-pr342`.

---

## 4. Architecture Overview: Documented Claims vs. Actual Codebase

### 4.1 Structural Divergence [STATIC]
A rigorous structural audit reveals substantial discrepancies between `README.md` and the actual codebase layout:

```
Claimed in README.md                  Actual Implementation on dev
--------------------------------      -----------------------------------------
src/osdagbridge/bridge_types/    -->  src/osdagbridge/core/bridge_types/
src/osdagbridge/bridge_components/--> src/osdagbridge/core/bridge_components/
src/osdagbridge/web/             -->  web/ (at repo root, not inside src/)
(not mentioned)                  -->  src/ospgrillage/ (bundled grillage wrapper)
(not mentioned)                  -->  conda-recipe/ & constructor/ (packaging)
```

### 4.2 Module Implementation Analysis [STATIC]

| Subsystem | Source Location | Implementation Status | Technical Assessment |
| :--- | :--- | :---: | :--- |
| **Plate Girder Module** | `src/osdagbridge/core/bridge_types/plate_girder/` | **COMPLETE** | Mature implementation: `plategirderbridge.py` (223 KB), `designer.py` (185 KB), `analyser.py` (123 KB), `deckdesign.py` (60 KB), `cad_generator.py` (50 KB). |
| **Desktop GUI (PySide6)**| `src/osdagbridge/desktop/` | **COMPLETE** | Production GUI: `CustomWindow`, dual-view CAD docks, report option dialogs, input/output docks. |
| **Box Girder Module** | `src/osdagbridge/core/bridge_types/box_girder/` | **STUB** | 7 files containing only 1-line docstrings (e.g. `"""box_girder analyser (stub)."""`). |
| **Truss Bridge Module** | `src/osdagbridge/core/bridge_types/truss/` | **STUB** | 7 files containing only 1-line docstrings. |
| **CLI Interface** | `src/osdagbridge/cli/` | **STUB** | `commands.py` contains only dummy `print("analyze", path)`. README commands do not exist. |
| **Web Interface** | `web/backend/` & `web/frontend/` | **STUB** | `manage.py` prints `"Django manage stub"`; `package.json` has `"version": "0.0.0"`. |

**Forensic Finding:** OsdagBridge is effectively a **desktop-only Plate Girder Bridge application**. All screening task verification must focus entirely on this module.

### 4.3 Startup Pipeline & Database Architecture [STATIC]
Startup begins in `src/osdagbridge/desktop/__main__.py`:
1. `_register_conda_dll_directories()`: Dynamically adds conda prefix `Library/bin`, `DLLs`, and `Library/mingw-w64/bin` to the Windows DLL search path via `os.add_dll_directory` to prevent native C++ crashes during OpenBLAS/MKL and Qt delay-loading.
2. `_ensure_std_streams()`: Guards against Windows `pythonw.exe` GUI crashes where `stdout`/`stderr` are `None`.
3. `_set_windows_app_id()`: Registers Windows AppUserModelID (`Osdag.OsdagBridge.Desktop.1`) for taskbar icon binding.
4. `create_sqlite()`: Inspects `ResourceFiles/Intg_osdag.sql` and generates `Intg_osdag.sqlite` if missing or stale.
5. `ensure_osdag_core_db()`: Connects to `osdag_core.data.ResourceFiles.Database` and compiles SQLite tables (`Beams`, `Angles`, `Columns`). Requires the `osdag` base package.
6. Launches `CustomWindow("OsdagBridge", PlateGirderBridge)` inside `QApplication`.

---

## 5. Test Suite & Continuous Integration Assessment

### 5.1 Automated Test Suite Audit [STATIC]
Inspection of `tests/` revealed six test files across two subdirectories:
- `tests/integration/test_api_plate_girder.py` (46 bytes)
- `tests/integration/test_cli_plate_girder.py` (46 bytes)
- `tests/integration/verification_ddcl_cases.py` (47 bytes)
- `tests/unit/test_analyser.py` (51 bytes)
- `tests/unit/test_designer.py` (51 bytes)
- `tests/unit/test_io.py` (45 bytes)

**Code Inspection of All Test Files:**
```python
def test_placeholder():
    assert True
```
- **Real Automated Test Coverage:** **0.00%**.
- No functional test assertions, no regression tests, and no design code validation tests exist in the official repository.

### 5.2 CI Pipeline Audit [STATIC]
- `README.md` asserts: *"Continuous integration runs automatically through GitHub Actions (`.github/workflows/ci.yml`)."*
- **Reality:** `.github/workflows/ci.yml` **does not exist**.
- The sole workflow in `.github/workflows/` is `conda-publish.yml`, which triggers only on pushes to the `packaging` branch to upload conda binaries to Anaconda Cloud.
- **Risk:** No automated regression testing guards pull requests on `dev`.

---

## 6. Dependency Risks & Blocker Analysis

### 6.1 Dependency Triangulation [STATIC]

```
                   ┌───────────────────────────────────────┐
                   │           environment.yml             │
                   │ python>=3.11,<3.13, osdag::osdag      │
                   │ scipy, fiona, shapely, pydantic       │
                   │ pip: openseespy, opsvis, -e .         │
                   └──────────────────┬────────────────────┘
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│       requirements.txt        │               │     conda-recipe/meta.yaml    │
│ PySide6>=6.5.0,<=6.9.3        │               │ pyside6, pythonocc-core       │
│ numpy, scipy, fiona, shapely  │               │ navcube, ifcopenshell, fiona  │
│ pydantic, xarray, openpyxl    │               │ shapely, scipy, pydantic,     │
│ ifcopenshell                  │               │ xarray, numpy, matplotlib-base│
└───────────────────────────────┘               │ pyyaml, openpyxl, pandas,     │
                                                │ plotly, osdag                 │
                                                └───────────────────────────────┘
```

### 6.2 Key Dependency Risks
1. **The Native OpenCASCADE (`pythonocc-core`) Blocker:**
   `src/osdagbridge/desktop/ui/cad_3d.py` imports `from OCC.Core.Quantity import Quantity_Color`. PyPI does not distribute functional Windows wheels for OpenCASCADE. It **must** be installed via Conda (`conda-forge` or `osdag` channels).
2. **The `osdag_core 0.0.0` Bogus `sqlite` Package Blocker (Issue #98):**
   The upstream `osdag_core` package declares `sqlite` in its `Requires-Dist` metadata. Pip resolution fails when attempting to query PyPI for `sqlite` because Python uses built-in `sqlite3`. 
   *Mitigation:* Install conda dependencies first and install pip packages with `--no-deps`.
3. **Python 3.13 Binary Incompatibility:**
   Binary wheels for `pythonocc-core` and `osdag` are compiled strictly for Python 3.11 and 3.12 (`python>=3.11,<3.13`).
   *Mitigation:* Pin `python=3.11` during environment creation.

---

## 7. Executed Runtime Verification & Failure Analysis

### 7.1 Executed Desktop Launch Failure [EXECUTED]
- **Command:** `cd "F:\FOSSEE internship\source\OsdagBridge\src"; python -m osdagbridge.desktop`
- **Result:** Immediate Process Termination (Exit Code 1)
- **Traceback:**
  ```python
  Traceback (most recent call last):
    File "<frozen runpy>", line 198, in _run_module_as_main
    File "<frozen runpy>", line 88, in _run_code
    File "F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\desktop\__main__.py", line 75, in <module>
      from PySide6.QtWidgets import QApplication
  ModuleNotFoundError: No module named 'PySide6'
  ```
- **Finding:** The host environment lacks `PySide6`.

### 7.2 Executed Backend Import Failure [EXECUTED]
- **Command:** `python -c "from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge"`
- **Result:** Process Termination (Exit Code 1)
- **Traceback:**
  ```python
  Traceback (most recent call last):
    File "F:\FOSSEE internship\source\OsdagBridge\src\ospgrillage\__init__.py", line 47, in <module>
      import openseespy.opensees as ops
  ModuleNotFoundError: No module named 'openseespy'
  ```
- **Finding:** The grillage solver subsystem fails due to missing `openseespy`.

---

## 8. Existing Issue Coverage & De-Duplication Register

The upstream repository has 40+ tracked issues. The following table highlights the critical issues directly impacting our planned testing:

| Issue # | Title | Affected Component | Known Root Cause / Impact |
| :---: | :--- | :--- | :--- |
| **#19** | OSI load does not restore `_material_custom_fields` | `input_dock.py`, `template_page.py` | Custom material properties reload from defaults on re-design after loading `.osi`. |
| **#20** | Custom steel density ignored in `_build_material_props` | `plategirderbridge.py` | Code hardcodes $\rho = 78500\text{ N/m}^3$ and ignores `material.girder.density`. |
| **#41** | Custom deck density never reaches `create_deck_load` | `plategirderbridge.py`, `dto.py` | `ConcreteProperties` lacks density; dead-load analysis always uses $25\text{ kN/m}^3$. |
| **#43** | Cross-bracing/end-diaphragm custom grades unused | `plategirderbridge.py` | Transverse members reuse main girder steel properties. |
| **#72** | End Diaphragm tab displays cross-bracing results | `transverse_member_design.py` | GUI tab points to wrong dictionary key in output dock. |
| **#76** | Custom material dialog restricts to 1 decimal place | `material_properties.py` | DoubleSpinBox format `0.0` prevents entering Poisson's ratio `0.31`. |
| **#85** | 3D CAD model not displayed after unlock and redesign | `cad_3d.py`, `cad_safety.py` | Teardown during unlock leaves OCC context unable to redraw in run 2. |
| **#96** | Loading `.osi` skips custom-material validation | `osi_validator.py` | Out-of-range material values bypass load-time checks. |
| **#97** | Toggling lock crashes when Additional Inputs not opened | `input_dock.py` | Unconditional call to `_additional_inputs_dialog.lock()` raises `AttributeError` on `None`. |
| **#98** | `osdag_core` declares bogus `sqlite` package | Package Metadata | Breaks clean pip dependency resolution in fresh environments. |

---

## 9. Proposed Multi-Level Testing Strategy

To address the official task requirements comprehensively, we propose a 5-track testing strategy:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   OsdagBridge Verification Engine                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    ▼                               ▼                               ▼
┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
│ Track 1: Geometry &    │    │ Track 2: Custom        │    │ Track 3: Multi-Run &   │
│ Boundary Limits        │    │ Materials & Dictionaries│   │ State Persistence      │
│ - Spans: 20m, 30m, 45m │    │ - Custom steel & conc. │    │ - 3+ consecutive runs  │
│ - Boundary: 19.9m, 45.1m│   │ - Input/Output diffs   │    │ - CAD blanking audit   │
│ - Skew: 0°, 15°, 30°   │    │ - OSI Save/Load round  │    │ - Cache leakage checks │
│ - Lanes: 1, 2, 4 + med.│    │   trip validation      │    │ - Padlock unlock state │
└────────────────────────┘    └────────────────────────┘    └────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
        ┌────────────────────────┐      ┌────────────────────────┐
        │ Track 4: 3D CAD &      │      │ Track 5: Code-Level    │
        │ Graphics Integrity     │      │ Anomaly Investigation  │
        │ - Component toggles    │      │ - Exact file:line root │
        │ - Triad & navcube      │      │   cause identification │
        │ - BMD/SFD plot synch   │      │ - Unified diff patches │
        │ - Screen capture video │      │ - De-duplicated reports│
        └────────────────────────┘      └────────────────────────┘
```

### Planned Test Execution Matrices:
1. **Geometric Parameter Sweep:** Evaluate straight, skewed ($10^\circ, 30^\circ$), wide deck ($>12\text{ m}$), and edge-limit spans ($19.9\text{ m}, 45.1\text{ m}$).
2. **Material Customization Sweep:** Configure custom steel ($f_y = 350\text{ MPa}, \rho = 80.0\text{ kN/m}^3, \nu = 0.31$) and custom concrete ($f_{ck} = 45\text{ MPa}, \rho = 26.0\text{ kN/m}^3$). Compare UI values against captured `input_dict` and `output_dict`.
3. **Sequential Multi-Run Protocol:** Execute Run 1 (Span 25 m) $\rightarrow$ Unlock $\rightarrow$ Modify (Span 35 m, Skew 15°) $\rightarrow$ Run 2 $\rightarrow$ Unlock $\rightarrow$ Modify (Custom materials) $\rightarrow$ Run 3. Capture video and audit 3D viewport state.
4. **Automated Dictionary Comparison:** Execute automated scripts in `testing/scripts/` to assert exact matching between entered parameters, internal dictionaries, and output dock summaries.

---

## 10. Phased Installation Plan (Execution Scheduled for Phase 1)

### Phase 1 Execution Blueprint:

```powershell
# 1. Install Miniconda3 via winget
winget install --id Anaconda.Miniconda3 -e --silent --accept-package-agreements --accept-source-agreements

# 2. Inject Conda into active PowerShell environment
$env:Path = "C:\Users\Subodh\miniconda3;C:\Users\Subodh\miniconda3\Scripts;C:\Users\Subodh\miniconda3\Library\bin;" + $env:Path

# 3. Create dedicated isolated conda environment with Python 3.11
conda create -n osdagbridge-env python=3.11 -c osdag -c geompy -c conda-forge -y

# 4. Install native C++ CAD and calculation dependencies
conda install -n osdagbridge-env -c osdag -c geompy -c conda-forge osdag pythonocc-core navcube pyside6 fiona shapely scipy pydantic xarray matplotlib-base openpyxl ifcopenshell -y

# 5. Activate environment and install wheel dependencies with --no-deps (bypasses Issue #98)
conda activate osdagbridge-env
pip install --no-deps openseespy>=3.2.2.6 opsvis

# 6. Install OsdagBridge in editable mode
cd "F:\FOSSEE internship\source\OsdagBridge"
pip install --no-deps -e .

# 7. Execute baseline verification suite
python -c "import osdagbridge, PySide6, OCC.Core, ospgrillage; print('[OK] All core packages imported successfully!')"
python -m osdagbridge.desktop
```

---

## 11. GO / NO-GO Recommendation

| Gate / Audit Category | Assessment | Status |
| :--- | :--- | :---: |
| **Workspace & Directory Architecture** | Fully initialized at `F:\FOSSEE internship` without nested directories | **PASS** |
| **Hardware Capability** | Intel Core i9-14900HX, 32 GB RAM, NVIDIA RTX 5070 | **PASS** |
| **Repository Baseline** | Upstream `dev` branch cloned cleanly at commit `d74f56d` | **PASS** |
| **Toolchain & Remote Auth** | Git 2.55, GitHub CLI authenticated as `Subodh-17` | **PASS** |
| **Ecosystem & Blocker Analysis** | Known packaging issues (#98, #97, OpenCASCADE) fully mapped | **PASS** |
| **Current Host Python Readiness** | Missing PySide6, Conda, and OpenCASCADE | **BLOCKED (Expected)** |
| **Installation Plan Viability** | Fully specified with winget and `--no-deps` mitigation | **PASS** |

### FINAL VERDICT: **CONDITIONAL GO**
The repository forensics, hardware audits, and architecture inspections for Phase 0 are 100% complete. The environment is fully understood, and all blockers are documented with concrete mitigations. 

We are fully prepared to proceed to **Phase 1: Environment Provisioning & Application Verification** upon user confirmation.
