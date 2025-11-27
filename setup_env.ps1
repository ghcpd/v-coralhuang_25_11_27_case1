param(
    [string]$venvPath = "venv"
)

Write-Host "Checking Python 3.8+..."
$py = & python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>$null
if (-not $?) {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.8+"
    exit 1
}
if ([version]$py -lt [version]'3.8') {
    Write-Error "Python 3.8+ is required (found $py)"
    exit 1
}

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment: $venvPath"
    python -m venv $venvPath
}

Write-Host "Activating virtual environment"
. "$venvPath\Scripts\Activate.ps1"

Write-Host "Installing dev dependencies from requirements-dev.txt"
pip install --upgrade pip
pip install -r requirements-dev.txt

Write-Host "Environment setup complete. To run tests: .\run_tests.ps1"
