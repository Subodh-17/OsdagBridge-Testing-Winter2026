# Repository Audit: OsdagBridge (`dev` Branch)

## 1. Upstream Repository Metadata
- **Source URL:** `https://github.com/Nidhikhare12/OsdagBridge.git`
- **Local Clone Path:** `F:\FOSSEE internship\source\OsdagBridge`
- **Active Checked-Out Branch:** `dev`
- **Upstream Tracking:** `origin/dev`
- **HEAD Commit SHA:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
- **Commit Date:** Sun Jul 26 13:56:10 2026 +0530
- **Author:** `mhsuhail00 <mhsuhail00@gmail.com>`
- **Commit Message:** `fix: Z,Sa/g,Ah,Av in Report`
- **Modified Files in HEAD Commit:**
  - `src/osdagbridge/desktop/ui/dialogs/additional_input/additional_inputs.py` (+9, -1)
  - `src/osdagbridge/desktop/ui/dialogs/ui_builder/common_ui_builder.py` (+13, -0)
  - `src/osdagbridge/desktop/ui/template_page.py` (+23, -0)

---

## 2. Remote Branch Topology
An audit of remote branch references (`git ls-remote --heads`) revealed 10 active branches:

| Branch Name | Latest Commit SHA | Description / Purpose |
| :--- | :---: | :--- |
| `refs/heads/dev` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **Official target branch for internship testing** |
| `refs/heads/main` | `2cb7ddc8ab2d2e33bf86721cb8a219b82d02df74` | Production release baseline |
| `refs/heads/deck_design` | `1ff170931f2668b121352388e9dfccd3c1c40694` | Feature branch for deck slab calculation routines |
| `refs/heads/nidhi-temp` | `13877a90ba0c61e96ad193cdec76a05826638a45` | Maintainer sandbox branch |
| `refs/heads/optimization` | `16da49ff48ddd6dbbd62ae72eb4cfa2fbd23c549` | Design optimization exploration branch |
| `refs/heads/report` | `e004d75ccfd67eaa4273edfdf7e2f46585648b3e` | LaTeX/PDF reporting module updates |
| `refs/heads/screening-task-plot` | `8505b2355f0bd2685ec48c62150a6a29075815a6` | Plotting features for screening tasks |
| `refs/heads/screening-task-ui` | `aa5714b7912659e75549bcbde9c52bff0dbdfc89` | UI adjustments for screening tasks |
| `refs/heads/temp` | `f06348682d72a94a8680aa8562399b80586f6913` | Transient test commits |
| `refs/heads/test-pr342` | `ec78c22503443003d33ccfdf735cb733bd880533` | PR #342 integration testing |

---

## 3. Architecture Overview: Documented vs. Actual Code Layout

A critical forensic finding is the divergence between the architecture published in `README.md` and the actual source tree on `dev`:

### Documented Layout (README.md)
```
OsdagBridge/
├── docs/
├── examples/
├── tests/
└── src/
    └── osdagbridge/
        ├── core/              # Analysis, design, IO, solvers, codes
        ├── bridge_types/      # Plate girder, box girder, truss
        ├── bridge_components/ # Reusable components
        ├── cli/               # Command-line interface
        ├── desktop/           # PySide6 GUI
        └── web/               # Django + React web stack
```

### Actual Code Layout on Disk
```
OsdagBridge/
├── conda-recipe/              # Conda build packaging recipes
├── constructor/               # Standalone installer builder configuration
├── docs/                      # Sphinx documentation source
├── examples/                  # Example bridge input files
├── tests/                     # 6 placeholder test files
├── tools/                     # Packaging and helper utilities
├── web/                       # Django + React root directory (Stub)
└── src/
    ├── ospgrillage/           # Bundled grillage analysis wrapper (OpenSeesPy adapter)
    └── osdagbridge/
        ├── cli/               # Command-line interface (Stub)
        ├── core/              # Actual location of core engineering logic
        │   ├── boq/           # Bill of Quantities engine
        │   ├── bridge_components/ # Reusable component classes
        │   ├── bridge_types/  # Bridge type implementations (plate_girder, box_girder, truss)
        │   ├── data/          # SQLite database and standard section tables
        │   ├── ifc_export_bridge/ # IFC BIM export utilities
        │   ├── loads/         # IRC load models and placement
        │   ├── reports/       # Report templates and generation
        │   ├── solvers/       # Solvers (OpenSees, OspGrillage, Native)
        │   └── utils/         # Indian standard code implementations (IRC:6, 22, 24)
        └── desktop/           # PySide6 Desktop GUI application
            ├── resources/     # Icons, themes, stylesheets (.qrc/.qss)
            └── ui/            # Windows, dialogs, docks, and CAD viewers
```

### Key Architectural Divergences:
1. **Bridge Types & Components Location:** `bridge_types` and `bridge_components` reside inside `osdagbridge/core/`, not directly under `osdagbridge/`.
2. **Bundled `ospgrillage` Package:** The repository vendors a full internal copy of `ospgrillage` inside `src/ospgrillage/`, which interfaces directly with `openseespy`.
3. **Web Application Relocation:** `web/` is located at repository root, not inside `src/osdagbridge/web/`.

---

## 4. Module Implementation Status: Production Code vs. Stubs

| Subsystem / Module | Path | Implementation State | Findings |
| :--- | :--- | :---: | :--- |
| **Plate Girder Bridge** | `src/osdagbridge/core/bridge_types/plate_girder/` | **COMPLETE** | Production-ready: 223 KB `plategirderbridge.py`, 185 KB `designer.py`, 123 KB `analyser.py`. |
| **Desktop GUI (PySide6)** | `src/osdagbridge/desktop/` | **COMPLETE** | Full GUI: `CustomWindow`, input docks, output docks, 3D CAD OpenCASCADE viewer, dialogs. |
| **Box Girder Bridge** | `src/osdagbridge/core/bridge_types/box_girder/` | **STUB** | 7 files, each containing only 1 line (e.g. `"""box_girder analyser (stub)."""`). |
| **Truss Bridge** | `src/osdagbridge/core/bridge_types/truss/` | **STUB** | 7 files, each containing only 1 line stub docstring. |
| **CLI Application** | `src/osdagbridge/cli/` | **STUB** | `commands.py` contains dummy `print("analyze", path)`. Commands in README do not exist. |
| **Web Backend** | `web/backend/` | **STUB** | `manage.py` contains `print("Django manage stub")`. No Django project structure. |
| **Web Frontend** | `web/frontend/` | **STUB** | Only dummy `package.json` (`"version": "0.0.0"`). No React application. |

**Conclusion:** The OsdagBridge repository is currently a **single-module desktop application** dedicated to **Plate Girder Bridges**. Testing focus must be 100% concentrated on this module.

---

## 5. Test Suite & Continuous Integration Audit

### 5.1 Test Suite Status [STATIC]
An inspection of `tests/` revealed six test files across two directories:
```
tests/
├── integration/
│   ├── test_api_plate_girder.py      (46 bytes)
│   ├── test_cli_plate_girder.py      (46 bytes)
│   └── verification_ddcl_cases.py    (47 bytes)
└── unit/
    ├── test_analyser.py              (51 bytes)
    ├── test_designer.py              (51 bytes)
    └── test_io.py                    (45 bytes)
```

**Content Analysis:**
Every test file contains solely a placeholder function asserting `True`:
```python
def test_api_placeholder():
    assert True
```
- **Real Automated Test Coverage:** **0.00%**.
- No calculation validation tests exist in the official repository.
- Developing comprehensive automated test scripts in `testing/scripts/` during Phase 2 will provide immense value.

### 5.2 CI Pipeline Audit [STATIC]
- **README Claim:** *"Continuous integration runs automatically through GitHub Actions (`.github/workflows/ci.yml`)."*
- **Audit Finding:** `.github/workflows/ci.yml` **DOES NOT EXIST**.
- **Existing Workflows:** Only `.github/workflows/conda-publish.yml` exists. It only triggers on pushes to the `packaging` branch and builds conda binaries for Ubuntu and Windows.
- **Risk:** Pull requests and commits on `dev` have zero automated regression gates running on GitHub.
