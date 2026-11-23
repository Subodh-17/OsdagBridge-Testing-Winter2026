@echo off
REM ============================================================================
REM Phase 2.16 Independent Native Windows Validation Package Batch Launcher
REM ============================================================================
cd /d "F:\FOSSEE internship"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "testing\evidence\phase_2_15\run_independent_validation.ps1" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Validation suite reported failures. Exit code: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
echo.
echo [SUCCESS] Validation suite completed successfully.
exit /b 0
