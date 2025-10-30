# ML Inference Service Testing - Run Tests Script
# This script executes all tests and generates coverage reports

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Running ML Inference Service Tests" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get timestamp for logs
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = "test_logs"
$reportDir = "coverage_report"

# Create log and report directories
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}
if (-not (Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir | Out-Null
}

$logFile = Join-Path $logDir "test_run_$timestamp.log"
$htmlReportPath = Join-Path $reportDir "index.html"

Write-Host "Test Log:    $logFile" -ForegroundColor Cyan
Write-Host "HTML Report: $htmlReportPath" -ForegroundColor Cyan
Write-Host ""

# Start logging
"Test Run: $timestamp" | Out-File -FilePath $logFile -Encoding UTF8

Write-Host "[1/3] Running unit tests with coverage..." -ForegroundColor Yellow
# Run pytest with coverage
pytest test_ml_inference_service.py `
    --verbose `
    --cov=ml_inference_service `
    --cov-report=term-missing `
    --cov-report=html:$reportDir `
    --cov-report=json:$reportDir/coverage.json `
    -v | Tee-Object -FilePath $logFile -Append

$testExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "[2/3] Generating coverage report summary..." -ForegroundColor Yellow

# Generate coverage badge
$coverageJson = Join-Path $reportDir "coverage.json"
if (Test-Path $coverageJson) {
    Write-Host "✓ Coverage data collected" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/3] Test Summary" -ForegroundColor Yellow

# Display test results
if ($testExitCode -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
    "All tests passed successfully!" | Out-File -FilePath $logFile -Append
} else {
    Write-Host "✗ Some tests failed (exit code: $testExitCode)" -ForegroundColor Red
    "Tests failed with exit code: $testExitCode" | Out-File -FilePath $logFile -Append
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Test Execution Complete" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Reports Generated:" -ForegroundColor Yellow
Write-Host "  • HTML Coverage:  $htmlReportPath" -ForegroundColor Cyan
Write-Host "  • JSON Coverage:  $coverageJson" -ForegroundColor Cyan
Write-Host "  • Test Log:       $logFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "To view HTML report:" -ForegroundColor Yellow
Write-Host "  • Windows: start '$htmlReportPath'" -ForegroundColor White
Write-Host "  • On Browser: Open file://$((Get-Location).Path)/$htmlReportPath" -ForegroundColor White
Write-Host ""

exit $testExitCode
