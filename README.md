Inference service tests and automation

Files added:

- `inference_service/service.py`: Minimal inference service with main and fallback models.
- `tests/test_inference.py`: Pytest tests covering main, fallback, and error paths.
- `requirements.txt`: Python test dependencies.
- `setup.sh` / `setup.ps1`: Install dependencies (bash and PowerShell).
- `run_tests.sh` / `run_tests.ps1`: Run tests and generate coverage reports.

Quick start (PowerShell on Windows):

```powershell
.\
\setup.ps1
.\run_tests.ps1
```

Quick start (Unix / WSL / Git Bash):

```bash
./setup.sh
./run_tests.sh
```
