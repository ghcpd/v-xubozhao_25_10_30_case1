#!/bin/bash
# ML Inference Service Testing - Setup Script for Linux/macOS
# This script sets up the reproducible test environment

set -e

echo "================================"
echo "ML Inference Service - Setup"
echo "================================"
echo ""

# Check if Python is installed
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
echo "[2/4] Creating virtual environment..."
VENV_PATH="venv"
if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
    echo "✓ Virtual environment created at: $VENV_PATH"
else
    echo "✓ Virtual environment already exists at: $VENV_PATH"
fi
echo ""

# Activate virtual environment
echo "[3/4] Activating virtual environment..."
source "$VENV_PATH/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/4] Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Installation complete!"
echo ""
echo "================================"
echo "Setup Complete"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Run tests:    ./run_tests.sh"
echo "2. View results: Check 'coverage_report' directory"
echo ""
