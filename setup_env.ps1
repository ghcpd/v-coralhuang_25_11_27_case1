# Todo Application - Setup Environment Script (Windows)
# This script sets up the Python virtual environment and installs dependencies
# Usage: .\setup_env.ps1

param(
    [switch]$Force = $false
)

Write-Host "=== Todo Application - Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Get Python version
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Parse version (e.g., "Python 3.8.0" -> 3.8)
if ($pythonVersion -match "Python (\d+)\.(\d+)") {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "ERROR: Python 3.8 or higher is required. Found: $major.$minor" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ERROR: Could not parse Python version" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python version check passed" -ForegroundColor Green
Write-Host ""

# Check if venv exists
$venvPath = "venv"
if ((Test-Path $venvPath) -and -not $Force) {
    Write-Host "Virtual environment already exists" -ForegroundColor Cyan
} else {
    if ($Force -and (Test-Path $venvPath)) {
        Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $venvPath | Out-Null
    }
    
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = ".\$venvPath\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "ERROR: Could not find activation script" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to upgrade pip, continuing..." -ForegroundColor Yellow
}
Write-Host "✓ pip updated" -ForegroundColor Green
Write-Host ""

# Install requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing runtime dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Some runtime dependencies failed to install" -ForegroundColor Yellow
    } else {
        Write-Host "✓ Runtime dependencies installed" -ForegroundColor Green
    }
} else {
    Write-Host "No runtime dependencies to install" -ForegroundColor Cyan
}

Write-Host ""

# Install dev requirements
if (Test-Path "requirements-dev.txt") {
    Write-Host "Installing development dependencies (pytest)..." -ForegroundColor Yellow
    pip install -r requirements-dev.txt --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install development dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Development dependencies installed" -ForegroundColor Green
} else {
    Write-Host "No development dependencies to install" -ForegroundColor Cyan
}

Write-Host ""

# Verify installation
Write-Host "Verifying installations..." -ForegroundColor Yellow
python -c "import sys; print(f'Python: {sys.version.split()[0]}')" 2>$null
$pythonOk = $LASTEXITCODE -eq 0

python -c "import pytest; print(f'pytest: {pytest.__version__}')" 2>$null
$pytestOk = $LASTEXITCODE -eq 0

if ($pythonOk) {
    Write-Host "✓ Python verified" -ForegroundColor Green
} else {
    Write-Host "ERROR: Python verification failed" -ForegroundColor Red
    exit 1
}

if ($pytestOk) {
    Write-Host "✓ pytest verified" -ForegroundColor Green
} else {
    Write-Host "ERROR: pytest verification failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. To run tests: .\run_tests.ps1" -ForegroundColor White
Write-Host "2. To run application: python todo_with_tags.py" -ForegroundColor White
Write-Host "3. To activate venv manually: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
