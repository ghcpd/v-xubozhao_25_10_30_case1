#!/bin/bash
# ML Inference Service Testing - Run Tests Script for Linux/macOS
# This script executes all tests and generates coverage reports

set -e

echo "================================"
echo "Running ML Inference Service Tests"
echo "================================"
echo ""

# Get timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="test_logs"
REPORT_DIR="coverage_report"

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "$REPORT_DIR"

LOG_FILE="$LOG_DIR/test_run_$TIMESTAMP.log"
HTML_REPORT="$REPORT_DIR/index.html"

echo "Test Log:    $LOG_FILE"
echo "HTML Report: $HTML_REPORT"
echo ""

# Start logging
echo "Test Run: $TIMESTAMP" > "$LOG_FILE"

echo "[1/3] Running unit tests with coverage..."
# Run pytest with coverage
pytest test_ml_inference_service.py \
    --verbose \
    --cov=ml_inference_service \
    --cov-report=term-missing \
    --cov-report=html:"$REPORT_DIR" \
    --cov-report=json:"$REPORT_DIR"/coverage.json \
    -v | tee -a "$LOG_FILE"

TEST_EXIT_CODE=$?

echo ""
echo "[2/3] Generating coverage report summary..."

# Check if coverage data was generated
COVERAGE_JSON="$REPORT_DIR/coverage.json"
if [ -f "$COVERAGE_JSON" ]; then
    echo "✓ Coverage data collected"
fi

echo ""
echo "[3/3] Test Summary"

# Display test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed!"
    echo "All tests passed successfully!" >> "$LOG_FILE"
else
    echo "✗ Some tests failed (exit code: $TEST_EXIT_CODE)"
    echo "Tests failed with exit code: $TEST_EXIT_CODE" >> "$LOG_FILE"
fi

echo ""
echo "================================"
echo "Test Execution Complete"
echo "================================"
echo ""
echo "Reports Generated:"
echo "  • HTML Coverage:  $HTML_REPORT"
echo "  • JSON Coverage:  $COVERAGE_JSON"
echo "  • Test Log:       $LOG_FILE"
echo ""
echo "To view HTML report:"
echo "  • macOS:  open '$HTML_REPORT'"
echo "  • Linux:  xdg-open '$HTML_REPORT' (or your preferred browser)"
echo ""

exit $TEST_EXIT_CODE
