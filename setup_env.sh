#!/bin/bash
# Setup Environment Script for Linux/Mac
# This script sets up a Python virtual environment and installs dependencies

echo "=== Todo App with Tags - Environment Setup (Linux/Mac) ==="
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "Found: $PYTHON_VERSION"

# Extract version number and check if >= 3.8
VERSION_NUM=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
MAJOR=$(echo $VERSION_NUM | cut -d. -f1)
MINOR=$(echo $VERSION_NUM | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8 or higher is required"
    echo "Current version: $VERSION_NUM"
    exit 1
fi

echo ""

# Create virtual environment
VENV_PATH="venv"
if [ -d "$VENV_PATH" ]; then
    echo "Virtual environment already exists at '$VENV_PATH'"
    read -p "Do you want to recreate it? (y/N): " response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo "Removing existing virtual environment..."
        rm -rf "$VENV_PATH"
        echo "Creating new virtual environment..."
        $PYTHON_CMD -m venv "$VENV_PATH"
        echo "Virtual environment created successfully"
    else
        echo "Using existing virtual environment"
    fi
else
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_PATH"
    echo "Virtual environment created successfully"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

if [ $? -eq 0 ]; then
    echo "Virtual environment activated"
else
    echo "ERROR: Could not activate virtual environment"
    exit 1
fi

echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "pip upgraded successfully"

echo ""

# Install dependencies
echo "Installing dependencies..."

if [ -f "requirements.txt" ]; then
    echo "Installing production dependencies from requirements.txt..."
    pip install -r requirements.txt --quiet
    echo "Production dependencies installed"
fi

if [ -f "requirements-dev.txt" ]; then
    echo "Installing development dependencies from requirements-dev.txt..."
    pip install -r requirements-dev.txt --quiet
    echo "Development dependencies installed"
fi

echo ""

# Verify installation
echo "Verifying installation..."
PYTEST_VERSION=$(pytest --version 2>&1)
echo "pytest version: $PYTEST_VERSION"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run tests: ./run_tests.sh"
echo "  2. Run the app: python todo_with_tags.py"
echo ""
echo "Note: The virtual environment is now activated in this session."
echo "To activate it manually in a new session, run:"
echo "  source venv/bin/activate"
echo ""
