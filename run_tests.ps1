param(
    [string]$venvPath = "venv"
)

if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual environment not found, creating..."
    python -m venv $venvPath
}

Write-Host "Using virtual environment: $venvPath"
$py = "$venvPath\Scripts\python.exe"
& $py -m pip install --upgrade pip
& $py -m pip install -r requirements-dev.txt

Write-Host "Running pytest..."
& $py -m pytest -q
