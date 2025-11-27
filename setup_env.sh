#!/usr/bin/env bash
set -euo pipefail

echo "Checking Python 3.8+..."
PYTHON=$(command -v python || true)
if [[ -z "$PYTHON" ]]; then
  echo "Python not found on PATH. Please install Python 3.8+ and try again." >&2
  exit 1
fi

VERSION=$($PYTHON -c 'import sys; print("{}.{}.{}".format(*sys.version_info[:3]))')
ver() { printf "%02d%02d%02d" $(echo "$1" | tr '.' ' '); }
if [[ $(ver $VERSION) -lt $(ver 3.8.0) ]]; then
  echo "Python 3.8+ is required. Found $VERSION" >&2
  exit 1
fi

VENV_PATH=".venv"
if [[ ! -d "$VENV_PATH" ]]; then
  echo "Creating virtual environment at $VENV_PATH..."
  $PYTHON -m venv "$VENV_PATH"
fi

echo "Installing development dependencies..."
"$VENV_PATH/bin/python" -m pip install --upgrade pip
"$VENV_PATH/bin/python" -m pip install -r requirements-dev.txt

echo "Environment setup complete. Activate with: source $VENV_PATH/bin/activate"
echo "Then run tests: ./run_tests.sh"
