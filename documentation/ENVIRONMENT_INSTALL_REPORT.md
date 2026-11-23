# Environment Installation Report: OsdagBridge

## 1. Executive Summary
This report documents the provisioning and technical validation of an isolated execution environment (`osdagbridge-env`) for OsdagBridge on Windows 11 under the FOSSEE Winter Internship 2026. The installation strictly adheres to all safety invariants established in `ENVIRONMENT_INSTALL_PLAN.md`:
- Host system Python 3.11 (`C:\Users\Subodh\AppData\Local\Programs\Python\Python311\`) remains completely isolated, intact, and untouched.
- Miniconda3 (version 26.9.4) was provisioned at user-level (`C:\Users\Subodh\miniconda3\`).
- An isolated conda environment `osdagbridge-env` was created targeting Python 3.11.18.
- Channel resolution was configured to `--override-channels -c osdag -c geompy -c conda-forge` to eliminate SAT solver stalls.
- Native CAD (OpenCASCADE / `pythonocc-core 7.9.0`), Qt6 GUI (`PySide6 6.9.0`), and numerical packages (`numpy 2.4.6`, `scipy 1.17.1`) were resolved and installed via Conda.
- The finite element grillage analysis backend (`openseespy 3.7.0.1`, `opsvis 1.0.8`) and the local `OsdagBridge` repository were installed in development mode.
- All verification steps executed cleanly with zero warnings or errors.

---

## 2. Infrastructure & Toolchain Details

| Attribute | Observed Setting / Value | Status |
| :--- | :--- | :---: |
| **Miniconda Distribution** | Miniconda3 `py314_26.9.4-1` (Windows-x86_64) | INSTALLED |
| **Conda Version** | `conda 26.9.4` | VERIFIED |
| **Conda Solver** | `libmamba` (Accelerated dependency solver) | ACTIVE |
| **Miniconda Installation Root** | `C:\Users\Subodh\miniconda3` | ISOLATED USER-LEVEL |
| **Environment Name** | `osdagbridge-env` | CREATED |
| **Environment Location** | `C:\Users\Subodh\miniconda3\envs\osdagbridge-env` | ENCAPSULATED |
| **Target Python Version** | Python 3.11.18 (`win-64`) | COMPLIANT |
| **Configured Channels** | `osdag`, `geompy`, `conda-forge` | CONFIGURED |

---

## 3. Package Resolution & Installation Ledger

### 3.1 Native Binary & Core Conda Packages
The following packages were resolved through the Conda dependency solver:
- **`pythonocc-core` (7.9.0) & `occt` (7.9.0):** Native OpenCASCADE Technology (OCCT) 7.9.0 C++ kernel bindings and geometry libraries.
- **`pyside6` (6.9.0) & `qt6-main` (6.9.0):** Qt6 graphical user interface libraries.
- **`ifcopenshell` (0.8.3.post1):** Native Industry Foundation Classes (IFC) BIM model parser and generator.
- **`numpy` (2.4.6) & `scipy` (1.17.1):** Optimized scientific libraries linked against Intel MKL (`mkl-2025.3.1`).
- **`matplotlib-base` (3.10.9):** 2D graphics and structural diagram plotting engines.
- **`fiona` (1.10.1) & `shapely` (2.0.7):** Geospatial and computational 2D geometry engines wrapping native GDAL and GEOS.
- **`pydantic` (2.14.3) & `xarray` (2026.9.0):** Structural schema data validation and multidimensional results arrays.
- **`openpyxl` (3.1.5) & `pyyaml` (6.0.3):** Data exchange and `.osi` project file serialization.
- **`navcube` (1.1.0):** 3D interactive view navigation cube from `geompy`.

### 3.2 Pip Package Installation Ledger & Justification for `--no-deps`
`openseespy`, `opsvis`, and the local editable package `-e .` were installed via `pip`:
- **OpenSeesPy Stack:**
  - Installed `openseespy==3.7.0.1` and `openseespywin==3.7.0.1`.
  - Justification: `openseespywin 3.7.0.3` on PyPI was miscompiled against `python312.dll`. `openseespywin 3.7.0.1` correctly links to `python311.dll`, matching the active Python 3.11 runtime.
- **Support Parsers:**
  - Installed `lark==1.3.1` (eliminates IfcOpenShell stream parser fallback warning).
  - Installed `pyyaml==6.0.3` (required by `CustomWindow` and project serialization).
- **Justification for `--no-deps` (Issue #98):**
  The upstream package `osdag_core 0.0.0` declares an invalid PyPI dependency `sqlite` in its metadata (`Requires-Dist`). Python includes `sqlite3` in its standard library; no package named `sqlite` exists on PyPI. Running standard `pip install` without `--no-deps` causes pip to fail during dependency resolution. Because all dependencies (`numpy`, `scipy`, `matplotlib`, `fiona`, `shapely`, `pydantic`, `xarray`) are already provided and satisfied by the Conda environment, `--no-deps` safely circumvents this bug without causing dependency drift.
- **Local Repository Setup:**
  - `conda run -n osdagbridge-env pip install --no-deps -e "F:\FOSSEE internship\source\OsdagBridge"`
  - Successfully built and installed `osdagbridge-1.0.0-0.editable-py3-none-any.whl`.
  - Automatically provided bundled `ospgrillage` from `src/ospgrillage/`.

---

## 4. Disk Space Footprint
- **Miniconda Base:** ~450 MB on Drive `C:`
- **`osdagbridge-env` Environment:** ~2.8 GB on Drive `C:`
- **Remaining Free Space on Drive C:** ~24.9 GB free (Safe operating margin)
- **Workspace on Drive F:** 135.3 GB free (Completely unimpacted)

---

## 5. Verification Command & Reproducibility
The full environment can be re-validated at any time via:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-env\python.exe" "F:\FOSSEE internship\testing\scripts\verify_phase_1a.py"
```
Output log is archived at: `F:\FOSSEE internship\testing\test_logs\phase_1a_verification.log`.
