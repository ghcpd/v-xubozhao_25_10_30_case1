VENV=venv

.PHONY: setup test clean

setup:
	python -m venv $(VENV)
	$(VENV)/bin/pip install -U pip || true
	$(VENV)/bin/pip install -r requirements.txt || true

test:
	pytest --cov=model_service --cov-report=term --cov-report=html:.coverage_reports/html --cov-report=xml:.coverage_reports/coverage.xml -q || true
	coverage report -m

clean:
	rm -rf $(VENV) .coverage_reports .pytest_cache
