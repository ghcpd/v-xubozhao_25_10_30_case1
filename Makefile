.PHONY: setup test

setup:
	@echo "Creating virtual environment and installing dependencies"
	python3 -m venv .venv
	@echo "Activating .venv and installing requirements"
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt

test: setup
	@echo "Running tests with coverage"
	. .venv/bin/activate && pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing --cov-report=html:coverage_html
