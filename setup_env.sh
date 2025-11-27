#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"
PYTHON_COMMAND=${PYTHON:-python3}

if ! command -v "$PYTHON_COMMAND" >/dev/null 2>&1; then
  echo "Python 3.8+ is required. Command '$PYTHON_COMMAND' not found." >&2
  exit 1
fi

# Version check
"$PYTHON_COMMAND" - <<'PY'
import sys
if sys.version_info < (3, 8):
    raise SystemExit(f"Python 3.8+ is required. Found {sys.version.split()[0]}")
PY

if [[ ! -d "$VENV" || "${FORCE:-}" != "" ]]; then
  echo "Creating virtual environment at $VENV"
  "$PYTHON_COMMAND" -m venv "$VENV"
fi

# shellcheck source=/dev/null
source "$VENV/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r "$ROOT/requirements-dev.txt"

echo "Verifying pytest installation..."
pytest --version

echo "Environment ready at $VENV"
