# setup_env.ps1 - Setup Python venv and install dependencies (Windows PowerShell)
param(
    [string]$PythonExe = 'python'
)

$python = Get-Command $PythonExe -ErrorAction SilentlyContinue
if (-not $python) {
    throw "Python executable '$PythonExe' was not found. Please install Python 3.8+ and ensure it's on PATH."
}

$ver = &$PythonExe -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"
$major, $minor = $ver -split '\.'
if (($major -lt 3) -or (($major -eq 3) -and ($minor -lt 8))) {
    throw "Python 3.8+ required. Found: $ver"
}

if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment in .venv..."
    &$PythonExe -m venv .venv
}

# Activate venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

python -V
pip -V
Write-Host "Setup complete. Activate the venv with: . .\.venv\Scripts\Activate.ps1"
