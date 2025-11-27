Param()

Write-Host "Checking Python 3.8+..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python is not on PATH. Please install Python 3.8+ and try again."
    exit 1
}

$versionInfo = & python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
if ([version]$versionInfo -lt [version]'3.8.0') {
    Write-Error "Python 3.8+ is required. Found $versionInfo"
    exit 1
}

$venvPath = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath..."
    & python -m venv $venvPath
}

Write-Host "Installing development dependencies..."
& $venvPath\Scripts\python.exe -m pip install --upgrade pip
& $venvPath\Scripts\python.exe -m pip install -r requirements-dev.txt

Write-Host "Environment setup complete. Activate with:`n`$venvPath\Scripts\Activate.ps1`nThen run tests: .\run_tests.ps1"
