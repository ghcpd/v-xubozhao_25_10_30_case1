Write-Host "Running tests with coverage..."
python -m coverage run -m pytest -q
python -m coverage report -m
python -m coverage html -d coverage_html
Write-Host "Coverage HTML report generated in coverage_html/"
