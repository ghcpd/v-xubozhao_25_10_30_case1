#!/usr/bin/env bash
set -euo pipefail
# create venv if not exists
if [ ! -d .venv ]; then
  ./setup.sh
fi
source .venv/bin/activate
# run pytest with coverage
PYTHONPATH=$(pwd) pytest --cov=src --cov-report=term --cov-report=html:htmlcov tests 2>&1 | tee test_output.log
# also produce xml for CI
coverage xml -o coverage.xml
