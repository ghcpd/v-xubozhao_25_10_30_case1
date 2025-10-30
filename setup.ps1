param()

Write-Host "Creating virtual environment in .venv"
python -m venv .venv

Write-Host "Activating virtual environment"
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and installing dependencies"
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Setup complete. To activate the virtual environment run: . .\\.venv\\Scripts\\Activate.ps1"
