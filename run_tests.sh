#!/bin/bash
# Todo Application - Test Runner Script (Linux/Mac)
# This script runs the test suite using pytest
# Usage: ./run_tests.sh [options]

set -e

TEST_FILE=""
VERBOSE=false
COVERAGE=false
ADDITIONAL_ARGS=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--test)
            TEST_FILE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        *)
            ADDITIONAL_ARGS="$ADDITIONAL_ARGS $1"
            shift
            ;;
    esac
done

echo "=== Todo Application - Test Suite ==="
echo ""

# Check if venv exists
VENV_PATH="venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Running setup..."
    echo ""
    if ! ./setup_env.sh; then
        echo "ERROR: Setup failed"
        exit 1
    fi
    echo ""
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Build pytest command
PYTEST_CMD="pytest"

if [ -n "$TEST_FILE" ]; then
    PYTEST_CMD="$PYTEST_CMD $TEST_FILE"
else
    PYTEST_CMD="$PYTEST_CMD test_todo_with_tags.py"
fi

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -vv"
else
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=. --cov-report=html --cov-report=term"
fi

if [ -n "$ADDITIONAL_ARGS" ]; then
    PYTEST_CMD="$PYTEST_CMD $ADDITIONAL_ARGS"
fi

echo "Running tests..."
echo "Command: $PYTEST_CMD"
echo ""

# Run tests
eval "python -m $PYTEST_CMD"
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=== All Tests Passed ==="
else
    echo "=== Some Tests Failed ==="
fi

echo ""

if [ "$COVERAGE" = true ]; then
    echo "Coverage report generated in htmlcov/index.html"
fi

exit $TEST_EXIT_CODE
