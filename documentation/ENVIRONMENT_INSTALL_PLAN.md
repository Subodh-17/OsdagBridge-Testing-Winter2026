# Environment Installation Plan: OsdagBridge (`osdagbridge-env`)

## 1. Objectives & Safety Invariants
This installation plan defines the deterministic provisioning of an isolated Python runtime environment for verifying and testing the **OsdagBridge** short-span steel girder bridge engineering module under the FOSSEE Winter Internship 2026.

### Strict Safety Invariants:
1. **Host Isolation:** Do not replace, overwrite, or mutate the existing host Python installation (`C:\Users\Subodh\AppData\Local\Programs\Python\Python311\`).
2. **Environment Encapsulation:** All packages, binaries, and compilers must reside strictly inside an isolated conda environment named `osdagbridge-env` located at `C:\Users\Subodh\miniconda3\envs\osdagbridge-env\`.
3. **No Blind Installations:** Resolve dependencies deliberately; verify channels, package availability, and version bounds before triggering native binary installation.
4. **Resolution Issue Documentation:** Do not employ `--no-deps` indiscriminately. Where `--no-deps` is required (specifically during pip wheel installation of `openseespy` and local editable install `-e .`), it must be formally justified by the documented ecosystem bug where `osdag_core 0.0.0` declares a non-existent PyPI package `sqlite` (Issue #98).
5. **Clean Rollback Guarantee:** In the event of resolution failure, the environment can be cleanly destroyed via `conda env remove -n osdagbridge-env -y` without leaving orphaned files or system registry pollution.

---

## 2. Channel Hierarchy & Resolution Strategy

The upstream project specifies four distinct conda channels across `environment.yml` and `constructor/construct.yaml`:
1. `https://conda.anaconda.org/osdag` (Provides `osdag` core database and section packages)
2. `https://conda.anaconda.org/geompy` (Provides `navcube` 3D navigation cube)
3. `https://conda.anaconda.org/conda-forge` (Provides `pythonocc-core`, `pyside6`, `fiona`, `shapely`, `ifcopenshell`, `scipy`)
4. `https://conda.anaconda.org/gsrathore` (Packaged standalone releases)

### Channel Solver Resolution Finding:
Combining the default Anaconda channels (`defaults`, `pkgs/main`) with `conda-forge` results in severe combinatorial SAT graph explosion and solver timeouts due to conflicting C-runtime and ABI versions. 

**Prescribed Channel Configuration:**
To guarantee clean, deterministic resolution, the native package stack must be resolved using:
```bash
conda install -n osdagbridge-env --override-channels -c osdag -c geompy -c conda-forge <packages>
```
`conda-forge` acts as the foundational channel for standard open-source C++ science stacks, while `geompy` provides the CAD navigation cube (`navcube 1.1.0`).

---

## 3. Phased Step-by-Step Installation Procedure

### Phase B: Miniconda User-Level Provisioning
1. Install Miniconda3 via `winget` in user scope (`--scope user`) to `%USERPROFILE%\miniconda3`.
2. Configure active PowerShell session environment variables without touching permanent machine PATH:
   ```powershell
   $env:Path = "C:\Users\Subodh\miniconda3;C:\Users\Subodh\miniconda3\Scripts;C:\Users\Subodh\miniconda3\Library\bin;" + $env:Path
   ```
3. Verify Conda installation:
   ```powershell
   conda --version
   conda info
   ```

### Phase C: Environment Creation & Baseline Provisioning
1. Initialize a clean Python 3.11 environment:
   ```powershell
   conda create -n osdagbridge-env python=3.11 -y
   ```
2. Verify Python version and interpreter path:
   ```powershell
   & "C:\Users\Subodh\miniconda3\condabin\conda.bat" run -n osdagbridge-env python --version
   ```

### Phase D: Native CAD & Numerical Stack Provisioning
1. Install native C++ and Qt6 GUI packages from verified channels:
   ```powershell
   conda install -n osdagbridge-env --override-channels -c osdag -c geompy -c conda-forge `
     pythonocc-core pyside6 numpy scipy matplotlib-base ifcopenshell shapely fiona `
     pydantic xarray openpyxl navcube -y
   ```
2. Install finite element analysis and visualization backends via pip:
   - For OpenSeesPy on Windows Python 3.11, install matched binary wheels:
     ```powershell
     pip install openseespy==3.7.0.1 openseespywin==3.7.0.1 opsvis
     ```
   *(Note: `openseespywin 3.7.0.3` on PyPI was miscompiled against `python312.dll`, triggering DLL load failures on Python 3.11; `openseespywin 3.7.0.1` cleanly targets `python311.dll` and satisfies the `>=3.2.2.6` requirement).*
3. Install support parser packages:
   ```powershell
   pip install lark pyyaml
   ```
4. Install local OsdagBridge repository in editable development mode (`-e .`):
   ```powershell
   pip install --no-deps -e "F:\FOSSEE internship\source\OsdagBridge"
   ```

---

## 4. Rollback & Troubleshooting Procedures
If any package fails to install or produces binary incompatibility:
1. Document the exact error and stack trace.
2. Remove the isolated environment cleanly:
   ```powershell
   conda env remove -n osdagbridge-env -y
   ```
3. Re-create the environment following this verified deterministic manifest.
