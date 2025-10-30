# ML Inference Service Testing - Setup Script
# This script sets up the reproducible test environment

Write-Host "================================" -ForegroundColor Cyan
Write-Host "ML Inference Service - Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}
$pythonVersion = python --version
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment if it doesn't exist
Write-Host "[2/4] Creating virtual environment..." -ForegroundColor Yellow
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    python -m venv $venvPath
    Write-Host "✓ Virtual environment created at: $venvPath" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists at: $venvPath" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "[3/4] Activating virtual environment..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "[4/4] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "✓ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run tests:    .\run_tests.ps1" -ForegroundColor White
Write-Host "2. View results: Check 'coverage_report' directory" -ForegroundColor White
Write-Host ""
