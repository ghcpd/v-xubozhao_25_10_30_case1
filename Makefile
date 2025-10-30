.PHONY: setup test

setup:
	python -m venv .venv
	. .venv/bin/activate; pip install -r requirements.txt

test:
	. .venv/bin/activate; PYTHONPATH=$(pwd) pytest --cov=src --cov-report=term --cov-report=html:htmlcov tests
