# run_tests.ps1 - Run test suite inside virtual environment (Windows PowerShell)
if (-not (Test-Path -Path .venv)) {
    Write-Host "No virtual environment found. Running setup..."
    .\setup_env.ps1
}

# Activate venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

pytest -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host "All tests passed ✅"
} else {
    Write-Host "Tests failed ❌"
}
exit $LASTEXITCODE
