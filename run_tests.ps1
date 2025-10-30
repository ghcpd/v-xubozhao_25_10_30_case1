param()

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host ".venv not found; running setup.ps1 to create a virtual environment and install dependencies"
    .\setup.ps1
}

Write-Host "Activating virtual environment"
. .\.venv\Scripts\Activate.ps1

Write-Host "Running tests with coverage"
pytest --maxfail=1 --disable-warnings -q --cov=src --cov-report=term-missing --cov-report=html:coverage_html

Write-Host "Tests completed. Coverage HTML written to coverage_html/index.html"
