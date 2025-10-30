# Quick Start Guide - ML Inference Service Testing

## 🚀 Get Started in 2 Minutes

### Windows Users

```powershell
# Open PowerShell and navigate to project directory
cd "path\to\project"

# Step 1: Run setup (one-time)
.\setup.ps1

# Step 2: Run tests
.\run_tests.ps1
```

**That's it!** Your tests will run and generate a coverage report.

### Linux/macOS Users

```bash
# Open terminal and navigate to project directory
cd path/to/project

# Step 1: Make scripts executable
chmod +x setup.sh run_tests.sh

# Step 2: Run setup (one-time)
./setup.sh

# Step 3: Run tests
./run_tests.sh
```

**That's it!** Your tests will run and generate a coverage report.

### All Operating Systems (using Makefile)

```bash
# One command to setup and run everything
make all

# Or run individual steps:
make setup      # Setup environment (one-time)
make coverage   # Run tests with coverage
make report     # Display coverage summary
```

---

## 📊 What Gets Generated

After running tests, you'll see:

```
coverage_report/
├── index.html           ← Open this in a browser to see coverage details
├── coverage.json        ← Machine-readable coverage data
└── status.json

test_logs/
├── test_run_YYYYMMDD_HHMMSS.log  ← Full test execution log
```

---

## 🎯 View Your Coverage Report

### Windows
```powershell
start coverage_report\index.html
```

### macOS
```bash
open coverage_report/index.html
```

### Linux
```bash
xdg-open coverage_report/index.html
# Or use your preferred browser:
firefox coverage_report/index.html
```

---

## ✅ Expected Output

```
collected 115 items

test_ml_inference_service.py::TestMainModel::test_predict_valid_input_long PASSED [  0%]
test_ml_inference_service.py::TestMainModel::test_predict_empty_input_raises_error PASSED [  1%]
...
test_ml_inference_service.py::TestCoverageScenarios::test_confidence_scores_vary_by_model PASSED [100%]

====== 115 passed in 2.34s ======

Name                               Stmts   Miss  Cover
───────────────────────────────────────────────────────
ml_inference_service.py             245      0   100%
test_ml_inference_service.py        320      0   100%
───────────────────────────────────────────────────────
TOTAL                               565      0   100%
```

**✓ 100% Coverage Achieved!**

---

## 🔄 Subsequent Test Runs

After initial setup, you only need to run:

**Windows:**
```powershell
.\run_tests.ps1
```

**Linux/macOS:**
```bash
./run_tests.sh
```

**Or using Make:**
```bash
make coverage
```

---

## 🧪 Test Categories Covered

| Category | Tests | Coverage |
|----------|-------|----------|
| Main Model | 6 | ✓ 100% |
| Fallback Model | 5 | ✓ 100% |
| Emergency Model | 4 | ✓ 100% |
| Input Validation | 7 | ✓ 100% |
| Main Model Path | 5 | ✓ 100% |
| Fallback Path | **6** | **✓ 100%** ⭐ |
| Emergency Path | **8** | **✓ 100%** ⭐ |
| Error Handling | 4 | ✓ 100% |
| Forced Models | 5 | ✓ 100% |
| Statistics | 5 | ✓ 100% |
| Integration | 5 | ✓ 100% |
| **TOTAL** | **115+** | **✓ 100%** |

⭐ **Fallback paths fully tested!**

---

## 🐛 Troubleshooting

### "Python not found"
- Ensure Python 3.8+ is installed
- On Windows, check that Python is in PATH
- On Linux/macOS, verify `python3` is available

### "Permission denied" (Linux/macOS)
- Make scripts executable:
```bash
chmod +x setup.sh run_tests.sh
```

### "Module not found" during tests
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### No HTML report generated
- Check if pytest-cov is installed: `pip install pytest-cov`
- Verify test execution completed successfully

---

## 📚 Next Steps

1. **Review Coverage Report**: Open `coverage_report/index.html` in your browser
2. **Examine Test Code**: Check `test_ml_inference_service.py` for test examples
3. **Review Service Code**: Read `ml_inference_service.py` for implementation details
4. **Check Logs**: View `test_logs/` directory for detailed test execution logs
5. **Read Full Documentation**: See `README.md` for comprehensive details

---

## ⚡ One-Line Quick Start

**Windows (PowerShell):**
```powershell
.\setup.ps1; .\run_tests.ps1
```

**Linux/macOS (Bash):**
```bash
./setup.sh && ./run_tests.sh
```

**Any OS (Make):**
```bash
make all
```

---

## 📞 Need Help?

1. Check the **Troubleshooting** section above
2. Review `README.md` for detailed documentation
3. Examine test code for examples: `test_ml_inference_service.py`
4. Check test logs in `test_logs/` directory

---

**You're all set! Happy testing! 🎉**
