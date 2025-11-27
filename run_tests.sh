#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
  echo "No venv found. Setting up environment..."
  ./setup_env.sh
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

# Run pytest
pytest -q

RESULT=$?
if [ $RESULT -eq 0 ]; then
  echo "All tests passed ✅"
else
  echo "Tests failed ❌"
fi
exit $RESULT
