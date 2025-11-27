param(
    [string[]]$PytestArgs
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# Ensure env is ready
& (Join-Path $root "setup_env.ps1")

# Activate venv
$activateScript = Join-Path $root ".venv/Scripts/Activate.ps1"
. $activateScript

# Run tests
pytest @PytestArgs
