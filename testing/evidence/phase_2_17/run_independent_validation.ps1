<#
.SYNOPSIS
    Phase 2.17 Remediated Independent Native Windows Validation Package Runner
.DESCRIPTION
    Executes the Win32 Job Object containment validation suite and the 27-vector
    adversarial governance test suite natively on Windows outside AI agent orchestration.
    
    Hardened for Windows PowerShell 5.1 and PowerShell 7+:
    - Eliminates NativeCommandError exceptions on stderr by using OS-level process streaming.
    - Active Python interpreter identity enforcement: asserts Python 3.12.x and win32 platform (C3).
    - Prevents $null.Trim() exceptions when Git working tree is completely clean (C4(c)).
    - Enforced pre-flight and post-flight cryptographic and Git integrity gates.
    - Non-colliding, timestamped output run directories under phase_2_17 (C1).
    - Diagnostic failure manifest recorded on preflight failure (no empty directories) (C4(d)).
    - Transparent operator identity, execution mode, host environment, and parent process tracking (C4(b)).
    - Strict manifest generation verification: fails closed if manifest write fails or produces null (C4(a)).
    - Real-time console streaming via Out-Host with simultaneous file logging.
.EXAMPLE
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_independent_validation.ps1 -OperatorName "ExternalAuditor" -ExecutionMode "operator_execution"
#>

[CmdletBinding()]
param(
    [string]$WorkspaceRoot = "F:\FOSSEE internship",
    [string]$PythonExe = "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe",
    [string]$OutputDir = "",
    [string]$OperatorName = $env:USERNAME,
    [ValidateSet('agent_execution', 'operator_execution', 'auditor_execution')]
    [string]$ExecutionMode = "agent_execution"
)

$overallStopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$tOverallStartUtc = (Get-Date).ToUniversalTime().ToString("o")
$runGuid = [System.Guid]::NewGuid().ToString()
$shortRunId = $runGuid.Substring(0, 8)
$runTimestampStr = (Get-Date).ToUniversalTime().ToString("yyyyMMdd_HHmmss")

# Resolve parent process information
$parentPid = $null
$parentName = "UNKNOWN"
try {
    $procCim = Get-CimInstance Win32_Process -Filter "ProcessId = $PID" -ErrorAction SilentlyContinue
    if ($procCim) {
        $parentPid = $procCim.ParentProcessId
        $parentProc = Get-Process -Id $parentPid -ErrorAction SilentlyContinue
        if ($parentProc) { $parentName = $parentProc.Name }
    }
} catch {
    # Non-fatal diagnostic probe
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  PHASE 2.17 INDEPENDENT NATIVE WINDOWS VALIDATION EXECUTION RUNNER" -ForegroundColor Cyan
Write-Host "  Run ID:         $runGuid" -ForegroundColor Cyan
Write-Host "  Timestamp:      $tOverallStartUtc" -ForegroundColor Cyan
Write-Host "  Operator:       $OperatorName (Mode: $ExecutionMode)" -ForegroundColor Cyan
Write-Host "  Host / User:    $env:COMPUTERNAME / $env:USERNAME" -ForegroundColor Cyan
Write-Host "  Parent Process: $parentName (PID: $parentPid)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# 1. Workspace & Path Verification
# -----------------------------------------------------------------------------
if (-not (Test-Path -Path $WorkspaceRoot)) {
    Write-Host "[FATAL] Workspace root '$WorkspaceRoot' does not exist." -ForegroundColor Red
    exit 1
}
Set-Location -Path $WorkspaceRoot
Write-Host "`n[1/6] Workspace Directory: $WorkspaceRoot"

# -----------------------------------------------------------------------------
# 2. Output Directory Preparation (Collision Prevention & Unique Timestamping)
# -----------------------------------------------------------------------------
if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $baseOutputDir = Join-Path $WorkspaceRoot "testing\evidence\phase_2_17\windows\runs"
    $OutputDir = Join-Path $baseOutputDir "run_${runTimestampStr}_${shortRunId}"
}

if (Test-Path -Path $OutputDir) {
    Write-Host "[FATAL] Target output directory already exists: '$OutputDir'" -ForegroundColor Red
    Write-Host "        Overwriting prior independent evidence is strictly prohibited (C1)." -ForegroundColor Red
    exit 1
}

try {
    New-Item -ItemType Directory -Path $OutputDir -Force -ErrorAction Stop | Out-Null
    Write-Host "      Output Dir:  $OutputDir"
} catch {
    Write-Host "[FATAL] Failed to create output directory '$OutputDir': $_" -ForegroundColor Red
    exit 1
}

$containmentOut = Join-Path $OutputDir "windows_containment_validation.txt"
$containmentLog = Join-Path $OutputDir "windows_containment_validation.log"
$governanceOut  = Join-Path $OutputDir "governance_test_output.txt"
$governanceLog  = Join-Path $OutputDir "governance_test_output.log"
$summaryJson    = Join-Path $OutputDir "independent_run_manifest.json"

# Helper script block to record diagnostic failure manifest if pre-flight fails (C4(d))
$script:WritePreflightFailureRecord = {
    param([string[]]$Failures, [hashtable]$PartialEnv, [hashtable]$PreflightChecks)
    try {
        $failManifest = [ordered]@{
            manifest_schema_version = "2.17.0"
            run_id                  = $runGuid
            status                  = "PREFLIGHT_FAILURE"
            operator                = [ordered]@{
                operator_name       = $OperatorName
                execution_mode      = $ExecutionMode
                host_name           = $env:COMPUTERNAME
                user_profile        = $env:USERPROFILE
                parent_process_id   = $parentPid
                parent_process_name = $parentName
            }
            timestamp_utc           = $tOverallStartUtc
            failures                = $Failures
            environment             = $PartialEnv
            integrity_preflight     = $PreflightChecks
        }
        $failJson = ($failManifest | ConvertTo-Json -Depth 6)
        $failPath = Join-Path $OutputDir "preflight_failure_manifest.json"
        Set-Content -Path $failPath -Value $failJson -Encoding UTF8 -ErrorAction SilentlyContinue
        Write-Host "      Recorded preflight failure diagnostics to: $failPath" -ForegroundColor Yellow
    } catch {
        # Best effort diagnostic write
    }
}

# -----------------------------------------------------------------------------
# 3. Pinned Python Interpreter Identity Enforcement (C3 / P0.2)
# -----------------------------------------------------------------------------
Write-Host "`n[2/6] Pinned Python Interpreter Identity Enforcement (C3)..."
if (-not (Test-Path -Path $PythonExe -PathType Leaf)) {
    Write-Host "[FATAL] Pinned Python interpreter not found at: '$PythonExe'" -ForegroundColor Red
    Write-Host "        Silent PATH fallback is strictly prohibited by audit policy (P0.2)." -ForegroundColor Red
    Write-Host "        Configure the pinned 'osdagbridge-py312' conda environment." -ForegroundColor Red
    & $script:WritePreflightFailureRecord -Failures @("Pinned Python interpreter not found at '$PythonExe'") -PartialEnv @{ configured_path = $PythonExe } -PreflightChecks @{}
    exit 1
}

$pyProbeCmd = 'import sys, json, platform; print(json.dumps({\"major\": sys.version_info[0], \"minor\": sys.version_info[1], \"micro\": sys.version_info[2], \"version\": sys.version, \"platform\": sys.platform, \"executable\": sys.executable, \"machine\": platform.machine(), \"architecture\": platform.architecture()[0]}))'
$probeRaw = cmd.exe /c "`"$PythonExe`" -c `"$pyProbeCmd`" 2>nul"

if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($probeRaw)) {
    Write-Host "[FATAL] Failed to probe Python interpreter at: '$PythonExe'" -ForegroundColor Red
    & $script:WritePreflightFailureRecord -Failures @("Failed to probe Python interpreter at '$PythonExe'") -PartialEnv @{ configured_path = $PythonExe } -PreflightChecks @{}
    exit 1
}

$pyInfo = $null
try {
    $pyInfo = $probeRaw | ConvertFrom-Json
} catch {
    Write-Host "[FATAL] Failed to parse Python probe JSON output: $_" -ForegroundColor Red
    & $script:WritePreflightFailureRecord -Failures @("Failed to parse Python probe JSON output: $_") -PartialEnv @{ configured_path = $PythonExe; raw_probe = $probeRaw } -PreflightChecks @{}
    exit 1
}

$pyVersionMatch = ($pyInfo.major -eq 3 -and $pyInfo.minor -eq 12)
$pyPlatformMatch = ($pyInfo.platform -eq "win32")

Write-Host "      Configured Path: $PythonExe"
Write-Host "      Resolved Exe:    $($pyInfo.executable)"
Write-Host "      Python Version:  $($pyInfo.version) -> $(if ($pyVersionMatch) {'MATCH (3.12.x)'} else {'FAIL'})"
Write-Host "      Platform:        $($pyInfo.platform) (Arch: $($pyInfo.architecture)) -> $(if ($pyPlatformMatch) {'MATCH (win32)'} else {'FAIL'})"

if (-not $pyVersionMatch -or -not $pyPlatformMatch) {
    Write-Host "`n[FATAL] Python interpreter failed active identity enforcement (C3):" -ForegroundColor Red
    Write-Host "        Expected: Python 3.12 on win32 platform" -ForegroundColor Red
    Write-Host "        Detected: Python $($pyInfo.major).$($pyInfo.minor).$($pyInfo.micro) on $($pyInfo.platform)" -ForegroundColor Red
    & $script:WritePreflightFailureRecord -Failures @(
        "Python version mismatch: Expected 3.12.x, got $($pyInfo.major).$($pyInfo.minor).$($pyInfo.micro)",
        "Python platform mismatch: Expected win32, got $($pyInfo.platform)"
    ) -PartialEnv @{
        python_executable_configured = $PythonExe
        python_executable_resolved   = $pyInfo.executable
        python_version               = $pyInfo.version
        python_platform              = $pyInfo.platform
    } -PreflightChecks @{}
    exit 1
}

# -----------------------------------------------------------------------------
# 4. Pre-Flight Integrity Enforcement Gates (P0.3 / F-5.3)
# -----------------------------------------------------------------------------
Write-Host "`n[3/6] Pre-Run Host & Cryptographic Integrity Gates..."

$EXPECTED_BRANCH       = "dev"
$EXPECTED_HEAD         = "d74f56dd7f22925fb8148cabf5740ed8d1e39ff3"
$EXPECTED_DB_WEATHER   = "1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98"
$EXPECTED_DB_OSDAG     = "25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91"
$EXPECTED_TRUST_LEDGER = "5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1"

$preflightFailures = @()

# Git Branch
$actualBranchRaw = git -C "source/OsdagBridge" rev-parse --abbrev-ref HEAD
$actualBranch = if ($actualBranchRaw) { ($actualBranchRaw | Out-String).Trim() } else { "" }
$branchMatch = ($actualBranch -eq $EXPECTED_BRANCH)
if (-not $branchMatch) {
    $preflightFailures += "Git Branch mismatch: Expected '$EXPECTED_BRANCH', got '$actualBranch'"
}

# Git Commit HEAD
$actualHeadRaw = git -C "source/OsdagBridge" rev-parse HEAD
$actualHead = if ($actualHeadRaw) { ($actualHeadRaw | Out-String).Trim() } else { "" }
$headMatch = ($actualHead -eq $EXPECTED_HEAD)
if (-not $headMatch) {
    $preflightFailures += "Git HEAD mismatch: Expected '$EXPECTED_HEAD', got '$actualHead'"
}

# Git Clean Working Tree (C4(c) Fix: Safe extraction without $null.Trim())
$rawGitStatus = git -C "source/OsdagBridge" status --porcelain
$actualGitStatus = if ($rawGitStatus) { ($rawGitStatus | Out-String).Trim() } else { "" }
$cleanMatch = [string]::IsNullOrEmpty($actualGitStatus)
if (-not $cleanMatch) {
    $preflightFailures += "Git working tree is DIRTY: '$actualGitStatus'"
}

# Database: weather.sqlite
$weatherDbPath = "source/OsdagBridge/src/osdagbridge/core/data/project_location/weather.sqlite"
$actualDbWeather = (Get-FileHash $weatherDbPath -Algorithm SHA256).Hash.ToLower()
$weatherMatch = ($actualDbWeather -eq $EXPECTED_DB_WEATHER)
if (-not $weatherMatch) {
    $preflightFailures += "weather.sqlite hash mismatch: Expected '$EXPECTED_DB_WEATHER', got '$actualDbWeather'"
}

# Database: Intg_osdag.sqlite
$osdagDbPath = "source/OsdagBridge/src/osdagbridge/core/data/ResourceFiles/Intg_osdag.sqlite"
$actualDbOsdag = (Get-FileHash $osdagDbPath -Algorithm SHA256).Hash.ToLower()
$osdagMatch = ($actualDbOsdag -eq $EXPECTED_DB_OSDAG)
if (-not $osdagMatch) {
    $preflightFailures += "Intg_osdag.sqlite hash mismatch: Expected '$EXPECTED_DB_OSDAG', got '$actualDbOsdag'"
}

# Production Trust Store Ledger
$trustLedger = Join-Path $env:USERPROFILE ".osdagbridge_trust\trusted_run_seals.json"
if (-not (Test-Path $trustLedger)) {
    $preflightFailures += "Production trust ledger not found at: '$trustLedger'"
    $actualLedgerPre = "MISSING"
    $ledgerPreMatch = $false
} else {
    $actualLedgerPre = (Get-FileHash $trustLedger -Algorithm SHA256).Hash.ToLower()
    $ledgerPreMatch = ($actualLedgerPre -eq $EXPECTED_TRUST_LEDGER)
    if (-not $ledgerPreMatch) {
        $preflightFailures += "Production trust ledger hash mismatch: Expected '$EXPECTED_TRUST_LEDGER', got '$actualLedgerPre'"
    }
}

Write-Host "      Git Branch:          $actualBranch (Expected: $EXPECTED_BRANCH) -> $(if ($branchMatch) {'MATCH'} else {'FAIL'})"
Write-Host "      Git HEAD:            $actualHead (Expected: $EXPECTED_HEAD) -> $(if ($headMatch) {'MATCH'} else {'FAIL'})"
Write-Host "      Git Working Tree:    $(if ($cleanMatch) {'CLEAN (MATCH)'} else {'DIRTY (FAIL)'})"
Write-Host "      weather.sqlite:      $actualDbWeather -> $(if ($weatherMatch) {'MATCH'} else {'FAIL'})"
Write-Host "      Intg_osdag.sqlite:   $actualDbOsdag -> $(if ($osdagMatch) {'MATCH'} else {'FAIL'})"
Write-Host "      Trust Ledger Hash:   $actualLedgerPre -> $(if ($ledgerPreMatch) {'MATCH'} else {'FAIL'})"

$preflightChecksRecord = [ordered]@{
    git_branch          = $actualBranch
    git_branch_match    = $branchMatch
    git_head            = $actualHead
    git_head_match      = $headMatch
    git_clean           = $cleanMatch
    weather_db_sha256   = $actualDbWeather
    weather_db_match    = $weatherMatch
    intg_osdag_db_sha256 = $actualDbOsdag
    intg_osdag_db_match = $osdagMatch
    trust_ledger_sha256 = $actualLedgerPre
    trust_ledger_match  = $ledgerPreMatch
    all_preflight_passed = ($preflightFailures.Count -eq 0)
}

if ($preflightFailures.Count -gt 0) {
    Write-Host "`n[FATAL] Pre-Flight Integrity Gate FAILED with $($preflightFailures.Count) violation(s):" -ForegroundColor Red
    foreach ($err in $preflightFailures) {
        Write-Host "  - $err" -ForegroundColor Red
    }
    # Record diagnostic failure manifest so run folder is never an unexplained empty stub (C4(d))
    & $script:WritePreflightFailureRecord -Failures $preflightFailures -PartialEnv @{
        python_executable_configured = $PythonExe
        python_executable_resolved   = $pyInfo.executable
        python_version               = $pyInfo.version
        python_platform              = $pyInfo.platform
        workspace_root               = $WorkspaceRoot
        output_directory             = $OutputDir
    } -PreflightChecks $preflightChecksRecord
    Write-Host "`nAborting execution immediately before invoking test suites." -ForegroundColor Red
    exit 1
}
Write-Host "      Pre-Flight Gate:     PASSED (All baseline integrity criteria satisfied)" -ForegroundColor Green

# -----------------------------------------------------------------------------
# 5. Capture Harness Script Hashes
# -----------------------------------------------------------------------------
$harnessScriptHashes = @{
    validate_windows_containment_py = (Get-FileHash "testing/test_cases/baseline_regression/validate_windows_containment.py" -Algorithm SHA256).Hash.ToLower()
    test_evidence_governance_py    = (Get-FileHash "testing/test_cases/baseline_regression/test_evidence_governance.py" -Algorithm SHA256).Hash.ToLower()
    evidence_guard_py              = (Get-FileHash "testing/test_cases/baseline_regression/evidence_guard.py" -Algorithm SHA256).Hash.ToLower()
    run_independent_validation_ps1 = (Get-FileHash $MyInvocation.MyCommand.Path -Algorithm SHA256).Hash.ToLower()
}

# -----------------------------------------------------------------------------
# 6. Execution Helper: Safe OS-Level Native Invocation (P0.1 / F-5.1)
# -----------------------------------------------------------------------------
# Invoking through cmd.exe /c "python ... 2>&1" merges stdout/stderr at the OS
# C-runtime boundary. This prevents Windows PowerShell 5.1 from converting
# stderr streams into NativeCommandError.
# Piping to Out-Host streams live output directly to the console host while
# Tee-Object simultaneously records the full output to disk, without polluting
# the function's return pipeline.
function Invoke-SafePythonSuite {
    param(
        [string]$ScriptPath,
        [string[]]$Arguments,
        [string]$OutputFile
    )
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $tSuiteStartUtc = (Get-Date).ToUniversalTime().ToString("o")

    $argStr = ($Arguments -join " ")
    $cmdLine = "`"$PythonExe`" -u `"$ScriptPath`" $argStr"

    # Execute via cmd.exe redirection to guarantee PS 5.1 compatibility
    # Out-Host ensures real-time console streaming without capturing output into return value
    cmd.exe /c "$cmdLine 2>&1" | Tee-Object -FilePath $OutputFile | Out-Host
    $exitCode = $LASTEXITCODE

    $sw.Stop()
    $tSuiteEndUtc = (Get-Date).ToUniversalTime().ToString("o")

    return @{
        ExitCode   = $exitCode
        DurationS  = $sw.Elapsed.TotalSeconds
        StartUtc   = $tSuiteStartUtc
        EndUtc     = $tSuiteEndUtc
    }
}

# -----------------------------------------------------------------------------
# 7. Execute Suite 1: Win32 Job Object Containment Validation
# -----------------------------------------------------------------------------
Write-Host "`n[4/6] Executing Win32 Job Object Containment Suite..." -ForegroundColor Yellow
$containmentRes = Invoke-SafePythonSuite -ScriptPath "testing/test_cases/baseline_regression/validate_windows_containment.py" -Arguments @() -OutputFile $containmentOut
Copy-Item -Path $containmentOut -Destination $containmentLog -Force

$containmentPassed = ($containmentRes.ExitCode -eq 0)
Write-Host "      Containment Exit Code: $($containmentRes.ExitCode) (Duration: $($containmentRes.DurationS.ToString('F2'))s)" -ForegroundColor $(if ($containmentPassed) { 'Green' } else { 'Red' })

# -----------------------------------------------------------------------------
# 8. Execute Suite 2: Adversarial Evidence Governance Suite (27 Vectors)
# -----------------------------------------------------------------------------
Write-Host "`n[5/6] Executing Adversarial Evidence Governance Suite (27 Vectors)..." -ForegroundColor Yellow
$governanceRes = Invoke-SafePythonSuite -ScriptPath "testing/test_cases/baseline_regression/test_evidence_governance.py" -Arguments @("-v") -OutputFile $governanceOut
Copy-Item -Path $governanceOut -Destination $governanceLog -Force

$governancePassed = ($governanceRes.ExitCode -eq 0)
Write-Host "      Governance Exit Code:  $($governanceRes.ExitCode) (Duration: $($governanceRes.DurationS.ToString('F2'))s)" -ForegroundColor $(if ($governancePassed) { 'Green' } else { 'Red' })

# -----------------------------------------------------------------------------
# 9. Post-Flight Integrity Enforcement Gates (P0.4 / F-5.4)
# -----------------------------------------------------------------------------
Write-Host "`n[6/6] Post-Run Integrity Gates & Ledger Isolation..."

$postflightFailures = @()

# Re-check Git Branch
$actualBranchPostRaw = git -C "source/OsdagBridge" rev-parse --abbrev-ref HEAD
$actualBranchPost = if ($actualBranchPostRaw) { ($actualBranchPostRaw | Out-String).Trim() } else { "" }
$branchPostMatch = ($actualBranchPost -eq $actualBranch -and $actualBranchPost -eq $EXPECTED_BRANCH)
if (-not $branchPostMatch) {
    $postflightFailures += "Git Branch changed post-run: Expected '$actualBranch', got '$actualBranchPost'"
}

# Re-check Git HEAD
$actualHeadPostRaw = git -C "source/OsdagBridge" rev-parse HEAD
$actualHeadPost = if ($actualHeadPostRaw) { ($actualHeadPostRaw | Out-String).Trim() } else { "" }
$headPostMatch = ($actualHeadPost -eq $actualHead -and $actualHeadPost -eq $EXPECTED_HEAD)
if (-not $headPostMatch) {
    $postflightFailures += "Git HEAD changed post-run: Expected '$actualHead', got '$actualHeadPost'"
}

# Re-check Git Status (C4(c) Fix: Safe extraction without $null.Trim())
$rawGitStatusPost = git -C "source/OsdagBridge" status --porcelain
$actualGitStatusPost = if ($rawGitStatusPost) { ($rawGitStatusPost | Out-String).Trim() } else { "" }
$cleanPostMatch = [string]::IsNullOrEmpty($actualGitStatusPost)
if (-not $cleanPostMatch) {
    $postflightFailures += "Git working tree became DIRTY post-run: '$actualGitStatusPost'"
}

# Re-check Database: weather.sqlite
$actualDbWeatherPost = (Get-FileHash $weatherDbPath -Algorithm SHA256).Hash.ToLower()
$weatherPostMatch = ($actualDbWeatherPost -eq $actualDbWeather -and $actualDbWeatherPost -eq $EXPECTED_DB_WEATHER)
if (-not $weatherPostMatch) {
    $postflightFailures += "weather.sqlite hash changed post-run: Expected '$actualDbWeather', got '$actualDbWeatherPost'"
}

# Re-check Database: Intg_osdag.sqlite
$actualDbOsdagPost = (Get-FileHash $osdagDbPath -Algorithm SHA256).Hash.ToLower()
$osdagPostMatch = ($actualDbOsdagPost -eq $actualDbOsdag -and $actualDbOsdagPost -eq $EXPECTED_DB_OSDAG)
if (-not $osdagPostMatch) {
    $postflightFailures += "Intg_osdag.sqlite hash changed post-run: Expected '$actualDbOsdag', got '$actualDbOsdagPost'"
}

# Re-check Production Trust Ledger
$actualLedgerPost = (Get-FileHash $trustLedger -Algorithm SHA256).Hash.ToLower()
$ledgerPostMatch = ($actualLedgerPost -eq $actualLedgerPre -and $actualLedgerPost -eq $EXPECTED_TRUST_LEDGER)
if (-not $ledgerPostMatch) {
    $postflightFailures += "Production trust ledger modified post-run: Expected '$actualLedgerPre', got '$actualLedgerPost'"
}

Write-Host "      Git Branch Post:     $actualBranchPost -> $(if ($branchPostMatch) {'UNCHANGED'} else {'CHANGED'})"
Write-Host "      Git HEAD Post:       $actualHeadPost -> $(if ($headPostMatch) {'UNCHANGED'} else {'CHANGED'})"
Write-Host "      Git Clean Post:      $(if ($cleanPostMatch) {'CLEAN (MATCH)'} else {'DIRTY (FAIL)'})"
Write-Host "      weather.sqlite Post: $actualDbWeatherPost -> $(if ($weatherPostMatch) {'UNCHANGED'} else {'CHANGED'})"
Write-Host "      Intg_osdag Post:     $actualDbOsdagPost -> $(if ($osdagPostMatch) {'UNCHANGED'} else {'CHANGED'})"
Write-Host "      Trust Ledger Post:   $actualLedgerPost -> $(if ($ledgerPostMatch) {'UNCHANGED'} else {'CHANGED'})"

$postflightPassed = ($postflightFailures.Count -eq 0)
if (-not $postflightPassed) {
    Write-Host "`n[FATAL] Post-Flight Integrity Gate FAILED with $($postflightFailures.Count) violation(s):" -ForegroundColor Red
    foreach ($err in $postflightFailures) {
        Write-Host "  - $err" -ForegroundColor Red
    }
} else {
    Write-Host "      Post-Flight Gate:    PASSED (All isolation & immutability gates satisfied)" -ForegroundColor Green
}

# -----------------------------------------------------------------------------
# 10. Generate Complete Execution Manifest (P0.6 / F-5.6 / C4(a) / C4(b))
# -----------------------------------------------------------------------------
$overallStopwatch.Stop()
$tOverallEndUtc = (Get-Date).ToUniversalTime().ToString("o")

$testSuitesPassed = ($containmentPassed -and $governancePassed)
$integrityGatesPassed = ($preflightFailures.Count -eq 0 -and $postflightPassed)
$overallPassed = ($testSuitesPassed -and $integrityGatesPassed)

$manifest = [ordered]@{
    manifest_schema_version = "2.17.0"
    run_id                  = $runGuid
    operator                = [ordered]@{
        operator_name       = $OperatorName
        execution_mode      = $ExecutionMode
        host_name           = $env:COMPUTERNAME
        user_profile        = $env:USERPROFILE
        parent_process_id   = $parentPid
        parent_process_name = $parentName
    }
    overall_status          = if ($overallPassed) { "PASS" } else { "FAIL" }
    test_suites_status      = if ($testSuitesPassed) { "PASS" } else { "FAIL" }
    integrity_gates_status  = if ($integrityGatesPassed) { "PASS" } else { "FAIL" }
    timing                  = [ordered]@{
        overall_start_utc   = $tOverallStartUtc
        overall_end_utc     = $tOverallEndUtc
        overall_duration_s  = [math]::Round($overallStopwatch.Elapsed.TotalSeconds, 3)
        containment_suite   = [ordered]@{
            start_utc       = $containmentRes.StartUtc
            end_utc         = $containmentRes.EndUtc
            duration_s      = [math]::Round($containmentRes.DurationS, 3)
            exit_code       = $containmentRes.ExitCode
            passed          = $containmentPassed
        }
        governance_suite    = [ordered]@{
            start_utc       = $governanceRes.StartUtc
            end_utc         = $governanceRes.EndUtc
            duration_s      = [math]::Round($governanceRes.DurationS, 3)
            exit_code       = $governanceRes.ExitCode
            passed          = $governancePassed
        }
    }
    environment             = [ordered]@{
        platform                      = "win32"
        os_caption                    = (Get-CimInstance Win32_OperatingSystem).Caption
        os_version                    = (Get-CimInstance Win32_OperatingSystem).Version
        os_build                      = (Get-CimInstance Win32_OperatingSystem).BuildNumber
        powershell_edition            = $PSVersionTable.PSEdition
        powershell_version            = $PSVersionTable.PSVersion.ToString()
        python_executable_configured  = $PythonExe
        python_executable_resolved    = $pyInfo.executable
        python_version                = $pyInfo.version
        python_platform               = $pyInfo.platform
        python_architecture           = $pyInfo.architecture
        python_machine                = $pyInfo.machine
        python_version_enforced       = $pyVersionMatch
        python_platform_enforced      = $pyPlatformMatch
        workspace_root                = $WorkspaceRoot
        output_directory              = $OutputDir
    }
    harness_script_hashes   = $harnessScriptHashes
    integrity_preflight     = [ordered]@{
        git_branch          = $actualBranch
        git_branch_match    = $branchMatch
        git_head            = $actualHead
        git_head_match      = $headMatch
        git_clean           = $cleanMatch
        weather_db_sha256   = $actualDbWeather
        weather_db_match    = $weatherMatch
        intg_osdag_db_sha256 = $actualDbOsdag
        intg_osdag_db_match = $osdagMatch
        trust_ledger_sha256 = $actualLedgerPre
        trust_ledger_match  = $ledgerPreMatch
        all_preflight_passed = ($preflightFailures.Count -eq 0)
    }
    integrity_postflight    = [ordered]@{
        git_branch          = $actualBranchPost
        git_branch_match    = $branchPostMatch
        git_head            = $actualHeadPost
        git_head_match      = $headPostMatch
        git_clean           = $cleanPostMatch
        weather_db_sha256   = $actualDbWeatherPost
        weather_db_match    = $weatherPostMatch
        intg_osdag_db_sha256 = $actualDbOsdagPost
        intg_osdag_db_match = $osdagPostMatch
        trust_ledger_sha256 = $actualLedgerPost
        trust_ledger_match  = $ledgerPostMatch
        ledger_unchanged    = ($actualLedgerPre -eq $actualLedgerPost)
        databases_unchanged = ($actualDbWeather -eq $actualDbWeatherPost -and $actualDbOsdag -eq $actualDbOsdagPost)
        git_unchanged       = ($actualHead -eq $actualHeadPost -and $actualBranch -eq $actualBranchPost)
        all_postflight_passed = $postflightPassed
    }
    artifacts               = [ordered]@{
        containment_validation_txt = [ordered]@{
            path            = $containmentOut
            sha256          = (Get-FileHash $containmentOut -Algorithm SHA256).Hash.ToLower()
            bytes           = (Get-Item $containmentOut).Length
        }
        containment_validation_log = [ordered]@{
            path            = $containmentLog
            sha256          = (Get-FileHash $containmentLog -Algorithm SHA256).Hash.ToLower()
            bytes           = (Get-Item $containmentLog).Length
        }
        governance_output_txt      = [ordered]@{
            path            = $governanceOut
            sha256          = (Get-FileHash $governanceOut -Algorithm SHA256).Hash.ToLower()
            bytes           = (Get-Item $governanceOut).Length
        }
        governance_output_log      = [ordered]@{
            path            = $governanceLog
            sha256          = (Get-FileHash $governanceLog -Algorithm SHA256).Hash.ToLower()
            bytes           = (Get-Item $governanceLog).Length
        }
    }
}

try {
    $manifestJsonText = ($manifest | ConvertTo-Json -Depth 8)
    if ([string]::IsNullOrWhiteSpace($manifestJsonText) -or $manifestJsonText -eq "null") {
        throw "Manifest serialized to null or whitespace"
    }
    Set-Content -Path $summaryJson -Value $manifestJsonText -Encoding UTF8 -ErrorAction Stop

    # Active verification of the written manifest (C4(a))
    if (-not (Test-Path -Path $summaryJson)) {
        throw "Manifest file was not created on disk: '$summaryJson'"
    }
    $manifestItem = Get-Item -Path $summaryJson
    if ($manifestItem.Length -le 0) {
        throw "Manifest file on disk is 0 bytes: '$summaryJson'"
    }
    $parsedBack = Get-Content -Path $summaryJson -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $parsedBack -or [string]::IsNullOrWhiteSpace($parsedBack.overall_status)) {
        throw "Manifest file failed to parse back or overall_status is missing/null"
    }
    Write-Host "`nSaved and verified execution manifest: $summaryJson" -ForegroundColor Cyan
} catch {
    Write-Host "`n[FATAL] Manifest generation / verification failed (C4(a)): $_" -ForegroundColor Red
    $failNote = Join-Path $OutputDir "MANIFEST_WRITE_FAILURE.txt"
    Set-Content -Path $failNote -Value "MANIFEST_WRITE_FAILURE: $_" -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  INDEPENDENT EXECUTION SUMMARY" -ForegroundColor Cyan
Write-Host "  Overall Status:         $(if ($overallPassed) {'PASS'} else {'FAIL'})" -ForegroundColor $(if ($overallPassed) {'Green'} else {'Red'})
Write-Host "  Test Suites Status:     $(if ($testSuitesPassed) {'PASS'} else {'FAIL'})" -ForegroundColor $(if ($testSuitesPassed) {'Green'} else {'Red'})
Write-Host "  Integrity Gates Status: $(if ($integrityGatesPassed) {'PASS'} else {'FAIL'})" -ForegroundColor $(if ($integrityGatesPassed) {'Green'} else {'Red'})
Write-Host "  Output Directory:       $OutputDir"
Write-Host "================================================================================" -ForegroundColor Cyan

if (-not $overallPassed) {
    exit 1
}
exit 0
