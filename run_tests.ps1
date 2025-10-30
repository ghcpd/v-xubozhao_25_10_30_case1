$ErrorActionPreference = 'Stop'
if (Test-Path -Path '.\venv\Scripts\Activate.ps1') { . .\venv\Scripts\Activate.ps1 }

pytest --cov=model_service --cov-report=term --cov-report=html:.coverage_reports\html --cov-report=xml:.coverage_reports\coverage.xml -q

$coverage = coverage report -m
$coverage | Out-File -FilePath .coverage_reports\summary.txt -Encoding utf8
Write-Host $coverage
