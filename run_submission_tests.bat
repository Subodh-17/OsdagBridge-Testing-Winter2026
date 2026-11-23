@echo off
cd /d "%~dp0"
echo ======================================================================
echo  OsdagBridge screening task - verification suites
echo  Candidate: Subodh Bansode (GitHub: Subodh-17)
echo ======================================================================

echo.
echo [1/4] Evidence governance suite (expect 27/27 OK on Windows)...
python testing\test_cases\baseline_regression\test_evidence_governance.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo [2/4] Batch 2 - FE load conservation suite (expect 17/17 OK)...
python -m unittest testing\test_cases\phase_3\test_batch_2_comprehensive.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo [3/4] Batch 3 - load factor scaling suite (expect 15/15 OK)...
python -m unittest testing\test_cases\phase_3\test_batch_3_factor_scaling.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo [4/4] Moving-load mesh mapping suite (expect 10/10 OK)...
python -m unittest testing\test_cases\phase_3\test_moving_load_mesh_mapping.py
if %ERRORLEVEL% NEQ 0 goto :fail

echo.
echo ======================================================================
echo  All four suites passed.
echo ======================================================================
pause
exit /b 0

:fail
echo.
echo  A suite reported a failure - see the output above.
pause
exit /b 1
