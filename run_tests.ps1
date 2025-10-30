# PowerShell runner
if (!(Test-Path -Path ".venv")) {
    ./setup.ps1
}
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
pytest --cov=src --cov-report=term --cov-report=html:htmlcov tests 2>&1 | Tee-Object -FilePath test_output.log
coverage xml -o coverage.xml
