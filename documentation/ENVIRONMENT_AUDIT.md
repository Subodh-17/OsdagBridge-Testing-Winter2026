# Environment Audit & Pre-Installation Analysis

## 1. Host System & Hardware Profile

All hardware and operating system parameters were verified via native Windows CIM/WMI queries:

| Component | Specification | Forensic Status |
| :--- | :--- | :---: |
| **Operating System** | Microsoft Windows 11 Home Single Language (64-bit) | **[EXECUTED]** |
| **OS Version / Build** | Version 10.0.26300, Build 26300 | **[EXECUTED]** |
| **Hardware Platform** | HP OMEN Gaming Laptop 16-am0xxx | **[EXECUTED]** |
| **Processor (CPU)** | Intel(R) Core(TM) i9-14900HX (24 physical cores, 32 logical threads) | **[EXECUTED]** |
| **Physical Memory (RAM)** | 33,970,475,008 bytes (~31.63 GB usable) | **[EXECUTED]** |
| **Discrete GPU** | NVIDIA GeForce RTX 5070 Laptop GPU (4 GB VRAM, Driver 32.0.15.9227) | **[EXECUTED]** |
| **Integrated GPU** | Intel(R) UHD Graphics (Driver 32.0.101.7084) | **[EXECUTED]** |
| **Workspace Storage (F:)** | 135.38 GB Free of 245.00 GB (NTFS) | **[EXECUTED]** |
| **System Storage (C:)** | 28.42 GB Free of 190.14 GB (NTFS) | **[EXECUTED]** |

**Hardware Readiness Verdict:** Exceptional performance tier. High-core CPU and discrete RTX 5070 GPU ensure instant OpenCASCADE 3D CAD rendering, FEM grillage solving via OpenSees, and seamless high-frame-rate video screencast recording.

---

## 2. Host Development Toolchain Status

| Tool / CLI | Detected Version / Path | Readiness State |
| :--- | :--- | :---: |
| **Git** | `git version 2.55.0.windows.3` | **READY** |
| **GitHub CLI (`gh`)** | `gh version 2.102.0 (2026-09-30)` | **READY** |
| **GitHub Auth** | Authenticated as `Subodh-17` (`repo`, `workflow` scopes) | **READY** |
| **System Python** | Python 3.11.0 (`C:\Users\Subodh\AppData\Local\Programs\Python\Python311\`) | **INCOMPATIBLE ALONE** |
| **Windows Package Manager** | `winget v1.29.380` | **READY** |
| **Conda / Miniconda** | **NOT FOUND IN SYSTEM PATH** | **BLOCKER (Needs Install)** |

---

## 3. Dependency Specification Triangulation

An in-depth cross-comparison between the project's four dependency declarations reveals notable variations:

| Package | `environment.yml` | `requirements.txt` | `pyproject.toml` | `conda-recipe/meta.yaml` | Resolving Source |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Python** | `>=3.11,<3.13` | — | `>=3.11,<3.13` | `>=3.11,<3.13` | Conda (`python=3.11` or `3.12`) |
| **PySide6** | Implied via `osdag` | `>=6.5.0,<=6.9.3` | — | `pyside6` | Conda / Pip |
| **pythonocc-core** | Implied via `osdag` | — | — | `pythonocc-core` | `osdag` / `conda-forge` |
| **navcube** | Implied via `osdag` | — | — | `navcube` | `osdag` / `geompy` channel |
| **osdag / osdag_core**| `osdag::osdag` | — | — | `osdag` | `osdag` conda channel |
| **openseespy** | `>=3.2.2.6` (pip) | — | `>=3.2.2.6` | — | Pip wheel |
| **opsvis** | `opsvis` (pip) | — | `>=1.0` | — | Pip wheel |
| **scipy** | `>=1.10.1` | `>=1.10.1` | `>=1.10.1` | `>=1.10.1` | Conda / Pip |
| **shapely** | `shapely` | `shapely` | `shapely` | `shapely` | Conda / Pip |
| **fiona** | `fiona` | `fiona` | `fiona` | `fiona` | Conda / Pip |
| **xarray** | `xarray` | `xarray` | `xarray` | `xarray` | Conda / Pip |
| **pydantic** | `pydantic` | `pydantic` | `>=2.0` | `pydantic` | Conda / Pip |
| **ifcopenshell** | — | `ifcopenshell` | — | `ifcopenshell` | Conda / Pip |
| **openpyxl** | — | `openpyxl` | — | `openpyxl` | Conda / Pip |

### Critical Dependency Insights:
1. **The `pythonocc-core` Hard Requirement:** The 3D CAD viewer widget (`src/osdagbridge/desktop/ui/cad_3d.py`) directly imports `from OCC.Core.Quantity import Quantity_Color`. PyPI wheels for OpenCASCADE (`pythonocc-core`) on Windows are virtually non-existent or unreliable; it **must** be installed via Conda (`conda-forge` or `osdag` channel).
2. **The `osdag::osdag` Requirement:** The application references `osdag_core` database definitions and section tables. The channel `https://conda.anaconda.org/osdag` must be declared in Conda.

---

## 4. Empirical Execution Failures [EXECUTED]

To distinguish static assumptions from real behavior, the application launch was tested against the existing host environment:

### Test 1: Desktop Application Startup
- **Command:** `cd "F:\FOSSEE internship\source\OsdagBridge\src"; python -m osdagbridge.desktop`
- **Result:** FAILED (Exit Code 1)
- **Output:**
  ```python
  Traceback (most recent call last):
    File "<frozen runpy>", line 198, in _run_module_as_main
    File "<frozen runpy>", line 88, in _run_code
    File "F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\desktop\__main__.py", line 75, in <module>
      from PySide6.QtWidgets import QApplication
  ModuleNotFoundError: No module named 'PySide6'
  ```

### Test 2: Core Engineering Backend Import
- **Command:** `python -c "from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge"`
- **Result:** FAILED (Exit Code 1)
- **Output:**
  ```python
  Traceback (most recent call last):
    File "F:\FOSSEE internship\source\OsdagBridge\src\ospgrillage\__init__.py", line 47, in <module>
      import openseespy.opensees as ops
  ModuleNotFoundError: No module named 'openseespy'
  ```

**Conclusion:** The application cannot run in the unprovisioned host environment.

---

## 5. Identified Installation Blockers & Mitigation Strategy

### Blocker 1: Missing Conda Distribution
- **Impact:** Cannot create the prescribed `osdagbridge-env` or install native OpenCASCADE binaries.
- **Mitigation:** In Phase 1, install Miniconda3 silently via `winget install --id Anaconda.Miniconda3 -e --silent --accept-package-agreements --accept-source-agreements` or download the official installer to `C:\Users\Subodh\Miniconda3`.

### Blocker 2: Upstream `osdag_core` Bogus `sqlite` Metadata (Issue #98)
- **Impact:** The installed `osdag_core 0.0.0` conda package specifies `sqlite` in its PyPI distribution requirements (`Requires-Dist`). When pip attempts to resolve or rebuild dependencies, it crashes because `sqlite` does not exist on PyPI (Python uses the built-in `sqlite3` standard library module).
- **Mitigation:** Use conda for core package resolution, and install `openseespy`, `opsvis`, and the editable project `-e .` using `--no-deps` or explicit package lists during the pip stage.

### Blocker 3: Python 3.13 Incompatibility
- **Impact:** System default Python on some modern Windows setups is Python 3.13. OpenCASCADE and PySide6 bindings in the `osdag` channel have wheels pinned to Python 3.11 and 3.12 (`python>=3.11,<3.13`).
- **Mitigation:** Explicitly pin `python=3.11` or `python=3.12` during `conda create`.

---

## 6. Phased Installation Plan (Execution Scheduled for Phase 1)

1. **Step 1: Install Miniconda3**
   ```powershell
   winget install --id Anaconda.Miniconda3 -e --silent --accept-package-agreements --accept-source-agreements
   ```
2. **Step 2: Add Conda to PATH for the Session**
   ```powershell
   $env:Path = "C:\Users\Subodh\miniconda3;C:\Users\Subodh\miniconda3\Scripts;C:\Users\Subodh\miniconda3\Library\bin;" + $env:Path
   ```
3. **Step 3: Create `osdagbridge-env` with Prescribed Channels**
   ```powershell
   conda create -n osdagbridge-env python=3.11 -c osdag -c geompy -c conda-forge -y
   ```
4. **Step 4: Install Core Conda Packages**
   ```powershell
   conda activate osdagbridge-env
   conda install -n osdagbridge-env -c osdag -c geompy -c conda-forge osdag pythonocc-core navcube pyside6 fiona shapely scipy pydantic xarray matplotlib-base openpyxl ifcopenshell -y
   ```
5. **Step 5: Install Python Wheel Backends via Pip**
   ```powershell
   pip install --no-deps openseespy>=3.2.2.6 opsvis
   ```
6. **Step 6: Install OsdagBridge in Editable Mode**
   ```powershell
   cd "F:\FOSSEE internship\source\OsdagBridge"
   pip install --no-deps -e .
   ```
7. **Step 7: Verify Installation & Launch Application**
   ```powershell
   python -c "import osdagbridge, PySide6, OCC.Core, ospgrillage; print('All core modules verified successfully!')"
   python -m osdagbridge.desktop
   ```
