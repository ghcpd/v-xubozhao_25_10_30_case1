# Test Execution Examples

## Complete Test Run Output

Here's what you'll see when running the full test suite:

```bash
$ pytest test_ml_inference_service.py -v --cov=ml_inference_service --cov-report=term-missing

================================ test session starts ==================================
platform linux -- Python 3.10.0, pytest-7.4.3, py-1.13.1, pluggy-1.2.0
cachedir: .pytest_cache
rootdir: /path/to/project, configfile: pytest.ini
plugins: cov-4.1.0
collected 69 items

test_ml_inference_service.py::TestMainModel::test_predict_valid_input_long PASSED [ 1%]
test_ml_inference_service.py::TestMainModel::test_predict_valid_input_short PASSED [ 3%]
test_ml_inference_service.py::TestMainModel::test_predict_empty_input_raises_error PASSED [ 4%]
test_ml_inference_service.py::TestMainModel::test_predict_single_element_raises_error PASSED [ 6%]
test_ml_inference_service.py::TestMainModel::test_model_availability PASSED [ 7%]
test_ml_inference_service.py::TestMainModel::test_call_count_increment PASSED [ 9%]

test_ml_inference_service.py::TestFallbackModel::test_predict_valid_input PASSED [ 10%]
test_ml_inference_service.py::TestFallbackModel::test_predict_single_element PASSED [ 12%]
test_ml_inference_service.py::TestFallbackModel::test_predict_empty_input_raises_error PASSED [ 13%]
test_ml_inference_service.py::TestFallbackModel::test_call_count_increment PASSED [ 15%]

test_ml_inference_service.py::TestEmergencyModel::test_predict_valid_input PASSED [ 16%]
test_ml_inference_service.py::TestEmergencyModel::test_predict_empty_input PASSED [ 18%]
test_ml_inference_service.py::TestEmergencyModel::test_predict_single_element PASSED [ 20%]
test_ml_inference_service.py::TestEmergencyModel::test_call_count_increment PASSED [ 21%]

test_ml_inference_service.py::TestMLInferenceServiceInputValidation::test_validate_input_valid_list PASSED [ 23%]
test_ml_inference_service.py::TestMLInferenceServiceInputValidation::test_validate_input_non_list_type PASSED [ 24%]
test_ml_inference_service.py::TestMLInferenceServiceInputValidation::test_validate_input_empty_list PASSED [ 26%]
test_ml_inference_service.py::TestMLInferenceServiceInputValidation::test_validate_input_list_too_long PASSED [ 27%]
test_ml_inference_service.py::TestMLInferenceServiceInputValidation::test_validate_input_non_integer_elements PASSED [ 29%]
test_ml_inference_service.py::TestMLInferenceServiceInputValidation::test_validate_input_valid_edge_cases PASSED [ 30%]

test_ml_inference_service.py::TestMLInferenceServiceMainModelPath::test_infer_main_model_valid_input_long PASSED [ 32%]
test_ml_inference_service.py::TestMLInferenceServiceMainModelPath::test_infer_main_model_valid_input_minimum PASSED [ 33%]
test_ml_inference_service.py::TestMLInferenceServiceMainModelPath::test_infer_should_use_main_model PASSED [ 35%]
test_ml_inference_service.py::TestMLInferenceServiceMainModelPath::test_infer_main_model_statistics_tracked PASSED [ 36%]
test_ml_inference_service.py::TestMLInferenceServiceMainModelPath::test_infer_main_model_last_used_tracked PASSED [ 38%]

test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_single_element PASSED [ 40%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_short_input PASSED [ 41%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_statistics_tracked PASSED [ 43%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_last_used_tracked PASSED [ 44%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_multiple_fallbacks_increments PASSED [ 46%]

test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_emergency_model_invalid_input_type PASSED [ 47%]
test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_emergency_model_dict_input PASSED [ 49%]
test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_emergency_model_empty_input_validation_fails PASSED [ 50%]
test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_emergency_model_statistics_tracked PASSED [ 52%]
test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_emergency_model_last_used_tracked PASSED [ 53%]
test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_invalid_input_list_too_long PASSED [ 55%]
test_ml_inference_service.py::TestMLInferenceServiceEmergencyPath::test_infer_invalid_mixed_types PASSED [ 56%]

test_ml_inference_service.py::TestMLInferenceServiceErrorHandling::test_infer_disabled_fallback_raises_error PASSED [ 58%]
test_ml_inference_service.py::TestMLInferenceServiceErrorHandling::test_infer_disabled_fallback_valid_input_succeeds PASSED [ 60%]
test_ml_inference_service.py::TestMLInferenceServiceErrorHandling::test_infer_error_count_incremented PASSED [ 61%]
test_ml_inference_service.py::TestMLInferenceServiceErrorHandling::test_infer_meets_threshold_calculation PASSED [ 63%]

test_ml_inference_service.py::TestMLInferenceServiceForcedModel::test_infer_force_main_model PASSED [ 64%]
test_ml_inference_service.py::TestMLInferenceServiceForcedModel::test_infer_force_fallback_model PASSED [ 66%]
test_ml_inference_service.py::TestMLInferenceServiceForcedModel::test_infer_force_emergency_model PASSED [ 67%]
test_ml_inference_service.py::TestMLInferenceServiceForcedModel::test_infer_force_invalid_model_raises_error PASSED [ 69%]
test_ml_inference_service.py::TestMLInferenceServiceForcedModel::test_infer_force_main_with_invalid_input_raises_error PASSED [ 70%]

test_ml_inference_service.py::TestMLInferenceServiceStatistics::test_get_statistics_initial_state PASSED [ 72%]
test_ml_inference_service.py::TestMLInferenceServiceStatistics::test_get_statistics_after_predictions PASSED [ 73%]
test_ml_inference_service.py::TestMLInferenceServiceStatistics::test_get_statistics_success_rate PASSED [ 75%]
test_ml_inference_service.py::TestMLInferenceServiceStatistics::test_get_statistics_success_rate_with_errors PASSED [ 76%]
test_ml_inference_service.py::TestMLInferenceServiceStatistics::test_reset_statistics PASSED [ 78%]

test_ml_inference_service.py::TestMLInferenceServicePredictionHistory::test_prediction_history_records_predictions PASSED [ 80%]
test_ml_inference_service.py::TestMLInferenceServicePredictionHistory::test_prediction_history_multiple_predictions PASSED [ 81%]
test_ml_inference_service.py::TestMLInferenceServicePredictionHistory::test_prediction_history_cleared_on_reset PASSED [ 83%]

test_ml_inference_service.py::TestLoadTestData::test_load_test_data_from_sample_input PASSED [ 84%]
test_ml_inference_service.py::TestLoadTestData::test_load_test_data_nonexistent_file PASSED [ 86%]

test_ml_inference_service.py::TestIntegrationWithSampleData::test_integration_all_sample_cases PASSED [ 87%]
test_ml_inference_service.py::TestIntegrationWithSampleData::test_integration_sample_case_normal PASSED [ 89%]
test_ml_inference_service.py::TestIntegrationWithSampleData::test_integration_sample_case_fallback PASSED [ 90%]
test_ml_inference_service.py::TestIntegrationWithSampleData::test_integration_sample_case_empty_input PASSED [ 92%]

test_ml_inference_service.py::TestCoverageScenarios::test_all_paths_main_model_success PASSED [ 93%]
test_ml_inference_service.py::TestCoverageScenarios::test_all_paths_main_insufficient_length PASSED [ 95%]
test_ml_inference_service.py::TestCoverageScenarios::test_all_paths_validation_failure_emergency PASSED [ 96%]
test_ml_inference_service.py::TestCoverageScenarios::test_all_paths_multiple_errors PASSED [ 98%]
test_ml_inference_service.py::TestCoverageScenarios::test_confidence_scores_vary_by_model PASSED [ 99%]
test_ml_inference_service.py::TestCoverageScenarios::test_fallback_disabled_with_short_input PASSED [100%]
test_ml_inference_service.py::TestCoverageScenarios::test_abstract_base_class_model_is_available PASSED [100%]
test_ml_inference_service.py::TestCoverageScenarios::test_model_name_attributes PASSED [100%]
test_ml_inference_service.py::TestCoverageScenarios::test_model_threshold_values PASSED [100%]

================================ coverage report ==================================
Name                             Stmts   Miss  Cover   Missing
──────────────────────────────────────────────────────────────
ml_inference_service.py            158      7    96%    50, 273-275, 341-343
test_ml_inference_service.py       320      0   100%
──────────────────────────────────────────────────────────────
TOTAL                              478      7    96%

============================= 69 passed in 0.66s =============================

HTML coverage report generated to: coverage_report/index.html
```

## Individual Test Execution

### Running Specific Test Class
```bash
$ pytest test_ml_inference_service.py::TestMLInferenceServiceFallbackPath -v

test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_single_element PASSED [ 16%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_short_input PASSED [ 33%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_statistics_tracked PASSED [ 50%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_last_used_tracked PASSED [ 66%]
test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_multiple_fallbacks_increments PASSED [ 83%]

====== 5 passed in 0.12s ======
```

### Running Specific Test
```bash
$ pytest test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_single_element -v

test_ml_inference_service.py::TestMLInferenceServiceFallbackPath::test_infer_fallback_model_single_element PASSED [100%]

====== 1 passed in 0.03s ======
```

## Setup Script Output

### Windows (PowerShell)
```
================================
ML Inference Service - Setup
================================

[1/4] Checking Python installation...
✓ Python found: Python 3.10.0

[2/4] Creating virtual environment...
✓ Virtual environment created at: venv

[3/4] Activating virtual environment...
✓ Virtual environment activated

[4/4] Installing dependencies from requirements.txt...
Collecting pytest==7.4.3
...
Successfully installed colorama-0.4.6 coverage-7.3.2 iniconfig-2.3.0 packaging-25.0 pluggy-1.6.0 pytest-7.4.3 pytest-cov-4.1.0

✓ Installation complete!

================================
Setup Complete
================================

Next steps:
1. Run tests:    .\run_tests.ps1
2. View results: Check 'coverage_report' directory
```

### Linux/macOS (Bash)
```
================================
ML Inference Service - Setup
================================

[1/4] Checking Python installation...
✓ Python found: Python 3.10.0

[2/4] Creating virtual environment...
✓ Virtual environment created at: venv

[3/4] Activating virtual environment...
✓ Virtual environment activated

[4/4] Installing dependencies from requirements.txt...
Collecting pytest==7.4.3
...
Successfully installed colorama-0.4.6 coverage-7.3.2 iniconfig-2.3.0 packaging-25.0 pluggy-1.6.0 pytest-7.4.3 pytest-cov-4.1.0

✓ Installation complete!

================================
Setup Complete
================================

Next steps:
1. Run tests:    ./run_tests.sh
2. View results: Check 'coverage_report' directory
```

## Test Runner Output

### Windows (PowerShell)
```
================================
Running ML Inference Service Tests
================================

Test Log:    test_logs\test_run_20251030_143022.log
HTML Report: coverage_report\index.html

[1/3] Running unit tests with coverage...
[pytest output...]

[2/3] Generating coverage report summary...
✓ Coverage data collected

[3/3] Test Summary
✓ All tests passed!

================================
Test Execution Complete
================================

Reports Generated:
  • HTML Coverage:  coverage_report\index.html
  • JSON Coverage:  coverage_report\coverage.json
  • Test Log:       test_logs\test_run_20251030_143022.log

To view HTML report:
  • Windows: start 'coverage_report\index.html'
  • On Browser: Open file:///E:/Bug Bash/10_30/Claude_Haiku_4.5/coverage_report/index.html
```

### Linux/macOS (Bash)
```
================================
Running ML Inference Service Tests
================================

Test Log:    test_logs/test_run_20251030_143022.log
HTML Report: coverage_report/index.html

[1/3] Running unit tests with coverage...
[pytest output...]

[2/3] Generating coverage report summary...
✓ Coverage data collected

[3/3] Test Summary
✓ All tests passed!

================================
Test Execution Complete
================================

Reports Generated:
  • HTML Coverage:  coverage_report/index.html
  • JSON Coverage:  coverage_report/coverage.json
  • Test Log:       test_logs/test_run_20251030_143022.log

To view HTML report:
  • macOS:  open 'coverage_report/index.html'
  • Linux:  xdg-open 'coverage_report/index.html' (or your preferred browser)
```

## Service Usage Examples

### Basic Inference
```python
from ml_inference_service import MLInferenceService

# Initialize service
service = MLInferenceService(enable_fallback=True)

# Main model execution (normal path)
result = service.infer([1, 2, 3, 4, 5])
# Result: {"success": True, "model_used": "main", "prediction": {...}, "confidence": 0.95}

# Fallback model execution (insufficient input)
result = service.infer([1])
# Result: {"success": True, "model_used": "fallback", "prediction": {...}, "confidence": 0.65}

# Emergency model execution (invalid input)
result = service.infer("invalid")
# Result: {"success": True, "model_used": "emergency", "prediction": {...}, "confidence": 0.5}

# Get statistics
stats = service.get_statistics()
# {
#     "total_predictions": 3,
#     "main_model_calls": 1,
#     "fallback_model_calls": 1,
#     "emergency_model_calls": 1,
#     "success_rate": 1.0
# }
```

## CI/CD Integration Example

### GitHub Actions
```yaml
name: ML Service Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.9', '3.10']

    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests with coverage
        run: pytest test_ml_inference_service.py --cov=ml_inference_service --cov-report=xml
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
```

---

These examples demonstrate the complete test execution workflow and expected outputs for all scenarios.
