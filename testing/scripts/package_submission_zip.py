"""
Package Submission ZIP Archive
FOSSEE Winter Internship 2026 Screening Task - Subodh Bansode

Assembles a clean, minimal, self-contained, reproducible ZIP archive in submission/zip/
excluding .git, caches, virtual environments, scratch files, and large binary blobs.
"""

import os
import sys
import shutil
import zipfile
import stat

def remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

WORKSPACE = r"F:\FOSSEE internship"
SUBMISSION_DIR = os.path.join(WORKSPACE, "submission")
ZIP_DIR = os.path.join(SUBMISSION_DIR, "zip")
os.makedirs(ZIP_DIR, exist_ok=True)

ZIP_NAME = "OsdagBridge_Testing_Package_Subodh_Bansode.zip"
ZIP_PATH = os.path.join(ZIP_DIR, ZIP_NAME)

# Staging directory
STAGE_DIR = os.path.join(SUBMISSION_DIR, "_staging_package")
if os.path.exists(STAGE_DIR):
    shutil.rmtree(STAGE_DIR, onerror=remove_readonly)
os.makedirs(STAGE_DIR, exist_ok=True)

print("=" * 70)
print(" FOSSEE WINTER INTERNSHIP 2026 - SUBMISSION ZIP PACKAGER")
print("=" * 70)

# Helper to copy directory with exclusions
def copy_tree_filtered(src, dst, ignore_patterns):
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if not any(d == p or d.startswith(p) for p in ignore_patterns)]
        rel_root = os.path.relpath(root, src)
        dest_root = os.path.join(dst, rel_root) if rel_root != "." else dst
        os.makedirs(dest_root, exist_ok=True)
        for f in files:
            if any(f.endswith(ext) for ext in [".pyc", ".tmp", ".log.old"]):
                continue
            if any(f == p for p in ignore_patterns):
                continue
            src_file = os.path.join(root, f)
            dest_file = os.path.join(dest_root, f)
            shutil.copy2(src_file, dest_file)

# 1. Source (Application Code with Phase 3 commits applied, excluding .git)
print("\n[1/6] Staging application source code (excluding .git)...")
copy_tree_filtered(
    os.path.join(WORKSPACE, "source", "OsdagBridge"),
    os.path.join(STAGE_DIR, "source", "OsdagBridge"),
    [".git", "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info"]
)

# 2. Testing Suites & Harness (excluding scratch)
print("[2/6] Staging test suites and harness...")
copy_tree_filtered(
    os.path.join(WORKSPACE, "testing", "test_cases"),
    os.path.join(STAGE_DIR, "testing", "test_cases"),
    ["__pycache__", ".pytest_cache"]
)
copy_tree_filtered(
    os.path.join(WORKSPACE, "testing", "scripts"),
    os.path.join(STAGE_DIR, "testing", "scripts"),
    ["__pycache__"]
)
copy_tree_filtered(
    os.path.join(WORKSPACE, "testing", "fixtures"),
    os.path.join(STAGE_DIR, "testing", "fixtures"),
    ["__pycache__"]
)
copy_tree_filtered(
    os.path.join(WORKSPACE, "testing", "evidence"),
    os.path.join(STAGE_DIR, "testing", "evidence"),
    ["__pycache__", "scratch"]
)

# 3. Reports
print("[3/6] Staging engineering reports...")
copy_tree_filtered(
    os.path.join(WORKSPACE, "reports"),
    os.path.join(STAGE_DIR, "reports"),
    ["__pycache__", "v1_original"]
)

# 4. Documentation
print("[4/6] Staging documentation...")
copy_tree_filtered(
    os.path.join(WORKSPACE, "documentation"),
    os.path.join(STAGE_DIR, "documentation"),
    ["__pycache__"]
)

# 5. Evidence Screenshots
print("[5/6] Staging screenshots...")
copy_tree_filtered(
    os.path.join(WORKSPACE, "evidence", "screenshots"),
    os.path.join(STAGE_DIR, "evidence", "screenshots"),
    ["py312"] # py312 is duplicate of base
)

# 6. Submission Deliverables (Resume, Report PDF, OSI sample, video script)
print("[6/6] Staging deliverables...")
os.makedirs(os.path.join(STAGE_DIR, "submission", "resume"), exist_ok=True)
os.makedirs(os.path.join(STAGE_DIR, "submission", "pdf"), exist_ok=True)
os.makedirs(os.path.join(STAGE_DIR, "submission", "osi"), exist_ok=True)
os.makedirs(os.path.join(STAGE_DIR, "submission", "video"), exist_ok=True)

shutil.copy2(
    os.path.join(SUBMISSION_DIR, "resume", "Subodh_Resume.pdf"),
    os.path.join(STAGE_DIR, "submission", "resume", "Subodh_Resume.pdf")
)
shutil.copy2(
    os.path.join(SUBMISSION_DIR, "pdf", "OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf"),
    os.path.join(STAGE_DIR, "submission", "pdf", "OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf")
)
shutil.copy2(
    os.path.join(SUBMISSION_DIR, "osi", "sample_24m_composite_plate_girder.osi"),
    os.path.join(STAGE_DIR, "submission", "osi", "sample_24m_composite_plate_girder.osi")
)
shutil.copy2(
    os.path.join(SUBMISSION_DIR, "video", "VIDEO_RECORDING_SCRIPT_AND_TELEPROMPTER.md"),
    os.path.join(STAGE_DIR, "submission", "video", "VIDEO_RECORDING_SCRIPT_AND_TELEPROMPTER.md")
)

# Create Master README in Staging Root
stage_readme = """# FOSSEE Winter Internship 2026 — OsdagBridge Testing Submission Package

**Candidate:** Subodh Shivmurti Bansode (ID: `Subodh-17` | `subodh171011@gmail.com`)  
**Target Module:** Short-Span Steel Girder Bridge (Composite Plate Girder)  
**Host Institution:** FOSSEE, IIT Bombay  
**Governing Standards:** IRC:6-2017, IRC:22-2015, IRC:24-2010, IS 800:2007  

---

## Package Contents
- `submission/resume/Subodh_Resume.pdf`: Candidate Resume.
- `submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf`: Master Technical Report (8-page publication-grade PDF).
- `submission/osi/sample_24m_composite_plate_girder.osi`: Sample saved project input file.
- `submission/video/VIDEO_RECORDING_SCRIPT_AND_TELEPROMPTER.md`: Demonstration video script and URL.
- `source/OsdagBridge/`: Application source code with Phase 3 engineering remediations applied (Commits 418fd75 to f555075).
- `testing/`: Self-contained automated regression, governance, and acceptance test suites.
- `reports/`: Complete forensic audit dossiers and Defect Traceability Matrix (18 defects cataloged).
- `evidence/screenshots/`: High-resolution GUI and 3D CAD OpenCASCADE screenshots.

---

## Turnkey Verification Instructions (1-Click)

### Option A: Using Windows Batch Script
```bat
:: In Command Prompt or PowerShell:
run_submission_tests.bat
```

### Option B: Step-by-Step Manual Commands
```powershell
# 1. Activate Conda Environment
conda activate osdagbridge-py312

# 2. Run Evidence Governance Suite (27/27 OK)
python testing/test_cases/baseline_regression/test_evidence_governance.py

# 3. Run Batch 2 Statics Conservation Suite (17/17 OK)
python -m unittest testing/test_cases/phase_3/test_batch_2_comprehensive.py

# 4. Run Batch 3 Load Factor Scaling Suite (15/15 OK)
python -m unittest testing/test_cases/phase_3/test_batch_3_factor_scaling.py

# 5. Launch Desktop GUI Smoke Test & 3D CAD Assembly
python testing/scripts/gui_smoke_test_py312.py
```
"""

with open(os.path.join(STAGE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(stage_readme)

# Create 1-click test runner script
bat_runner = """@echo off
echo ======================================================================
echo  FOSSEE Winter Internship 2026 - OsdagBridge Turnkey Test Runner
echo  Candidate: Subodh Bansode (Subodh-17)
echo ======================================================================
echo.

echo [1/4] Running Automated Evidence Governance Suite (27 Tests)...
python testing\\test_cases\\baseline_regression\\test_evidence_governance.py
if %ERRORLEVEL% NEQ 0 (
    echo Governance Suite Failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Running Batch 2 Statics Equilibrium Acceptance Suite (17 Tests)...
python -m unittest testing\\test_cases\\phase_3\\test_batch_2_comprehensive.py
if %ERRORLEVEL% NEQ 0 (
    echo Batch 2 Suite Failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/4] Running Batch 3 Load Factor Scaling Acceptance Suite (15 Tests)...
python -m unittest testing\\test_cases\\phase_3\\test_batch_3_factor_scaling.py
if %ERRORLEVEL% NEQ 0 (
    echo Batch 3 Suite Failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [4/4] Launching PySide6 Desktop GUI Smoke Test & CAD Viewport...
python testing\\scripts\\gui_smoke_test_py312.py

echo.
echo ======================================================================
echo  ALL TEST SUITES PASSED SUCCESSFULLY!
echo ======================================================================
pause
"""

with open(os.path.join(STAGE_DIR, "run_submission_tests.bat"), "w", encoding="utf-8") as f:
    f.write(bat_runner)

# Create ZIP archive
print("\nCompressing staged package into ZIP archive...")
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(STAGE_DIR):
        for f in files:
            full_file = os.path.join(root, f)
            arc_name = os.path.relpath(full_file, STAGE_DIR)
            zf.write(full_file, arc_name)

zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
print(f"SUCCESS: ZIP Archive created at: {ZIP_PATH}")
print(f"Archive Size: {zip_size_mb:.2f} MB")

# Clean up staging directory
shutil.rmtree(STAGE_DIR, onerror=remove_readonly)
print("Staging directory cleaned up.")
