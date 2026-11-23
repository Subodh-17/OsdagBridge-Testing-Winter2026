# OsdagBridge — Software Testing & Issue Reporting (FOSSEE Winter Internship 2026)

**Candidate:** Subodh Shivmurti Bansode (`Subodh-17`)  
**Task:** OsdagBridge Software Testing & Issue Reporting — FOSSEE Winter Internship 2026 Screening Task  
**Host Institution:** FOSSEE, IIT Bombay  
**Software Under Test:** [Nidhikhare12/OsdagBridge](https://github.com/Nidhikhare12/OsdagBridge)  
**Baseline Lineage:** Branch `dev`, Commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Remediated Source HEAD:** Commit `bbfe14c7dfe1954bb890579f7e076edfbe180fd6`  
**Governing Standards:** IRC:6-2017, IRC:22-2015, IRC:24-2010, IS 800:2007  

---

## 1. Project Overview & Screening-Task Context

This repository contains the complete, evidence-backed software testing, defect analysis, issue reporting, and engineering remediation package for the composite plate girder bridge module of OsdagBridge.

### Core Testing Objectives
1. **Verification of Structural Mechanics & Design Calculations:** Verify whether finite-element grillage compilation, load generation, partial safety factor scaling, and component capacity checks conform strictly to IRC and IS specifications.
2. **Defect Identification & Forensic Traceability:** Reconstruct suspected anomalies, identify exact code-level root causes in `src/osdagbridge/` and `src/ospgrillage/`, and provide minimal, isolated remediation patches.
3. **Multi-Run Stability & GUI Integrity:** Audit parameter persistence, state reset behavior across consecutive design runs, and 3D CAD visualization in the desktop interface.
4. **Reproducibility & Evidence Governance:** Secure all baseline and post-fix evidence with cryptographic SHA-256 manifests, HMAC-SHA256 signatures, and automated regression suites.

---

## 2. Quick Start & Key Documents

1. **Master Technical Report:** [`submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf`](file:///submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf) — Start here. A 7-page executive engineering report covering defect taxonomy, mathematical proofs, remediation benchmarks, full-pipeline verification, and upstream issue cross-references.
2. **Test Runner:** Run `run_submission_tests.bat` (Windows) or `run_submission_tests.sh` (Linux/macOS) from the repository root to execute the automated verification test suites.
3. **Headless Full Design Execution:** Run `python testing/scripts/run_full_design_from_osi.py` to execute a complete end-to-end design of the sample bridge project.
4. **Interactive GUI Launch:** Launch the desktop application directly from the packaged source:
   ```bat
   cd source\OsdagBridge\src
   python -m osdagbridge.desktop
   ```

---

## 3. Source Lineage & Remediation Batches

### Baseline Upstream
- **Repository:** `https://github.com/Nidhikhare12/OsdagBridge`
- **Branch:** `dev` @ commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

### The Three Formal Remediation Batches (`fix/phase-3-engineering-remediation` @ `f555075`)
Our formal engineering remediation comprises 5 critical defects resolved in 6 small, atomic commits on branch `fix/phase-3-engineering-remediation` (HEAD: `f55507563175c2bd7f6cf9ec701ec123e228d50d`):

- **Batch 1 (Commits 1–3):**
  - Patch `0001` (DEF-12): Correct bearing-stiffener web buckling capacity formula from IS 800:2007 Clause 8.7.1.5 (eliminates ~3,384× overstatement).
  - Patch `0002` (DEF-08): Correct executive summary status table to dynamically reflect component DCR failure.
  - Patch `0003` (DEF-11): Align `BridgeConfig` girder count with physical layout.
- **Batch 2 (Commits 4–5):**
  - Patch `0004` (DEF-18-LINE): Correct finite-element line load magnitude scaling, vector centroid, and coordinate indices.
  - Patch `0005` (DEF-18-PATCH): Eliminate patch load corner node overcounting in 2D grillage cells.
- **Batch 3 (Commit 6):**
  - Patch `0006` (DEF-01): Preserve and compound component partial safety factors during finite-element load compilation.

### Follow-Up Moving-Load Regression Fix (`fix/moving-load-mesh-mapping` @ `bbfe14c`)
- **Patch `0007` (DEF-MOVING-LOAD-MESH):** Follow-up commit `bbfe14c` on branch `fix/moving-load-mesh-mapping` (parent `f555075`). Resolves a moving-load point load mapping regression where vehicle axles crossing outside deck boundaries raised an unhandled `ValueError`. Vehicle point loads off the deck now contribute zero reaction, while non-vehicle point loads retain strict fail-closed boundary validation.

### Applying Patches Upstream
All 7 commits are exported as clean git patches in [`patches/`](file:///patches/):
```bash
git clone https://github.com/Nidhikhare12/OsdagBridge.git && cd OsdagBridge
git checkout -b fix d74f56dd7f22925fb8148cabf5740ed8d1e39ff3
git am ../patches/*.patch
```
The tree in [`source/OsdagBridge/`](file:///source/OsdagBridge/) already has all 7 patches applied (`bbfe14c`), allowing all tests to execute out of the box without manual patch application.

---

## 4. Repository Structure

| Path | Contents |
|:--|:--|
| `submission/pdf/` | Master Technical Report PDF (`OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf`) |
| `submission/osi/` | Verified sample bridge project file (`sample_24m_composite_plate_girder.osi`) and documentation |
| `submission/github_issues/` | Formatted issue writeups and peer comments prepared for upstream filing |
| `submission/video/` | Submission video recording script and presentation guide *(candidate video submitted via portal)* |
| `source/OsdagBridge/` | Remediated OsdagBridge source code at commit `bbfe14c` |
| `patches/` | Seven atomic git patches (`0001` through `0007`) matching commits |
| `testing/test_cases/` | Verification suites: governance (`baseline_regression/`) and acceptance (`phase_3/`) |
| `testing/evidence/` | HMAC-sealed logs and manifests: baseline failures (`phase_2_13/`) and post-fix passes (`phase_3/`) |
| `testing/evidence/phase_3/full_design_check/` | Headless full design check comparative logs across `d74f56d`, `f555075`, and `bbfe14c` |
| `evidence/screenshots/live_gui_verification/` | High-resolution screenshots of live desktop GUI design runs on the final code |
| `reports/` | Detailed engineering reports across testing phases, defect registers, and verification summaries |
| `documentation/` | Environment migration guides, test plan specifications, and issue registers |

*(Note: Candidate resume is submitted privately via the FOSSEE portal and intentionally excluded from public git tracking).*

---

## 5. Environment Requirements & Reproduction Instructions

### A. Lightweight Python 3.12 Environment (Pip Set)
Runs the evidence governance suite, Batch 2 load conservation suites, Batch 3 factor scaling suite, and the moving-load mesh mapping suite (58 Phase 3 tests + 27 governance tests):
```bash
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r testing/requirements-tests.txt
```

### B. Full Conda Environment (`osdagbridge-py312`)
Required for the full-pipeline live-load conservation suite, headless end-to-end design script (`run_full_design_from_osi.py`), and the desktop GUI. Requires `PySide6`, `pythonocc-core`, and `osdag` from the `osdag` conda channel:
- Upstream specification: [`source/OsdagBridge/environment.yml`](file:///source/OsdagBridge/environment.yml)
- Verified migration setup: [`documentation/PHASE_1C_ENVIRONMENT_MIGRATION_REPORT.md`](file:///documentation/PHASE_1C_ENVIRONMENT_MIGRATION_REPORT.md)

### Test Execution Commands
From the repository root:
```bat
# Run turnkey verification test runner:
run_submission_tests.bat          # Linux/macOS: ./run_submission_tests.sh

# Run headless full design check of sample project:
python testing\scripts\run_full_design_from_osi.py

# Launch desktop GUI:
cd source\OsdagBridge\src
python -m osdagbridge.desktop
```

---

## 6. Verification Results

| Verification Suite | Target Defect / Scope | Test Count | Status |
|:--|:--|:--:|:--:|
| **Evidence Governance** | Manifest integrity, HMAC verification, adversarial injection rejection | 27 | **27/27 PASS** |
| **Batch 2 Load Conservation** | DEF-18: Comprehensive, line load, and patch load equilibrium | 17 | **17/17 PASS** |
| **Batch 3 Factor Scaling** | DEF-01: Load factor scaling & compounding (re-verifies Batch 1) | 15 | **15/15 PASS** |
| **Moving-Load Mesh Mapping** | DEF-MOVING-LOAD-MESH: Point-load mapping & axle traversal | 10 | **10/10 PASS** |
| **Full-Pipeline Live-Load** | Live-load conservation compiled from `.osi` across bridge geometries | 3 | **3/3 PASS** |
| **Total Phase 3 Verification** | **Combined functional & full-pipeline acceptance test suite** | **61** | **61/61 PASS** |

### Live Interactive Desktop GUI Verification
Both target configurations were verified interactively in the desktop application:
1. **Configuration A (30 m span, 7.5 m carriageway, 10° skew):**
   - Full Design executed successfully.
   - Output Dock populated with 4 girders (G1–G4) across 49 load combinations.
   - OpenCASCADE 3D CAD rendered all superstructure components with 0 errors.
2. **Configuration B (25 m span, 7.5 m carriageway, 10° skew, Median Yes, Single-side Footpath):**
   - Full Design executed successfully.
   - Output Dock populated across 53 load combinations including footpath and median barrier loadings.
   - OpenCASCADE 3D CAD rendered asymmetric deck, median barrier, and internal cross bracings with 0 errors.

Screenshots and detailed verification notes are located in [`evidence/screenshots/live_gui_verification/`](file:///evidence/screenshots/live_gui_verification/).

---

## 7. Engineering Limitations & Boundaries

1. **Remediation Scope:** Exactly 5 of the 20 cataloged defects (Batches 1–3 + follow-up commit) are committed to source code. The remaining 15 defects are thoroughly documented in [`reports/SUBMISSION_TECHNICAL_REPORT.md`](file:///reports/SUBMISSION_TECHNICAL_REPORT.md) and [`submission/github_issues/`](file:///submission/github_issues/) with root-cause analyses, proposed diffs, and test fixtures.
2. **Moving Load Point Load Dropping:** Setting `allow_out_of_mesh=True` during vehicle traversal correctly assigns 0 grillage reaction to off-bridge vehicle axles. Direct manual point load calls retain default `allow_out_of_mesh=False` to fail-closed on misplaced inputs.
3. **Integration Testing Boundaries:** Full-pipeline coverage evaluates live-load conservation across three geometries and end-to-end design on the sample project. The design results are verified comparatively across code versions rather than an independent manual bridge calculation.
4. **Certification Disclaimer:** This work was performed as an evaluation submission for the FOSSEE Winter Internship 2026 screening task. It does not constitute professional certification of the entire OsdagBridge codebase, and does not claim that the entire application is defect-free.

---

## 8. Author & Evaluation Metadata

- **Author:** Subodh Shivmurti Bansode  
- **GitHub:** [@Subodh-17](https://github.com/Subodh-17)  
- **Repository:** [Subodh-17/OsdagBridge-Testing-Winter2026](https://github.com/Subodh-17/OsdagBridge-Testing-Winter2026) (Private)  
- **Host Institution:** FOSSEE, IIT Bombay  
- **Submission Date:** November 2026  
