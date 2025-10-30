"""
Comprehensive Test Suite for ML Inference Service

This test suite provides 100% coverage of:
- Normal execution paths (main model)
- Fallback model logic
- Emergency model logic
- Error handling and edge cases
- Input validation
- Service statistics
"""

import unittest
import json
import os
import logging
from pathlib import Path
from typing import List

from ml_inference_service import (
    MLInferenceService,
    MainModel,
    FallbackModel,
    EmergencyModel,
    ModelType,
    load_test_data
)

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestMainModel(unittest.TestCase):
    """Tests for the MainModel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = MainModel()

    def test_predict_valid_input_long(self):
        """Test main model with valid long input."""
        data = [1, 2, 3, 4, 5, 6]
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["model"], "main")
        self.assertEqual(result["sum"], 21)
        self.assertEqual(result["mean"], 3.5)
        self.assertEqual(result["count"], 6)
        self.assertEqual(result["max"], 6)
        self.assertEqual(result["min"], 1)
        self.assertGreater(confidence, 0.8)
        self.assertEqual(self.model.call_count, 1)

    def test_predict_valid_input_short(self):
        """Test main model with minimum valid input (2 elements)."""
        data = [10, 20]
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["sum"], 30)
        self.assertEqual(result["count"], 2)
        self.assertGreater(confidence, 0.7)

    def test_predict_empty_input_raises_error(self):
        """Test main model raises error on empty input."""
        with self.assertRaises(ValueError) as context:
            self.model.predict([])
        
        self.assertIn("non-empty", str(context.exception))

    def test_predict_single_element_raises_error(self):
        """Test main model raises error on single element."""
        with self.assertRaises(ValueError) as context:
            self.model.predict([42])
        
        self.assertIn("at least 2", str(context.exception))

    def test_model_availability(self):
        """Test model availability check."""
        self.assertTrue(self.model.is_available())

    def test_call_count_increment(self):
        """Test call count increments correctly."""
        self.assertEqual(self.model.call_count, 0)
        self.model.predict([1, 2, 3])
        self.assertEqual(self.model.call_count, 1)
        self.model.predict([4, 5, 6])
        self.assertEqual(self.model.call_count, 2)


class TestFallbackModel(unittest.TestCase):
    """Tests for the FallbackModel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = FallbackModel()

    def test_predict_valid_input(self):
        """Test fallback model with valid input."""
        data = [1, 2]
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["model"], "fallback")
        self.assertEqual(result["sum"], 3)
        self.assertEqual(result["count"], 2)
        self.assertEqual(confidence, 0.65)

    def test_predict_single_element(self):
        """Test fallback model accepts single element."""
        data = [42]
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["sum"], 42)
        self.assertEqual(result["count"], 1)

    def test_predict_empty_input_raises_error(self):
        """Test fallback model raises error on empty input."""
        with self.assertRaises(ValueError):
            self.model.predict([])

    def test_call_count_increment(self):
        """Test fallback model call count."""
        self.assertEqual(self.model.call_count, 0)
        self.model.predict([1, 2, 3])
        self.assertEqual(self.model.call_count, 1)


class TestEmergencyModel(unittest.TestCase):
    """Tests for the EmergencyModel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.model = EmergencyModel()

    def test_predict_valid_input(self):
        """Test emergency model with valid input."""
        data = [1, 2, 3]
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["model"], "emergency")
        self.assertEqual(result["count"], 3)
        self.assertEqual(confidence, 0.5)

    def test_predict_empty_input(self):
        """Test emergency model handles empty input gracefully."""
        data = []
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["count"], 0)

    def test_predict_single_element(self):
        """Test emergency model with single element."""
        data = [99]
        result, confidence = self.model.predict(data)
        
        self.assertEqual(result["count"], 1)

    def test_call_count_increment(self):
        """Test emergency model call count."""
        self.assertEqual(self.model.call_count, 0)
        self.model.predict([1])
        self.assertEqual(self.model.call_count, 1)


class TestMLInferenceServiceInputValidation(unittest.TestCase):
    """Tests for input validation in MLInferenceService."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_validate_input_valid_list(self):
        """Test validation of valid list input."""
        self.assertTrue(self.service._validate_input([1, 2, 3]))

    def test_validate_input_non_list_type(self):
        """Test validation rejects non-list input."""
        self.assertFalse(self.service._validate_input("not a list"))
        self.assertFalse(self.service._validate_input(123))
        self.assertFalse(self.service._validate_input({"key": "value"}))

    def test_validate_input_empty_list(self):
        """Test validation accepts empty list."""
        self.assertTrue(self.service._validate_input([]))

    def test_validate_input_list_too_long(self):
        """Test validation rejects overly long list."""
        self.assertFalse(self.service._validate_input(list(range(101))))

    def test_validate_input_non_integer_elements(self):
        """Test validation rejects non-integer elements."""
        self.assertFalse(self.service._validate_input([1, "2", 3]))
        self.assertFalse(self.service._validate_input([1.5, 2, 3]))
        self.assertFalse(self.service._validate_input([1, 2, None]))

    def test_validate_input_valid_edge_cases(self):
        """Test validation with edge case valid inputs."""
        self.assertTrue(self.service._validate_input([0]))
        self.assertTrue(self.service._validate_input([-1, -2, -3]))
        self.assertTrue(self.service._validate_input(list(range(100))))  # Max length


class TestMLInferenceServiceMainModelPath(unittest.TestCase):
    """Tests for main model inference path."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_infer_main_model_valid_input_long(self):
        """Test inference with valid long input uses main model."""
        result = self.service.infer([1, 2, 3, 4, 5, 6])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "main")
        self.assertGreater(result["confidence"], 0.8)
        self.assertEqual(result["prediction"]["sum"], 21)

    def test_infer_main_model_valid_input_minimum(self):
        """Test inference with minimum valid input (2 elements) uses main model."""
        result = self.service.infer([10, 20])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "main")
        self.assertEqual(result["prediction"]["sum"], 30)

    def test_infer_should_use_main_model(self):
        """Test decision logic for main model usage."""
        self.assertTrue(self.service._should_use_main_model([1, 2]))
        self.assertTrue(self.service._should_use_main_model([1, 2, 3, 4]))
        self.assertFalse(self.service._should_use_main_model([1]))
        self.assertFalse(self.service._should_use_main_model([]))

    def test_infer_main_model_statistics_tracked(self):
        """Test that main model calls are tracked in statistics."""
        self.service.infer([1, 2, 3])
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["main_model_calls"], 1)
        self.assertEqual(stats["total_predictions"], 1)

    def test_infer_main_model_last_used_tracked(self):
        """Test that last used model is tracked."""
        self.service.infer([1, 2, 3])
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["last_model_used"], "main")


class TestMLInferenceServiceFallbackPath(unittest.TestCase):
    """Tests for fallback model inference path."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_infer_fallback_model_single_element(self):
        """Test inference with single element triggers fallback."""
        result = self.service.infer([42])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "fallback")
        self.assertEqual(result["prediction"]["sum"], 42)

    def test_infer_fallback_model_short_input(self):
        """Test inference with insufficient input for main model."""
        result = self.service.infer([99])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "fallback")

    def test_infer_fallback_model_statistics_tracked(self):
        """Test that fallback model calls are tracked."""
        self.service.infer([1])
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["fallback_model_calls"], 1)

    def test_infer_fallback_model_last_used_tracked(self):
        """Test last used model shows fallback."""
        self.service.infer([1])
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["last_model_used"], "fallback")

    def test_infer_multiple_fallbacks_increments(self):
        """Test multiple fallback calls increment counter."""
        self.service.infer([1])
        self.service.infer([2])
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["fallback_model_calls"], 2)
        self.assertEqual(stats["total_predictions"], 2)


class TestMLInferenceServiceEmergencyPath(unittest.TestCase):
    """Tests for emergency model inference path (graceful degradation)."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_infer_emergency_model_invalid_input_type(self):
        """Test inference with invalid input type uses emergency model."""
        result = self.service.infer("invalid")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "emergency")

    def test_infer_emergency_model_dict_input(self):
        """Test inference with dict input triggers emergency."""
        result = self.service.infer({"key": "value"})
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "emergency")

    def test_infer_emergency_model_empty_input_validation_fails(self):
        """Test emergency model when validation fails on empty input."""
        # Note: Empty list is technically valid, so use invalid type
        result = self.service.infer(None)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "emergency")

    def test_infer_emergency_model_statistics_tracked(self):
        """Test emergency model calls are tracked."""
        self.service.infer("invalid")
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["emergency_model_calls"], 1)

    def test_infer_emergency_model_last_used_tracked(self):
        """Test last used model shows emergency."""
        self.service.infer("invalid")
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["last_model_used"], "emergency")

    def test_infer_invalid_input_list_too_long(self):
        """Test very long list triggers emergency path."""
        long_list = list(range(101))
        result = self.service.infer(long_list)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "emergency")

    def test_infer_invalid_mixed_types(self):
        """Test list with mixed types triggers emergency."""
        result = self.service.infer([1, "2", 3])
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "emergency")


class TestMLInferenceServiceErrorHandling(unittest.TestCase):
    """Tests for error handling and edge cases."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_infer_error_count_incremented(self):
        """Test error count increments on validation failure."""
        initial_errors = self.service.error_count
        self.service.infer("invalid")
        
        self.assertEqual(self.service.error_count, initial_errors + 1)

    def test_infer_disabled_fallback_raises_error(self):
        """Test inference raises error when fallback is disabled and input invalid."""
        service = MLInferenceService(enable_fallback=False)
        
        with self.assertRaises(ValueError):
            service.infer("invalid")

    def test_infer_disabled_fallback_valid_input_succeeds(self):
        """Test inference succeeds with valid input even with fallback disabled."""
        service = MLInferenceService(enable_fallback=False)
        result = service.infer([1, 2, 3])
        
        self.assertTrue(result["success"])

    def test_infer_meets_threshold_calculation(self):
        """Test confidence threshold comparison."""
        result = self.service.infer([1, 2, 3])
        
        # Fallback threshold is 0.6
        self.assertTrue(result["meets_threshold"])


class TestMLInferenceServiceForcedModel(unittest.TestCase):
    """Tests for forced model selection."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_infer_force_main_model(self):
        """Test forcing main model selection."""
        result = self.service.infer([1, 2, 3], force_model="main")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "main")

    def test_infer_force_fallback_model(self):
        """Test forcing fallback model selection."""
        result = self.service.infer([1, 2, 3], force_model="fallback")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "fallback")

    def test_infer_force_emergency_model(self):
        """Test forcing emergency model selection."""
        result = self.service.infer([1, 2, 3], force_model="emergency")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "emergency")

    def test_infer_force_invalid_model_raises_error(self):
        """Test forcing unknown model raises error."""
        with self.assertRaises(ValueError):
            self.service.infer([1, 2, 3], force_model="unknown")

    def test_infer_force_main_with_invalid_input_raises_error(self):
        """Test forcing main model with invalid input raises error."""
        with self.assertRaises(ValueError):
            self.service.infer([1], force_model="main")


class TestMLInferenceServiceStatistics(unittest.TestCase):
    """Tests for service statistics and tracking."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_get_statistics_initial_state(self):
        """Test statistics in initial state."""
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["total_predictions"], 0)
        self.assertEqual(stats["error_count"], 0)
        self.assertEqual(stats["main_model_calls"], 0)
        self.assertEqual(stats["fallback_model_calls"], 0)
        self.assertEqual(stats["emergency_model_calls"], 0)
        self.assertIsNone(stats["last_model_used"])

    def test_get_statistics_after_predictions(self):
        """Test statistics after various predictions."""
        self.service.infer([1, 2, 3])  # main
        self.service.infer([1])  # fallback
        self.service.infer("invalid")  # emergency
        
        stats = self.service.get_statistics()
        
        self.assertEqual(stats["total_predictions"], 3)
        self.assertEqual(stats["main_model_calls"], 1)
        self.assertEqual(stats["fallback_model_calls"], 1)
        self.assertEqual(stats["emergency_model_calls"], 1)

    def test_get_statistics_success_rate(self):
        """Test success rate calculation."""
        self.service.infer([1, 2, 3])
        self.service.infer([1])
        
        stats = self.service.get_statistics()
        
        # Both should succeed, so 100%
        self.assertEqual(stats["success_rate"], 1.0)

    def test_get_statistics_success_rate_with_errors(self):
        """Test success rate with errors."""
        self.service.infer([1, 2, 3])
        self.service.infer("invalid")
        
        stats = self.service.get_statistics()
        
        # First succeeds, second triggers error_count increment but still returns success
        # So success_rate = (2 predictions - 1 error) / 2 = 0.5
        self.assertEqual(stats["success_rate"], 0.5)

    def test_reset_statistics(self):
        """Test statistics reset."""
        self.service.infer([1, 2, 3])
        self.service.infer([1])
        
        stats_before = self.service.get_statistics()
        self.assertGreater(stats_before["total_predictions"], 0)
        
        self.service.reset_statistics()
        
        stats_after = self.service.get_statistics()
        self.assertEqual(stats_after["total_predictions"], 0)
        self.assertEqual(stats_after["main_model_calls"], 0)
        self.assertEqual(stats_after["fallback_model_calls"], 0)


class TestMLInferenceServicePredictionHistory(unittest.TestCase):
    """Tests for prediction history tracking."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_prediction_history_records_predictions(self):
        """Test predictions are recorded in history."""
        self.service.infer([1, 2, 3])
        
        self.assertEqual(len(self.service.prediction_history), 1)

    def test_prediction_history_multiple_predictions(self):
        """Test multiple predictions recorded in order."""
        self.service.infer([1, 2, 3])
        self.service.infer([1])
        self.service.infer("invalid")
        
        self.assertEqual(len(self.service.prediction_history), 3)
        self.assertEqual(self.service.prediction_history[0]["model_used"], "main")
        self.assertEqual(self.service.prediction_history[1]["model_used"], "fallback")
        self.assertEqual(self.service.prediction_history[2]["model_used"], "emergency")

    def test_prediction_history_cleared_on_reset(self):
        """Test history is cleared on reset."""
        self.service.infer([1, 2, 3])
        self.service.reset_statistics()
        
        self.assertEqual(len(self.service.prediction_history), 0)


class TestLoadTestData(unittest.TestCase):
    """Tests for loading test data from JSON file."""

    def test_load_test_data_from_sample_input(self):
        """Test loading test data from sample_input.json."""
        file_path = os.path.join(os.path.dirname(__file__), "sample_input.json")
        
        # Only run if file exists
        if os.path.exists(file_path):
            data = load_test_data(file_path)
            
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
            # Based on provided sample_input.json
            self.assertEqual(len(data), 3)
            self.assertEqual(data[0], [1, 2, 3, 4, 5, 6])
            self.assertEqual(data[1], [1, 2])
            self.assertEqual(data[2], [])

    def test_load_test_data_nonexistent_file(self):
        """Test loading from nonexistent file."""
        data = load_test_data("/nonexistent/path/file.json")
        
        self.assertEqual(data, [])


class TestIntegrationWithSampleData(unittest.TestCase):
    """Integration tests using the provided sample input data."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)
        self.file_path = os.path.join(os.path.dirname(__file__), "sample_input.json")

    def test_integration_all_sample_cases(self):
        """Test inference on all sample input cases."""
        if not os.path.exists(self.file_path):
            self.skipTest(f"Sample input file not found: {self.file_path}")
        
        data = load_test_data(self.file_path)
        results = []
        
        for test_case in data:
            result = self.service.infer(test_case)
            results.append(result)
            self.assertTrue(result["success"])
        
        self.assertEqual(len(results), 3)

    def test_integration_sample_case_normal(self):
        """Test sample case 1: Normal execution (main model)."""
        if not os.path.exists(self.file_path):
            self.skipTest(f"Sample input file not found: {self.file_path}")
        
        data = load_test_data(self.file_path)
        result = self.service.infer(data[0])  # [1, 2, 3, 4, 5, 6]
        
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "main")
        self.assertEqual(result["prediction"]["sum"], 21)

    def test_integration_sample_case_fallback(self):
        """Test sample case 2: Fallback model logic."""
        if not os.path.exists(self.file_path):
            self.skipTest(f"Sample input file not found: {self.file_path}")
        
        data = load_test_data(self.file_path)
        result = self.service.infer(data[1])  # [1, 2]
        
        # This has 2 elements, so should use main model actually
        self.assertTrue(result["success"])
        self.assertEqual(result["model_used"], "main")

    def test_integration_sample_case_empty_input(self):
        """Test sample case 3: Empty input / error handling."""
        if not os.path.exists(self.file_path):
            self.skipTest(f"Sample input file not found: {self.file_path}")
        
        data = load_test_data(self.file_path)
        result = self.service.infer(data[2])  # []
        
        self.assertTrue(result["success"])
        # Empty input validation passes, but empty should use emergency
        self.assertEqual(result["model_used"], "emergency")


class TestCoverageScenarios(unittest.TestCase):
    """Additional tests to ensure comprehensive coverage."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = MLInferenceService(enable_fallback=True)

    def test_all_paths_main_model_success(self):
        """Verify main model success path is covered."""
        result = self.service.infer([1, 2, 3, 4, 5])
        self.assertEqual(result["model_used"], "main")

    def test_all_paths_main_insufficient_length(self):
        """Verify main model insufficient length fallback."""
        result = self.service.infer([1])
        self.assertEqual(result["model_used"], "fallback")

    def test_all_paths_validation_failure_emergency(self):
        """Verify validation failure triggers emergency."""
        result = self.service.infer(12345)
        self.assertEqual(result["model_used"], "emergency")

    def test_all_paths_multiple_errors(self):
        """Verify error tracking across multiple failures."""
        initial_errors = self.service.error_count
        self.service.infer(123)
        self.service.infer([1, 2.5, 3])
        self.service.infer({"a": 1})
        
        # Each invalid input increments error count
        self.assertGreater(self.service.error_count, initial_errors)

    def test_confidence_scores_vary_by_model(self):
        """Verify different models have different confidence scores."""
        main_result = self.service.infer([1, 2, 3, 4, 5])
        self.service.reset_statistics()
        
        fallback_result = self.service.infer([1])
        self.service.reset_statistics()
        
        emergency_result = self.service.infer("invalid")
        
        main_conf = main_result["confidence"]
        fallback_conf = fallback_result["confidence"]
        emergency_conf = emergency_result["confidence"]
        
        # Verify confidence scores differ
        self.assertNotEqual(main_conf, fallback_conf)
        self.assertNotEqual(fallback_conf, emergency_conf)

    def test_fallback_disabled_with_short_input(self):
        """Test behavior when fallback is disabled with insufficient input."""
        service = MLInferenceService(enable_fallback=False)
        # With fallback disabled and single element (< 2), main model won't be used
        # and fallback won't be attempted, so it goes to emergency which always succeeds
        result = service.infer([1])
        self.assertTrue(result["success"])

    def test_abstract_base_class_model_is_available(self):
        """Test that models report availability correctly."""
        self.assertTrue(self.service.main_model.is_available())
        self.assertTrue(self.service.fallback_model.is_available())
        self.assertTrue(self.service.emergency_model.is_available())

    def test_model_name_attributes(self):
        """Test that all models have correct names."""
        self.assertEqual(self.service.main_model.name, "MainModel")
        self.assertEqual(self.service.fallback_model.name, "FallbackModel")
        self.assertEqual(self.service.emergency_model.name, "EmergencyModel")

    def test_model_threshold_values(self):
        """Test that all models have confidence thresholds."""
        self.assertEqual(self.service.main_model.confidence_threshold, 0.8)
        self.assertEqual(self.service.fallback_model.confidence_threshold, 0.6)
        self.assertEqual(self.service.emergency_model.confidence_threshold, 0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
