#!/usr/bin/env bash
set -euo pipefail

echo "Creating virtual environment in .venv"
python3 -m venv .venv
echo "Activating virtual environment"
source .venv/bin/activate
echo "Upgrading pip and installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. To activate the virtual environment run: source .venv/bin/activate"
