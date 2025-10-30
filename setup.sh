#!/usr/bin/env bash
set -euo pipefail
python -m venv venv
. venv/bin/activate
pip install -U pip
pip install -r requirements.txt

mkdir -p .coverage_reports || true

echo "Environment setup complete. Activate the venv with 'source venv/bin/activate'"