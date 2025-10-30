#!/usr/bin/env bash
set -euo pipefail

# Run tests with coverage and output reports
coverage run -m pytest -q
coverage report -m
coverage html -d coverage_html
echo "Coverage HTML report generated in coverage_html/"
