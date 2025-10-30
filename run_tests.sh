#!/usr/bin/env bash
set -euo pipefail
if [ -f venv/bin/activate ]; then
  . venv/bin/activate
fi

# Run pytest with coverage
pytest --cov=model_service --cov-report=term --cov-report=html:.coverage_reports/html --cov-report=xml:.coverage_reports/coverage.xml -q

# Print & save summary
coverage report -m | tee .coverage_reports/summary.txt
