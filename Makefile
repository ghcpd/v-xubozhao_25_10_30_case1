.PHONY: help setup install test coverage clean report all

PYTHON := python
PIP := pip
VENV := venv
TEST_FILE := test_ml_inference_service.py
SOURCE_FILE := ml_inference_service.py
COVERAGE_DIR := coverage_report
LOG_DIR := test_logs

help:
	@echo "ML Inference Service Testing - Make Commands"
	@echo "=============================================="
	@echo "Available commands:"
	@echo "  make setup       - Set up virtual environment and install dependencies"
	@echo "  make install     - Install dependencies (requires venv activated)"
	@echo "  make test        - Run all tests"
	@echo "  make coverage    - Run tests with coverage report"
	@echo "  make report      - Generate and display coverage report"
	@echo "  make clean       - Clean up generated files and directories"
	@echo "  make all         - Run setup, test, and generate report"
	@echo "=============================================="

setup:
	@echo "[1/2] Creating virtual environment..."
	@if [ -d "$(VENV)" ]; then \
		echo "Virtual environment already exists"; \
	else \
		$(PYTHON) -m venv $(VENV); \
		echo "Virtual environment created"; \
	fi
	@echo "[2/2] Installing dependencies..."
	@if command -v python3 &> /dev/null; then \
		. $(VENV)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt; \
	else \
		$(PIP) install --upgrade pip && $(PIP) install -r requirements.txt; \
	fi
	@echo "Setup complete!"

install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Installation complete!"

test:
	@echo "Running tests..."
	@if [ ! -d "$(LOG_DIR)" ]; then mkdir -p $(LOG_DIR); fi
	pytest $(TEST_FILE) -v

coverage:
	@echo "Running tests with coverage analysis..."
	@if [ ! -d "$(LOG_DIR)" ]; then mkdir -p $(LOG_DIR); fi
	@if [ ! -d "$(COVERAGE_DIR)" ]; then mkdir -p $(COVERAGE_DIR); fi
	pytest $(TEST_FILE) \
		--verbose \
		--cov=ml_inference_service \
		--cov-report=term-missing \
		--cov-report=html:$(COVERAGE_DIR) \
		--cov-report=json:$(COVERAGE_DIR)/coverage.json
	@echo "Coverage report generated in $(COVERAGE_DIR)"

report:
	@echo "Coverage Report Summary"
	@echo "======================="
	@if [ -f "$(COVERAGE_DIR)/coverage.json" ]; then \
		cat $(COVERAGE_DIR)/coverage.json | grep -o '"percent_covered": [0-9.]*' | head -1; \
	else \
		echo "No coverage data found. Run 'make coverage' first."; \
	fi
	@echo ""
	@echo "HTML Report: $(COVERAGE_DIR)/index.html"

clean:
	@echo "Cleaning up..."
	rm -rf $(COVERAGE_DIR)
	rm -rf $(LOG_DIR)
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .coverage
	@echo "Cleanup complete!"

all: clean setup coverage report
	@echo ""
	@echo "All tasks completed successfully!"
	@echo "Test coverage report is available at: $(COVERAGE_DIR)/index.html"
