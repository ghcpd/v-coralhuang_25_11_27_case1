param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $root ".venv"

function Get-PythonCmd {
    if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
    if (Get-Command python3 -ErrorAction SilentlyContinue) { return "python3" }
    if (Get-Command py -ErrorAction SilentlyContinue) { return "py" }
    throw "Python 3.8+ not found. Install Python from https://www.python.org/downloads/"
}

$pyCmd = Get-PythonCmd
$versionStr = & $pyCmd -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"
$version = [version]$versionStr
if ($version -lt [version]"3.8") {
    throw "Python 3.8+ is required. Found $versionStr"
}

if ((-not (Test-Path $venvPath)) -or $Force) {
    Write-Host "Creating virtual environment at $venvPath" -ForegroundColor Cyan
    & $pyCmd -m venv $venvPath
}

$activateScript = Join-Path $venvPath "Scripts/Activate.ps1"
. $activateScript

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r (Join-Path $root "requirements-dev.txt")

Write-Host "Verifying pytest installation..." -ForegroundColor Cyan
pytest --version

Write-Host "Environment ready at $venvPath" -ForegroundColor Green
