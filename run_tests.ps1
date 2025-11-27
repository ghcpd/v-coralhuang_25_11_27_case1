Param(
    [Parameter(Mandatory=$false, ValueFromRemainingArguments=$true)]
    [string[]]$pytestArgs
)

$venvPath = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual env not found. Running setup..."
    & "$PSScriptRoot\setup_env.ps1"
}

Write-Host "Running tests with: $($pytestArgs -join ' ')"
if ($pytestArgs) {
    & "$venvPath\Scripts\python.exe" -m pytest @pytestArgs
} else {
    & "$venvPath\Scripts\python.exe" -m pytest
}
