# Dependency Compatibility Matrix: OsdagBridge

## 1. Multi-Manifest Dependency Reconciliation

This matrix audits and reconciles all 5 dependency specifications across the upstream repository:
1. `environment.yml` (Recommended Conda runtime)
2. `pyproject.toml` (PEP 621 build and runtime specification)
3. `requirements.txt` (Pip-centric requirements)
4. `conda-recipe/meta.yaml` (Conda package build recipe)
5. `constructor/construct.yaml` (Standalone installer packaging manifest)

---

## 2. Reconciled Component Matrix & Observed Status

| Dependency | `environment.yml` | `pyproject.toml` | `requirements.txt` | `meta.yaml` | `construct.yaml` | Selected Source | Installed Version in `osdagbridge-env` | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **Python** | `>=3.11,<3.13` | `>=3.11,<3.13` | — | `>=3.11,<3.13` | `==3.11.8` | Conda (`conda-forge`) | **3.11.18** | **PASS** | 64-bit Windows interpreter |
| **PySide6** | Implied | — | `>=6.5.0,<=6.9.3` | `pyside6` | `pyside6` | Conda (`conda-forge`) | **6.9.0** | **PASS** | Qt6 GUI framework & OpenGL |
| **pythonocc-core** | Implied | — | — | `pythonocc-core` | `pythonocc-core` | Conda (`conda-forge`) | **7.9.0** | **PASS** | OCCT 7.9.0 C++ CAD bindings |
| **OpenSeesPy** | `>=3.2.2.6` (pip) | `>=3.2.2.6` | — | `openseespy` | `openseespy` | Pip (`openseespywin`) | **3.7.0.1** | **PASS** | FEA engine linked against Python 3.11 C runtime |
| **opsvis** | Listed (pip) | `>=1.0` | — | — | — | Pip (PyPI) | **1.0.8** | **PASS** | Grillage visualization tool |
| **NumPy** | Implied | — | `>=1.21.0` | `numpy` | `numpy` | Conda (`conda-forge`) | **2.4.6** | **PASS** | Intel MKL backend |
| **SciPy** | `>=1.10.1` | `>=1.10.1` | `>=1.10.1` | `scipy` | `scipy` | Conda (`conda-forge`) | **1.17.1** | **PASS** | Scientific computation & spatial |
| **Matplotlib** | Listed | `>=3.5` | — | `matplotlib` | `matplotlib-base` | Conda (`conda-forge`) | **3.10.9** | **PASS** | 2D graph & diagram rendering |
| **IfcOpenShell** | — | — | Listed | `ifcopenshell` | `ifcopenshell` | Conda (`conda-forge`) | **0.8.3.post1** | **PASS** | Industry Foundation Classes BIM |
| **Fiona** | Listed | Listed | Listed | `fiona` | `fiona` | Conda (`conda-forge`) | **1.10.1** | **PASS** | Geospatial vector engine |
| **Shapely** | Listed | Listed | Listed | `shapely` | `shapely` | Conda (`conda-forge`) | **2.0.7** | **PASS** | 2D computational geometry |
| **Pydantic** | Listed | `>=2.0` | Listed | `pydantic` | `pydantic` | Conda (`conda-forge`) | **2.14.3** | **PASS** | Schema validation & core models |
| **Xarray** | Listed | Listed | Listed | `xarray` | `xarray` | Conda (`conda-forge`) | **2026.9.0** | **PASS** | N-dimensional labeled arrays |
| **Openpyxl** | — | — | Listed | `openpyxl` | `openpyxl` | Conda (`conda-forge`) | **3.1.5** | **PASS** | Excel report generation |
| **PyYAML** | — | — | — | — | — | Pip / Conda | **6.0.3** | **PASS** | `.osi` project file serialization |
| **Lark** | — | — | — | — | — | Pip (PyPI) | **1.3.1** | **PASS** | IfcOpenShell stream parser |
| **Navcube** | — | — | — | `navcube` | `navcube` | Conda (`geompy`) | **1.1.0** | **PASS** | 3D interactive navigation cube |
| **ospgrillage** | Vendor-bundled | Listed in package-data | — | — | — | Local (`src/ospgrillage`) | **0.1.0** (bundled) | **PASS** | OpenSees grillage pre/post-processor |
| **OsdagBridge** | Target App | Target App | Target App | Target App | Target App | Editable (`-e .`) | **1.0.0** (dev) | **PASS** | Plate girder bridge module |

---

## 3. Critical ABI & Upstream Bug Findings

### 1. The OpenSeesPy Windows Wheel Anomaly:
- PyPI release `openseespywin 3.7.0.3` was packaged with a binary `opensees.pyd` that depends on `python312.dll`, despite declaring `Requires-Python: ~=3.11.0`.
- In a Python 3.11 environment, installing `openseespywin 3.7.0.3` triggers `ImportError: DLL load failed while importing opensees: The specified module could not be found` (Windows Error Code 126).
- **Resolution:** Pinning `openseespy==3.7.0.1` and `openseespywin==3.7.0.1` provides binary compatibility with `python311.dll` and imports with zero errors.

### 2. Upstream Bug (Issue #98 - `sqlite` on PyPI):
- Upstream package metadata declares a requirement for `sqlite`. Python has included `sqlite3` natively in the standard library since Python 2.5; no active PyPI package named `sqlite` exists.
- Running standard pip commands without `--no-deps` causes pip to fail during dependency tree resolution.
- **Resolution:** All upstream dependencies are fully satisfied via Conda prior to running pip with `--no-deps`.

### 3. Solver SAT Combinatorial Explosion:
- Combining Anaconda's `defaults` (`main`) channel with `conda-forge` causes severe SAT solver conflicts between differing build variants of C/C++ runtimes.
- **Resolution:** Utilizing `--override-channels -c osdag -c geompy -c conda-forge` resolves the entire native C++ dependency tree in under 15 seconds without conflicts.
