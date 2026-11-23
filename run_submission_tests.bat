@echo off
cd /d "%~dp0"
echo ======================================================================
echo  OsdagBridge screening task - verification suites
echo  Candidate: Subodh Bansode (GitHub: Subodh-17)
echo ======================================================================

echo.
echo [1/5] Evidence governance suite (expect 27/27 OK on Windows)...
python testing\test_cases\baseline_regression\test_evidence_governance.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo [2/5] Batch 2 - FE load conservation suites (expect 33 tests OK: 17 + 11 + 5)...
python -m unittest testing\test_cases\phase_3\test_batch_2_comprehensive.py testing\test_cases\phase_3\test_batch_2_line_loads.py testing\test_cases\phase_3\test_batch_2_patch_loads.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo [3/5] Batch 3 - load factor scaling suite (expect 15/15 OK)...
python -m unittest testing\test_cases\phase_3\test_batch_3_factor_scaling.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo [4/5] Moving-load mesh mapping suite (expect 10/10 OK)...
python -m unittest testing\test_cases\phase_3\test_moving_load_mesh_mapping.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
python -c "import PySide6, osdag_core" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [5/5] Full-pipeline suite SKIPPED: needs the conda environment ^(PySide6 + osdag^). See README.
    goto :done
)
echo [5/5] Full-pipeline live-load conservation (expect 3/3 OK; needs the conda environment)...
python -m unittest testing\test_cases\phase_3\test_full_pipeline_live_load_conservation.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
:done
echo ======================================================================
echo  All suites that could run passed.
echo ======================================================================
pause
exit /b 0

:fail
echo.
echo  A suite reported a failure - see the output above.
pause
exit /b 1
