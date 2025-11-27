#!/bin/bash
set -euo pipefail

VENV_PATH="venv"
if [ ! -d "$VENV_PATH" ]; then
  echo "Virtual environment not found, creating..."
  python -m venv "$VENV_PATH"
fi

PY="$VENV_PATH/bin/python"
echo "Installing dev dependencies..."
$PY -m pip install --upgrade pip
$PY -m pip install -r requirements-dev.txt

echo "Running pytest..."
$PY -m pytest -q
