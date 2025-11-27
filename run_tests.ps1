# Todo Application - Test Runner Script (Windows)
# This script runs the test suite using pytest
# Usage: .\run_tests.ps1 [args]

param(
    [string]$TestFile = "",
    [switch]$Verbose = $false,
    [switch]$Coverage = $false,
    [string[]]$AdditionalArgs = @()
)

Write-Host "=== Todo Application - Test Suite ===" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual environment not found. Running setup..." -ForegroundColor Yellow
    Write-Host ""
    & ".\setup_env.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Setup failed" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Activate virtual environment
$activateScript = ".\$venvPath\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "ERROR: Could not find activation script" -ForegroundColor Red
    exit 1
}

# Build pytest command
$pytestCmd = @("pytest")

if ($TestFile) {
    $pytestCmd += $TestFile
} else {
    $pytestCmd += "test_todo_with_tags.py"
}

if ($Verbose) {
    $pytestCmd += "-vv"
} else {
    $pytestCmd += "-v"
}

if ($Coverage) {
    $pytestCmd += @("--cov=.", "--cov-report=html", "--cov-report=term")
}

# Add any additional arguments
if ($AdditionalArgs) {
    $pytestCmd += $AdditionalArgs
}

Write-Host "Running tests..." -ForegroundColor Yellow
Write-Host "Command: $($pytestCmd -join ' ')" -ForegroundColor Gray
Write-Host ""

# Run tests
& python -m $pytestCmd

$testExitCode = $LASTEXITCODE

Write-Host ""
if ($testExitCode -eq 0) {
    Write-Host "=== All Tests Passed ===" -ForegroundColor Green
} else {
    Write-Host "=== Some Tests Failed ===" -ForegroundColor Red
}

Write-Host ""

if ($Coverage) {
    Write-Host "Coverage report generated in htmlcov/index.html" -ForegroundColor Cyan
}

exit $testExitCode
