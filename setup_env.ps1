# Setup Environment Script for Windows PowerShell
# This script sets up a Python virtual environment and installs dependencies

Write-Host "=== Todo App with Tags - Environment Setup (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number and check if >= 3.8
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if (($major -eq 3 -and $minor -lt 8) -or $major -lt 3) {
            Write-Host "ERROR: Python 3.8 or higher is required" -ForegroundColor Red
            Write-Host "Current version: $major.$minor" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Create virtual environment
$venvPath = "venv"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists at '$venvPath'" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $venvPath
        Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
        python -m venv $venvPath
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "Using existing virtual environment" -ForegroundColor Green
    }
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "ERROR: Could not find activation script" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "pip upgraded successfully" -ForegroundColor Green

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow

if (Test-Path "requirements.txt") {
    Write-Host "Installing production dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    Write-Host "Production dependencies installed" -ForegroundColor Green
}

if (Test-Path "requirements-dev.txt") {
    Write-Host "Installing development dependencies from requirements-dev.txt..." -ForegroundColor Yellow
    pip install -r requirements-dev.txt --quiet
    Write-Host "Development dependencies installed" -ForegroundColor Green
}

Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
$pytestVersion = pytest --version 2>&1
Write-Host "pytest version: $pytestVersion" -ForegroundColor Green

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run tests: .\run_tests.ps1" -ForegroundColor White
Write-Host "  2. Run the app: python todo_with_tags.py" -ForegroundColor White
Write-Host ""
Write-Host "Note: The virtual environment is now activated in this session." -ForegroundColor Yellow
Write-Host "To activate it manually in a new session, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
