# OsdagBridge — Software Testing & Issue Reporting (FOSSEE Winter Internship 2026)

**Candidate:** Subodh Shivmurti Bansode (`Subodh-17` | `subodh171011@gmail.com`)  
**Task:** OsdagBridge Software Testing & Issue Reporting — FOSSEE Winter Internship 2026  
**Host Institution:** FOSSEE, IIT Bombay  
**Software Under Test:** [Nidhikhare12/OsdagBridge](https://github.com/Nidhikhare12/OsdagBridge)  
**Baseline Lineage:** Branch `dev`, Commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Governing Standards:** IRC:6-2017, IRC:22-2015, IRC:24-2010, IS 800:2007  

---

## 1. Executive Summary & Testing Objectives

This repository contains the complete, evidence-backed software testing, defect analysis, issue reporting, and engineering remediation package for OsdagBridge's composite plate girder bridge module.

### Core Testing Objectives
1. **Verification of Structural Mechanics & Design Calculations:** Rigorously verify whether finite-element grillage compilation, load generation, partial safety factor scaling, and component capacity checks conform to IRC and IS specifications.
2. **Defect Identification & Forensic Traceability:** Reconstruct suspected anomalies, identify exact code-level root causes in `src/osdagbridge/` and `src/ospgrillage/`, and provide minimal, isolated remediation patches.
3. **Multi-Run Stability & GUI Integrity:** Audit parameter persistence, state reset behavior across consecutive design runs, and 3D CAD visualization in the desktop interface.
4. **Reproducibility & Evidence Governance:** Secure all baseline and post-fix evidence with cryptographic SHA-256 manifests, HMAC-SHA256 signatures, and automated regression suites.

---

## 2. Source Code Lineage & Remediation Batches

### Baseline Upstream
- **Repository:** `https://github.com/Nidhikhare12/OsdagBridge`
- **Branch:** `dev` @ commit `d74f56d`

### The Three Formal Remediation Batches (`fix/phase-3-engineering-remediation` @ `f555075`)
Our formal engineering remediation comprises 5 defects resolved in 6 small, atomic commits on branch `fix/phase-3-engineering-remediation` (HEAD: `f55507563175c2bd7f6cf9ec701ec123e228d50d`):

- **Batch 1 (Commits 1–3):**
  - `0001` (DEF-12): Correct bearing-stiffener web buckling capacity formula from IS 800:2007 Clause 8.7.1.5 (fixed 3,384× overstatement).
  - `0002` (DEF-08): Correct executive summary status table to dynamically reflect component DCR failure.
  - `0003` (DEF-11): Align `BridgeConfig` girder count with physical layout.
- **Batch 2 (Commits 4–5):**
  - `0004` (DEF-18-LINE): Correct finite-element line load magnitude scaling, vector centroid, and coordinate indices.
  - `0005` (DEF-18-PATCH): Eliminate patch load corner node overcounting in 2D grillage cells.
- **Batch 3 (Commit 6):**
  - `0006` (DEF-01): Preserve and compound component partial safety factors during finite-element load compilation.

### Follow-Up Moving-Load Regression Fix (`fix/moving-load-mesh-mapping` @ `bbfe14c`)
- **Patch `0007` (DEF-MOVING-LOAD-MESH):**
  - *Context:* Batch 2 commit `0004` (`34cd4bf`) added strict out-of-domain checking in `_assign_load_to_four_node` by raising an unconditional `ValueError` when coordinates fall outside the grillage mesh. During live moving-vehicle analysis, multi-axle vehicles traverse incrementally from $x = -L_{\text{veh}}$ to $x = L_{\text{span}} + L_{\text{veh}}$, and across angled skew abutments ($z \tan \theta$). Axles outside the physical deck raised fatal `ValueError` exceptions, halting all skewed bridge designs.
  - *Structural Mechanics Resolution:* In structural mechanics, vehicle axles off the bridge deck rest on the approach roadway embankment/backfill and transmit zero load to the superstructure grillage. Commit `bbfe14c` added `allow_out_of_mesh=True` for vehicle moving-load point distributions (returning `[]` for off-bridge axles while retaining fail-closed `ValueError` by default for direct API calls), added $10^{-9}$ floating-point tolerance on cell boundaries to prevent edge-chatter rejection, and expanded coordinate duck-typing to accept `Point`, `LoadVertex`, `tuple`, `list`, and `np.ndarray`.
- **Packaged Source State:** The `source/OsdagBridge/` directory in this repository includes all 7 verified commits (`bbfe14c`). All commits are also available as clean, reproducible unified patches in `patches/0001`–`0007`.

---

## 3. Repository Structure

```text
OsdagBridge-Testing-Winter2026/
├── README.md                                # Master submission overview and documentation
├── run_submission_tests.bat                 # 1-Click turnkey test runner (Windows)
├── patches/                                 # Unified Git patches (0001 to 0007)
│   ├── 0001-fix-designer-correct-bearing-stiffener-web-buckling-.patch
│   ├── 0002-fix-reports-dynamically-evaluate-component-DCRs-in-e.patch
│   ├── 0003-fix-designer-align-BridgeConfig-girder-count-with-ph.patch
│   ├── 0004-fix-ospgrillage-correct-line-load-magnitude-scaling-.patch
│   ├── 0005-fix-ospgrillage-eliminate-patch-load-corner-overcoun.patch
│   ├── 0006-fix-ospgrillage-preserve-component-load-factors-in-l.patch
│   └── 0007-fix-ospgrillage-handle-moving-load-coordinates-outsi.patch
├── source/
│   └── OsdagBridge/                         # Application source code at commit bbfe14c
├── testing/
│   ├── test_cases/
│   │   ├── baseline_regression/             # TC-REG-* tests & test_evidence_governance.py
│   │   └── phase_3/                         # Batches 2 & 3 + moving load acceptance suites
│   ├── evidence/                            # Sealed run logs, JSON manifests, and HMACs
│   └── scripts/                             # Verification, report, and packaging scripts
├── evidence/
│   └── screenshots/
│       └── live_gui_verification/           # Full-window & 3D CAD screenshots (30m & 25m skew)
├── reports/                                 # Engineering audit reports & Defect Traceability Matrix
│   ├── SUBMISSION_TECHNICAL_REPORT.md       # Master Technical Report source
│   └── phase_3/                             # Phase 3 remediation & reconciliation records
├── documentation/                           # Environment setup, defect registers, task specs
└── submission/
    ├── pdf/                                 # Publication-grade Master Technical Report PDF
    ├── osi/                                 # Verified sample project input file (.osi)
    ├── github_issues/                       # Exhaustively de-duplicated GitHub issue drafts
    └── video/                               # Live screencast demonstration script & teleprompter
```

*(Note: Candidate resume is intentionally excluded from the public/collaborator GitHub repository for privacy and is delivered in the official submission form package).*

---

## 4. Test Execution & Verification

### Prerequisites
- Python 3.12 (Miniconda / Anaconda recommended)
- Dependencies installed from `source/OsdagBridge/environment.yml` (PySide6, OpenCASCADE `pythonocc-core`, OpenSeesPy, ospgrillage, NumPy, SciPy, Matplotlib)

### Option A: 1-Click Verification (Windows)
Double-click `run_submission_tests.bat` or run:
```bat
run_submission_tests.bat
```

### Option B: Manual CLI Execution
```powershell
# 1. Evidence Governance Suite (cryptographic seal and trust-ledger verification)
python testing\test_cases\baseline_regression\test_evidence_governance.py

# 2. Batch 2 Statics Conservation & Equilibrium Suite (17 tests)
python -m unittest testing\test_cases\phase_3\test_batch_2_comprehensive.py

# 3. Batch 3 Component Load Factor Scaling Suite (15 tests)
python -m unittest testing\test_cases\phase_3\test_batch_3_factor_scaling.py

# 4. Moving-Load Mesh Mapping Suite (10 tests)
python -m unittest testing\test_cases\phase_3\test_moving_load_mesh_mapping.py
```

### Verification Results Matrix

| Test Suite | Purpose | Tests | Status |
| :--- | :--- | :---: | :---: |
| `test_evidence_governance.py` | Validates write guards, SHA-256 manifests, HMAC seals, and SQLite integrity | 27 | **27/27 PASS** |
| `test_batch_2_comprehensive.py` | Verifies force, centroid, and reaction statics for uniform, trapezoidal, and patch loads | 17 | **17/17 PASS** |
| `test_batch_3_factor_scaling.py` | Verifies load factor preservation across all load types and compounds | 15 | **15/15 PASS** |
| `test_moving_load_mesh_mapping.py` | Verifies moving-load mesh mapping on orthogonal, skewed ($+10^\circ, -10^\circ$), and dual-carriageway decks | 10 | **10/10 PASS** |
| **Total Automated Suites** | **Distinct, non-overlapping verification tests** | **69** | **69/69 PASS** |

*(Full Phase 3 discovery across all sub-suites runs 58 tests in 31.2s with 0 failures, 0 errors).*

---

## 5. Live Interactive Desktop GUI Verification

Both target configurations were verified interactively in the desktop application:
1. **Configuration A ($30\text{ m}$ span, $7.5\text{ m}$ carriageway, $10^\circ$ skew):**
   - Full Design executed in $62.76\text{ s}$.
   - Output Dock populated with 4 girders (G1–G4) across 49 load combinations (ULS Basic 1–6, Accidental 1–3, Seismic 1–4, SLS Rare 1–6, Frequent, Quasi-Permanent, and Design Envelope).
   - OpenCASCADE 3D CAD rendered all superstructure components. Intercepted errors: **0**.
2. **Configuration B ($25\text{ m}$ span, $7.5\text{ m}$ carriageway, $10^\circ$ skew, Median Yes, Single-side Footpath):**
   - Full Design executed in $66.93\text{ s}$.
   - Output Dock populated across 53 load combinations including footpath and median barrier loadings.
   - OpenCASCADE 3D CAD rendered asymmetric deck, median barrier, and internal cross bracings. Intercepted errors: **0**.

Screenshots are available in `evidence/screenshots/live_gui_verification/`.

---

## 6. Engineering Limitations & Boundaries

1. **Scope of Remediations:** Only 5 of the 20 cataloged defects (Batches 1–3 + follow-up commit) are committed to source code. The remaining 15 defects are thoroughly documented in `reports/SUBMISSION_TECHNICAL_REPORT.md` and `reports/phase_3/` with proposed code diffs and regression specifications.
2. **Moving Load Point Load Dropping:** Setting `allow_out_of_mesh=True` during vehicle traversal correctly assigns 0 grillage reaction to off-bridge vehicle axles. Direct manual point load calls retain default `allow_out_of_mesh=False` to fail-closed on misplaced inputs.
3. **Certification Disclaimer:** This work was performed for the FOSSEE Winter Internship 2026 screening evaluation. It does not constitute professional certification of the entire OsdagBridge codebase or all civil engineering design outputs.

---

## 7. Author & Licensing

- **Author:** Subodh Shivmurti Bansode  
- **Email:** `subodh171011@gmail.com`  
- **GitHub:** [@Subodh-17](https://github.com/Subodh-17)  
- **Task Evaluation Target:** FOSSEE Osdag Team, IIT Bombay
