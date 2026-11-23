# PHASE 1D BASELINE PRESERVATION & FORENSIC RECORD

**Workspace:** `F:\FOSSEE internship`  
**Repository:** `F:\FOSSEE internship\source\OsdagBridge`  
**Baseline Git Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Branch:** `dev`  
**Evaluation Status:** **NO-GO (Defects Preserved, Working Tree Locked)**  
**Date:** 2026-11-16 (Updated with Reconciled Evidence)  

---

## 1. Executive Summary & Directive Adherence

Following the independent engineering audit (`PHASE_1D_INDEPENDENT_AUDIT.md`) and the subsequent conflict reconciliation (`PHASE_2_REVIEW_RECONCILIATION.md`), the Phase 1D Plate Girder Bridge computational run has been designated **EXECUTION SUCCESSFUL — ENGINEERING VALIDATION NO-GO**. 

While the software completed the end-to-end computational pipeline without unhandled Python exceptions, generating a 1,066-key output dictionary and a 51-page PDF design report, rigorous independent technical audit revealed that the structural engineering results are invalid due to severe underlying calculation defects.

In strict compliance with project directives:
1. **Zero Source Code Alteration:** No application code has been modified, patched, or refactored.
2. **Zero Package Changes:** No conda or pip dependencies have been installed, upgraded, downgraded, or removed.
3. **Database Integrity Maintained:** Both SQLite databases (`osdag_core` and `osdagbridge`) remain strictly read-only and unaltered.
4. **No Result Fabrication:** No tolerances or thresholds have been manipulated to convert an engineering FAIL into a PASS. All previously cited fabricated numbers have been expunged and replaced with authentic values from the raw output dictionary.
5. **Baseline State Frozen:** All raw evidence, logs, and artifacts from Phase 1D have been cryptographically hashed and preserved as a permanent regression baseline for Phase 2.

---

## 2. Baseline Repository & Environment Fingerprint

### 2.1 Git Repository State
- **Repository Path:** `F:\FOSSEE internship\source\OsdagBridge`
- **Current Branch:** `dev` (`origin/dev` tracking)
- **Commit SHA:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
- **Commit Date:** Sun Jul 26 13:56:10 2026 +0530
- **Commit Author:** `mhsuhail00 <mhsuhail00@gmail.com>`
- **Commit Subject:** `fix: Z,Sa/g,Ah,Av in Report`
- **Working Tree Tracked Status:** `CLEAN` (`git status` reports nothing to commit, working tree clean)

### 2.2 Python Runtime Fingerprint
- **Target Environment:** `osdagbridge-py312`
- **Python Binary:** `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`
- **Python Version:** `3.12.16 | packaged by conda-forge | (main, Oct 26 2026, 11:29:01) [MSC v.1944 64 bit (AMD64)]`
- **Isolation Setting:** `PYTHONNOUSERSITE = 1` (verified; host site-packages strictly excluded)
- **Host Operating System:** Windows 11 Build 26300 (`platform.platform() = Windows-11-10.0.26300-SP0`, `sys.getwindowsversion().build = 26300`)

### 2.3 Dependency Package Matrix & Channel Provenance

| Package Name | Conda Channel / Origin | Installed Build Version | Notes / Metadata Status |
| :--- | :--- | :--- | :--- |
| **`osdag`** | `osdag` | `2026.04.0.0` (build `py_0`) | Conda package index reports `2026.04.0.0`; runtime `osdag.__version__` reports `'2025.01.a.2'`; `importlib.metadata` reports `'0.0.0'` |
| **`osdag_latex_env`**| `osdag` | `1.0.2` (build `py313_0`) | Environment helper package providing TeX Live `pdflatex` |
| **`osdagbridge`** | Local / PyPI | `1.0.0` (`pypi_0`) | Application source under test |
| **`ospgrillage`** | Vendored Source | `src/ospgrillage/` | Vendored directly inside repository tree (based on PyPI 0.6.0) |
| **`pyside6`** | `conda-forge` | `6.11.3` (build `py312hdb84042_1`) | Qt 6.11.3 runtime bindings |
| **`pythonocc-core`**| `conda-forge` | `8.0.1.2` (build `all_h173387a_0`) | OpenCASCADE 8.0.1 Python bindings |
| **`occt`** | `conda-forge` | `8.0.1` (build `all_h6eddace_201`) | OpenCASCADE native C++ libraries |
| **`openseespy`** | `pypi` | `3.8.0.0` | OpenSees finite-element solver |
| **`openseespywin`**| `pypi` | `3.8.0.0` | Windows native OpenSees runtime engine |
| **`opsvis`** | `pypi` | `1.3.7` | OpenSees visualization package |
| **`ifcopenshell`** | `conda-forge` | `0.9.0post1` (build `py312h062a554_1`) | IFC export engine |
| **`numpy`** | `conda-forge` | `2.5.5` (build `py312ha3f287d_0`) | Numerical computations |
| **`scipy`** | `conda-forge` | `1.18.1` (build `py312h8847828_2`) | Scientific routines |
| **`matplotlib`** | `conda-forge` | `3.11.2` (build `py312hf9659c1_1`) | 2D plotting engine |
| **`plotly`** | `conda-forge` | `7.1.0` (build `pyhd8ed1ab_0`) | Interactive graphing |

---

## 3. Cryptographic Baseline Evidence Hashes

All evidence files generated during the Phase 1D end-to-end execution have been cataloged and verified with SHA-256 checksums to ensure uncompromised auditability.

### 3.1 Phase 1D Execution Evidence (`testing/evidence/phase_1d/`)

| File Name | File Size (Bytes) | SHA-256 Checksum | Verified Attributes |
| :--- | :--- | :--- | :--- |
| `01_end_to_end_design_full_window.png` | 79,374 | `BDF9141B8A8330560CFB88322482A6D8DE0971D761B199D9656A95D909246F17` | Full desktop window capture |
| `02_3d_cad_bridge_model.png` | 13,485 | `D8975350123784E2FC3AF34C7EA800015F0FA396E6AAFFEE57465D37C1E941AC` | RGBA image (793x1103), 92.95% transparent pixels |
| `execution.log` | 173,835 | `27D57835EABEDD4A5FDB54900DCC137E0BEED96F5DCB11392846F1D672036013` | Complete console log trace (2,248 lines) |
| `input_configuration.json` | 44,653 | `31AE62DC08A0DE7797AA4CA6451A178FD46CC66BBA4C00F7414021336FB10191` | Canonical 572-key input specification |
| `input_configuration.yaml` | 41,320 | `36E0E49EDAA42F6B98ABA06F32C2BCD8E73A668DC589FE0D80C8BD60163D19D8` | YAML serialized input configuration |
| `output_dictionary_snapshot.json` | 3,333,439 | `429A3198FC93C157A5BD5EE13C74B95612C3410D35A7BE1F246867167991A5AB` | Complete 1,066-key output dictionary snapshot |
| `phase_1d_design_report.pdf` | 402,485 | `8457482DBFEE9265BF84CC6D42DAD4E7FF767D2119D2CE330A8B449DEB8E3695` | **51-page** compiled PDF design report |
| `phase_1d_design_report.tex` | 91,775 | `33F4E581F35A6D40098F5CF7CD4491D056AF5E2CFD3DD1E70E221CEE44D920FF` | Generated LaTeX source (3,260 lines) |
| `task_a_metadata.json` | 1,479 | `73F7D65901AF396A4A304E642E8FC4DB29C1222832746A4B3825149F5B7A83B9` | Task A environment and metadata audit |
| `task_b_database_audit.json` | 106,119 | `193A08E259AC77C9261B94741C6AAD83B780A30D48F220F7091DE19B730BA13C` | Task B SQLite dual-database schema audit |

### 3.2 Database File Fingerprints

| Database Identifier | Absolute Filesystem Location | Size (Bytes) | SHA-256 Checksum | Last Modified (UTC) |
| :--- | :--- | :--- | :--- | :--- |
| **`osdag_core_db`** | `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\Lib\site-packages\osdag_core\data\ResourceFiles\Database\Intg_osdag.sqlite` | 249,856 | `fed15f8b7c045d9919202e7e251c79fd6c30495f1a90876b9cb6b6661220e218` | 2026-11-16 04:57:44 |
| **`osdagbridge_local_db`** | `F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\core\data\ResourceFiles\Intg_osdag.sqlite` | 270,336 | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | 2026-11-15 12:26:13 |
| **`weather_sqlite`** | `F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\core\data\project_location\weather.sqlite` | 180,224 | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | 2026-11-16 05:48:51 |

---

## 4. Forensic Investigation of `weather.sqlite` & Filesystem Hygiene

During Phase 1D Task B and GUI verification, a new SQLite database file was generated inside the repository tree:  
`src/osdagbridge/core/data/project_location/weather.sqlite`.

### 4.1 File Metadata
- **Path:** `F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\core\data\project_location\weather.sqlite`
- **Size:** 180,224 bytes (176 KB)
- **Timestamp:** 2026-11-16T11:18:51.200772 (+05:30)
- **SHA-256:** `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98`

### 4.2 Creation Mechanism in Source Code
Forensic static analysis traced the exact trigger to `src/osdagbridge/core/data/project_location/database.py`:
```python
# Lines 12, 21-30 in database.py
class Database:
    def __init__(self, db_name: str = 'weather.sqlite'):
        self.db_name = db_name

    def connect(self):
        db_missing = not os.path.exists(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        if db_missing or not self._table_exists("stations"):
            schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
            if os.path.exists(schema_file):
                with open(schema_file, 'r', encoding='utf-8') as f:
                    self.connection.executescript(f.read())
                self.connection.commit()
```

Every caller in OsdagBridge explicitly constructs an **absolute path** anchored on `__file__`:
1. `src/osdagbridge/core/data/project_location/zone_lookup.py:183`:
   `db_path = os.path.join(os.path.dirname(__file__), "weather.sqlite")`
2. `src/osdagbridge/core/bridge_types/plate_girder/ui_fields_project_location.py:16-17`:
   `DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "project_location", "weather.sqlite"))`
3. `src/osdagbridge/core/reports/report_generator.py:664-666`:
   `from ...ui_fields_project_location import DB_PATH; db = Database(DB_PATH)`

When any of these modules executes, `Database.connect()` detects that `self.db_name` does not exist on disk, creates the 0-byte file via `sqlite3.connect()`, and executes `schema.sql` to populate geographic weather stations, seismic zone mappings, and wind speeds directly into the package directory inside the source tree.

### 4.3 Gitignore Interaction and Ignored Files Inventory
Although `weather.sqlite` was generated inside the repository tree, standard `git status` reported `working tree clean` because `source/OsdagBridge/.gitignore` (lines 257–259) specifies:
```gitignore
*.sqlite
*.sqlite3
!src/osdagbridge/core/data/ResourceFiles/Intg_osdag.sqlite
```
Executing detailed `git status --ignored` reveals that the source tree actually contains ignored runtime artifacts:
1. `src/osdagbridge/core/data/project_location/weather.sqlite` (180,224 bytes)
2. `src/osdagbridge.egg-info/` (6 editable install files)
3. 30 `__pycache__/` directories (233 compiled `.pyc` files)

This distinguishes between a clean Git status of tracked files and an altered physical filesystem.

---

## 5. Cross-Platform Evidence Integrity Analysis

The independent audit and reconciliation verified the bit-level comparison between the Phase 1D Windows run and a parallel Linux verification run on the identical baseline commit (`d74f56d`).

### 5.1 Deterministic Consistency
1. **Input Equivalence:** Both platforms consumed the identical 572-key input specification (`input_configuration.json`).
2. **Output Dictionary Identity:** The generated 1,066-key output dictionary matched across all 35,404 numeric entries:
   - Applied ULS bending moment: $M_u = 1,526.50\text{ kNm}$
   - Applied ULS shear force: $V_u = 226.14\text{ kN}$
   - Support reaction: $R = 304.97\text{ kN}$
   - Applied SLS bending moment: $M_{sls} = 1,455.73\text{ kNm}$
   - Applied SLS shear force: $V_{sls} = 215.25\text{ kN}$
   - Governing Fatigue DCR: $1.9746$ (FAIL), with $\Delta \sigma = 182.633\text{ MPa}$ and $\tau_r = 41.268\text{ MPa}$
   - Snapped plate girder dimensions: $1340\text{ mm}$ total depth, $410 \times 18\text{ mm}$ top/bottom flanges, $8\text{ mm}$ web ($d_w = 1304\text{ mm}$)
3. **Implication:** The computational defects identified in Phase 1D are **100% platform-independent algorithmic and architectural defects** in OsdagBridge and vendored `ospgrillage`.

### 5.2 CAD Image Capture Analysis (`02_3d_cad_bridge_model.png`)
- **Image Format & Properties:** RGBA format, dimensions $793 \times 1103$, 874,679 total pixels.
- **Alpha Channel Distribution:** 813,005 pixels (92.95%) have an alpha value of exactly 0 ($\alpha = 0$, completely transparent). The remaining 61,674 non-transparent pixels have a mean RGB intensity of 246.05.
- **Root Cause:** In `testing/scripts/execute_phase_1d_e2e.py:220–226`, the test script invoked Qt's `widget.grab()` on `cad_w`. On Windows, OpenCASCADE (`pythonocc-core` 8.0.1.2 / OCCT 8.0.1) renders via native hardware OpenGL WGL swap chains. Calling Qt `widget.grab()` copies Qt's software `QPaintDevice` backing store, which remains transparent, producing an image that appears white or black depending on the image viewer.
- **Model Integrity:** In-memory inspection confirmed that OpenCASCADE successfully generated all 83 3D TopoDS solid shapes. The defect lies entirely within the test harness grab method; using OpenCASCADE's native `View.Dump()` or `ExportToImage()` produces a fully rendered 3D image.

---

## 6. Historical Notes & Document Errata

To maintain complete historical auditability, earlier versions of this document contained five inaccurate or unsupported assertions that were identified during independent review and have been formally corrected:
1. **Report Page Count:** Corrected from 38 pages to **51 pages** (verified via object `/Count 51` in the PDF).
2. **`osdag.__version__` Provenance:** Corrected from `'0.0.0'` to **`'2025.01.a.2'`** (verified via runtime inspection of `osdag/__init__.py`).
3. **Operating System Build:** Corrected from Windows Build 26100 to **Build 26300** (verified via `sys.getwindowsversion()`).
4. **Invented Cross-Platform Parity Values:** Expunged previously cited figures ($1,489,692.0\text{ N}\cdot\text{m}$ and $394,812.5\text{ N}$) which do not exist in the output dictionary. Replaced with authentic verified values ($M_u = 1526.50\text{ kNm}$, $V_u = 226.14\text{ kN}$, $M_{sls} = 1455.73\text{ kNm}$).
5. **Database Path Construction:** Corrected description from relative CWD path to **absolute path anchored on `__file__`** in all callers.

---

## 7. Preservation Conclusion

The Phase 1D baseline is permanently locked:
- Git HEAD is frozen at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` on `dev`.
- All 10 evidence files and 3 databases are verified, hashed, and cryptographically intact.
- The defect register (`PHASE_1D_DEFECT_REGISTER.md`) and regression test plan (`PHASE_2_TEST_PLAN.md`) establish the quality roadmap for Phase 2.
