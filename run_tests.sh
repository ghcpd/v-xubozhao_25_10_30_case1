#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  echo ".venv not found; running setup.sh to create a virtual environment and install dependencies"
  ./setup.sh
fi

# Activate the virtual environment (created by setup.sh)
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Running tests with coverage"
pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing --cov-report=html:coverage_html

echo "Tests completed. Coverage HTML written to coverage_html/index.html"
