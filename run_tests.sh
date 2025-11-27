#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  echo "Virtual environment not found. Running setup..."
  ./setup_env.sh
fi

VENV_PYTHON=".venv/bin/python"
if [[ $# -gt 0 ]]; then
  "$VENV_PYTHON" -m pytest "$@"
else
  "$VENV_PYTHON" -m pytest
fi
