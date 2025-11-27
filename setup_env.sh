#!/bin/bash
set -euo pipefail

VENV_PATH="venv"

echo "Checking Python 3.8+..."
PY_VER=$(python -c 'import sys; print("{}.{}".format(*sys.version_info[:2]))') || {
  echo "Python not found. Please install Python 3.8+" >&2
  exit 1
}
if [[ $(printf '%s\n' "3.8" "$PY_VER" | sort -V | head -n1) != "3.8" ]]; then
  echo "Python 3.8+ is required (found $PY_VER)" >&2
  exit 1
fi

if [ ! -d "$VENV_PATH" ]; then
  echo "Creating virtual environment: $VENV_PATH"
  python -m venv "$VENV_PATH"
fi

echo "Activating virtual environment"
source "$VENV_PATH/bin/activate"

echo "Installing dev dependencies from requirements-dev.txt"
pip install --upgrade pip
pip install -r requirements-dev.txt

echo "Environment setup complete. To run tests: ./run_tests.sh"
