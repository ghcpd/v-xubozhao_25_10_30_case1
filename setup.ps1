$ErrorActionPreference = 'Stop'
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt

if (-not (Test-Path -Path '.coverage_reports')) { New-Item -Path '.coverage_reports' -ItemType Directory | Out-Null }

Write-Host "Environment setup complete. Activate venv: .\venv\Scripts\Activate.ps1"