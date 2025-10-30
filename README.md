Reproducible test environment for inference service

Setup and run tests:
- Linux/Mac
  ./setup.sh
  ./run_tests.sh
- Windows (PowerShell)
  ./setup.ps1
  ./run_tests.ps1

The tests read `sample_input.json` located at the repo root and validate:
- main model path
- fallback when input short
- fallback when main model raises
- error handling for None input
- tests automatically add repository root to `sys.path` so `pytest -v` works in any shell (PowerShell, bash)

Coverage is generated into `htmlcov` and `coverage.xml` (also printed to console).
