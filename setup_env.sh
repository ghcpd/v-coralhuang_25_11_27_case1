#!/bin/bash
# Todo Application - Setup Environment Script (Linux/Mac)
# This script sets up the Python virtual environment and installs dependencies
# Usage: ./setup_env.sh

set -e

echo "=== Todo Application - Environment Setup ==="
echo ""

# Check Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found: Python $PYTHON_VERSION"

# Extract major.minor version
MAJOR_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1,2)
MAJOR=$(echo "$MAJOR_MINOR" | cut -d'.' -f1)
MINOR=$(echo "$MAJOR_MINOR" | cut -d'.' -f2)

# Check if version is 3.8 or higher
if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8 or higher is required. Found: $MAJOR_MINOR"
    exit 1
fi

echo "✓ Python version check passed"
echo ""

# Check if venv exists
VENV_PATH="venv"
FORCE_SETUP=false

# Parse command line arguments
if [ "$1" = "--force" ]; then
    FORCE_SETUP=true
fi

if [ -d "$VENV_PATH" ] && [ "$FORCE_SETUP" = false ]; then
    echo "Virtual environment already exists"
else
    if [ "$FORCE_SETUP" = true ] && [ -d "$VENV_PATH" ]; then
        echo "Removing existing virtual environment..."
        rm -rf "$VENV_PATH"
    fi
    
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    echo "✓ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet 2>/dev/null || echo "WARNING: pip upgrade had issues"
echo "✓ pip updated"
echo ""

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing runtime dependencies..."
    pip install -r requirements.txt --quiet 2>/dev/null || echo "WARNING: Some runtime dependencies failed"
    echo "✓ Runtime dependencies installed"
else
    echo "No runtime dependencies to install"
fi

echo ""

# Install dev requirements
if [ -f "requirements-dev.txt" ]; then
    echo "Installing development dependencies (pytest)..."
    if pip install -r requirements-dev.txt --quiet 2>/dev/null; then
        echo "✓ Development dependencies installed"
    else
        echo "ERROR: Failed to install development dependencies"
        exit 1
    fi
else
    echo "No development dependencies to install"
fi

echo ""

# Verify installation
echo "Verifying installations..."
PYTHON_CHECK=$(python -c "import sys; print(f'Python: {sys.version.split()[0]}')" 2>/dev/null || echo "")
PYTEST_CHECK=$(python -c "import pytest; print(f'pytest: {pytest.__version__}')" 2>/dev/null || echo "")

if [ -n "$PYTHON_CHECK" ]; then
    echo "✓ Python verified"
else
    echo "ERROR: Python verification failed"
    exit 1
fi

if [ -n "$PYTEST_CHECK" ]; then
    echo "✓ pytest verified"
else
    echo "ERROR: pytest verification failed"
    exit 1
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. To run tests: ./run_tests.sh"
echo "2. To run application: python todo_with_tags.py"
echo "3. To activate venv manually: source ./venv/bin/activate"
echo ""
