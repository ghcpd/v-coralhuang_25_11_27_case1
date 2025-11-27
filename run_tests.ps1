# Run Tests Script for Windows PowerShell
# This script activates the virtual environment and runs pytest

Write-Host "=== Todo App with Tags - Test Runner (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual environment not found. Running setup..." -ForegroundColor Yellow
    Write-Host ""
    & .\setup_env.ps1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Setup failed. Please fix the errors and try again." -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "ERROR: Could not find activation script" -ForegroundColor Red
    Write-Host "Try running setup_env.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if pytest is installed
Write-Host "Checking pytest installation..." -ForegroundColor Yellow
try {
    $pytestCheck = python -m pytest --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "pytest not found. Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements-dev.txt --quiet
        Write-Host "Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "pytest is installed" -ForegroundColor Green
    }
} catch {
    Write-Host "Installing pytest..." -ForegroundColor Yellow
    pip install -r requirements-dev.txt --quiet
    Write-Host "Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Running Tests ===" -ForegroundColor Cyan
Write-Host ""

# Run pytest with various options based on arguments
$testArgs = $args

if ($testArgs.Count -eq 0) {
    # Default: run all tests with verbose output
    python -m pytest test_todo_with_tags.py -v
} else {
    # Pass through any arguments
    python -m pytest @testArgs
}

$testExitCode = $LASTEXITCODE

Write-Host ""

# Display results
if ($testExitCode -eq 0) {
    Write-Host "=== All Tests Passed ===" -ForegroundColor Green
} else {
    Write-Host "=== Some Tests Failed ===" -ForegroundColor Red
    Write-Host "Review the output above for details" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Additional test options:" -ForegroundColor Cyan
Write-Host "  .\run_tests.ps1 -k test_name    # Run specific test" -ForegroundColor White
Write-Host "  .\run_tests.ps1 --cov           # Run with coverage" -ForegroundColor White
Write-Host "  .\run_tests.ps1 -v -s           # Verbose with print output" -ForegroundColor White
Write-Host "  .\run_tests.ps1 --lf            # Run last failed tests" -ForegroundColor White
Write-Host ""

exit $testExitCode
