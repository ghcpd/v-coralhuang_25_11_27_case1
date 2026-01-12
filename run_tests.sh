#!/bin/bash
# Run Tests Script for Linux/Mac
# This script activates the virtual environment and runs pytest

echo "=== Todo App with Tags - Test Runner (Linux/Mac) ==="
echo ""

# Check if virtual environment exists
VENV_PATH="venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Running setup..."
    echo ""
    bash setup_env.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please fix the errors and try again."
        exit 1
    fi
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

if [ $? -eq 0 ]; then
    echo "Virtual environment activated"
else
    echo "ERROR: Could not activate virtual environment"
    echo "Try running setup_env.sh first"
    exit 1
fi

echo ""

# Check if pytest is installed
echo "Checking pytest installation..."
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Installing dependencies..."
    pip install -r requirements-dev.txt --quiet
    echo "Dependencies installed"
else
    echo "pytest is installed"
fi

echo ""
echo "=== Running Tests ==="
echo ""

# Run pytest with various options based on arguments
if [ $# -eq 0 ]; then
    # Default: run all tests with verbose output
    python -m pytest test_todo_with_tags.py -v
else
    # Pass through any arguments
    python -m pytest "$@"
fi

TEST_EXIT_CODE=$?

echo ""

# Display results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=== All Tests Passed ==="
else
    echo "=== Some Tests Failed ==="
    echo "Review the output above for details"
fi

echo ""
echo "Additional test options:"
echo "  ./run_tests.sh -k test_name    # Run specific test"
echo "  ./run_tests.sh --cov           # Run with coverage"
echo "  ./run_tests.sh -v -s           # Verbose with print output"
echo "  ./run_tests.sh --lf            # Run last failed tests"
echo ""

exit $TEST_EXIT_CODE
