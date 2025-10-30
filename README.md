# Inference Service - Test Suite

This project demonstrates a minimal ML inference service with a primary model and a fallback model. The tests cover normal execution, fallback logic, and error handling.

## Setup (Windows - PowerShell)

1. Open PowerShell
2. Run `.uild\setup.ps1` or `.\\setup.ps1` (or `.\\setup.ps1` from workspace root)
3. Activate the virtual environment:
   - `.\venv\Scripts\Activate.ps1`

## Setup (Unix / macOS)

1. Run `./setup.sh`
2. Activate the virtual environment:
   - `source venv/bin/activate`

## Run Tests

- PowerShell: `.
un_tests.ps1`
- Unix: `./run_tests.sh`
- Make: `make test`

Coverage reports will be generated under `.coverage_reports/html` and `.coverage_reports/coverage.xml`.

## Files
- `model_service.py` - Inference service with main and fallback models
- `tests/test_model_service.py` - Unit tests covering main and fallback paths
- `sample_input.json` - Test input data
- `requirements.txt` - Test dependencies
- `setup.sh`, `setup.ps1` - Setup scripts
- `run_tests.sh`, `run_tests.ps1` - Run test scripts
- `Makefile` - Convenience commands

