#!/usr/bin/env bash
set -e

# setup_env.sh - Create a venv and install dependencies
PYTHON=${PYTHON:-python3}
if ! command -v ${PYTHON} >/dev/null 2>&1; then
  PYTHON=${PYTHON:-python}
  if ! command -v ${PYTHON} >/dev/null 2>&1; then
    echo "Python not found. Please install Python 3.8+ and ensure 'python' is on PATH."
    exit 1
  fi
fi

ver=$(${PYTHON} -c 'import sys; print("%d.%d" % sys.version_info[:2])')
major=$(echo "${ver}" | cut -d. -f1)
minor=$(echo "${ver}" | cut -d. -f2)
if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
  echo "Python 3.8+ required. Found: ${ver}"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in .venv..."
  ${PYTHON} -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

python -V
pip -V

echo "Setup complete. Activate the venv with: source .venv/bin/activate"
