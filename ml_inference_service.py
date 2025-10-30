"""
Machine Learning Inference Service with Dynamic Model Switching and Fallback Logic

This module provides a robust inference service that:
- Dynamically switches between models based on input conditions
- Implements comprehensive fallback logic for error handling
- Supports multiple model backends (main, fallback, emergency)
"""

import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Enum for available model types."""
    MAIN = "main"
    FALLBACK = "fallback"
    EMERGENCY = "emergency"


class Model(ABC):
    """Abstract base class for ML models."""

    def __init__(self, name: str, confidence_threshold: float = 0.7):
        self.name = name
        self.confidence_threshold = confidence_threshold
        self.call_count = 0

    @abstractmethod
    def predict(self, data: List[int]) -> Tuple[Any, float]:
        """
        Generate a prediction from input data.
        
        Args:
            data: Input list of integers
            
        Returns:
            Tuple of (prediction, confidence_score)
        """
        pass

    def is_available(self) -> bool:
        """Check if the model is available."""
        return True


class MainModel(Model):
    """Primary ML model with advanced inference capabilities."""

    def __init__(self):
        super().__init__("MainModel", confidence_threshold=0.8)

    def predict(self, data: List[int]) -> Tuple[Dict[str, Any], float]:
        """
        Advanced prediction using main model.
        
        Args:
            data: Input list of integers
            
        Returns:
            Tuple of (prediction_dict, confidence)
            
        Raises:
            ValueError: If input is empty
        """
        self.call_count += 1
        
        if not data:
            logger.warning("MainModel: Empty input received")
            raise ValueError("Main model requires non-empty input")

        if len(data) < 2:
            logger.warning("MainModel: Insufficient input length")
            raise ValueError("Main model requires at least 2 elements")

        result = {
            "model": "main",
            "sum": sum(data),
            "mean": sum(data) / len(data),
            "count": len(data),
            "max": max(data),
            "min": min(data)
        }
        confidence = min(0.95, 0.7 + len(data) * 0.05)
        
        logger.info(f"MainModel prediction successful: {result}")
        return result, confidence


class FallbackModel(Model):
    """Fallback model for basic inference when main model fails."""

    def __init__(self):
        super().__init__("FallbackModel", confidence_threshold=0.6)

    def predict(self, data: List[int]) -> Tuple[Dict[str, Any], float]:
        """
        Simple prediction using fallback model.
        
        Args:
            data: Input list of integers
            
        Returns:
            Tuple of (prediction_dict, confidence)
        """
        self.call_count += 1
        
        if not data:
            logger.warning("FallbackModel: Empty input received")
            raise ValueError("Fallback model requires non-empty input")

        result = {
            "model": "fallback",
            "sum": sum(data),
            "count": len(data)
        }
        confidence = 0.65
        
        logger.info(f"FallbackModel prediction successful: {result}")
        return result, confidence


class EmergencyModel(Model):
    """Emergency model for graceful degradation with minimal requirements."""

    def __init__(self):
        super().__init__("EmergencyModel", confidence_threshold=0.5)

    def predict(self, data: List[int]) -> Tuple[Dict[str, Any], float]:
        """
        Minimal prediction using emergency model.
        
        Args:
            data: Input list of integers
            
        Returns:
            Tuple of (prediction_dict, confidence)
        """
        self.call_count += 1
        
        logger.info(f"EmergencyModel prediction made for {len(data)} elements")
        result = {
            "model": "emergency",
            "count": len(data)
        }
        confidence = 0.5
        
        return result, confidence


class MLInferenceService:
    """
    Main inference service with dynamic model switching and fallback logic.
    
    This service manages multiple models and automatically switches between them
    based on input conditions and error states.
    """

    def __init__(self, enable_fallback: bool = True):
        """
        Initialize the ML Inference Service.
        
        Args:
            enable_fallback: Whether to enable fallback models
        """
        self.enable_fallback = enable_fallback
        self.main_model = MainModel()
        self.fallback_model = FallbackModel()
        self.emergency_model = EmergencyModel()
        self.last_model_used: Optional[ModelType] = None
        self.prediction_history: List[Dict[str, Any]] = []
        self.error_count = 0

    def _validate_input(self, data: Any) -> bool:
        """
        Validate input data format and constraints.
        
        Args:
            data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, list):
            logger.error(f"Invalid input type: {type(data)}")
            return False

        if len(data) > 100:
            logger.error("Input exceeds maximum length of 100 elements")
            return False

        if not all(isinstance(x, int) for x in data):
            logger.error("All input elements must be integers")
            return False

        return True

    def _should_use_main_model(self, data: List[int]) -> bool:
        """
        Determine if main model should be used.
        
        Args:
            data: Input data
            
        Returns:
            True if main model conditions are met
        """
        return len(data) >= 2

    def infer(self, data: List[int], force_model: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform inference with dynamic model switching and fallback logic.
        
        This is the main entry point that:
        1. Validates input
        2. Attempts to use the main model
        3. Falls back to fallback model if main fails
        4. Uses emergency model if all else fails
        
        Args:
            data: Input list of integers
            force_model: Force a specific model ('main', 'fallback', 'emergency')
            
        Returns:
            Dictionary containing prediction, confidence, and metadata
            
        Raises:
            ValueError: If input validation fails and fallback is disabled
        """
        logger.info(f"Inference request: data_len={len(data) if isinstance(data, list) else 'N/A'}, force_model={force_model}")

        # Validate input
        if not self._validate_input(data):
            self.error_count += 1
            if not self.enable_fallback:
                raise ValueError("Invalid input format and fallback is disabled")
            logger.info("Input validation failed, falling back to emergency model")
            return self._use_emergency_model(data)

        # Force specific model if requested
        if force_model:
            return self._use_forced_model(force_model, data)

        # Normal inference with fallback logic
        return self._infer_with_fallback(data)

    def _infer_with_fallback(self, data: List[int]) -> Dict[str, Any]:
        """
        Perform inference with automatic fallback logic.
        
        Args:
            data: Validated input data
            
        Returns:
            Prediction result dictionary
        """
        # Try main model first
        if self._should_use_main_model(data):
            try:
                result, confidence = self.main_model.predict(data)
                self.last_model_used = ModelType.MAIN
                return self._format_result(result, confidence, ModelType.MAIN)
            except (ValueError, Exception) as e:
                logger.warning(f"Main model failed: {str(e)}")
                self.error_count += 1

        # Fallback to fallback model
        if self.enable_fallback:
            try:
                result, confidence = self.fallback_model.predict(data)
                self.last_model_used = ModelType.FALLBACK
                return self._format_result(result, confidence, ModelType.FALLBACK)
            except (ValueError, Exception) as e:
                logger.warning(f"Fallback model failed: {str(e)}")
                self.error_count += 1

        # Final fallback to emergency model
        return self._use_emergency_model(data)

    def _use_forced_model(self, model_name: str, data: List[int]) -> Dict[str, Any]:
        """
        Use a specific model by name.
        
        Args:
            model_name: Name of the model to use
            data: Input data
            
        Returns:
            Prediction result dictionary
            
        Raises:
            ValueError: If model not found or fails
        """
        try:
            if model_name == "main":
                result, confidence = self.main_model.predict(data)
                self.last_model_used = ModelType.MAIN
                return self._format_result(result, confidence, ModelType.MAIN)
            elif model_name == "fallback":
                result, confidence = self.fallback_model.predict(data)
                self.last_model_used = ModelType.FALLBACK
                return self._format_result(result, confidence, ModelType.FALLBACK)
            elif model_name == "emergency":
                result, confidence = self.emergency_model.predict(data)
                self.last_model_used = ModelType.EMERGENCY
                return self._format_result(result, confidence, ModelType.EMERGENCY)
            else:
                raise ValueError(f"Unknown model: {model_name}")
        except Exception as e:
            logger.error(f"Forced model '{model_name}' failed: {str(e)}")
            raise

    def _use_emergency_model(self, data: List[int]) -> Dict[str, Any]:
        """
        Use emergency model for graceful degradation.
        
        Args:
            data: Input data (may be invalid)
            
        Returns:
            Prediction result dictionary
        """
        try:
            # Handle empty or invalid data gracefully
            if not isinstance(data, list):
                data = []
            
            result, confidence = self.emergency_model.predict(data)
            self.last_model_used = ModelType.EMERGENCY
            return self._format_result(result, confidence, ModelType.EMERGENCY)
        except Exception as e:
            logger.error(f"Emergency model also failed: {str(e)}")
            return {
                "success": False,
                "error": "All models failed",
                "error_message": str(e),
                "model_used": "none"
            }

    def _format_result(self, result: Dict[str, Any], confidence: float, model_type: ModelType) -> Dict[str, Any]:
        """
        Format the prediction result.
        
        Args:
            result: Raw prediction result
            confidence: Confidence score
            model_type: Type of model used
            
        Returns:
            Formatted result dictionary
        """
        formatted = {
            "success": True,
            "prediction": result,
            "confidence": confidence,
            "model_used": model_type.value,
            "meets_threshold": confidence >= self.fallback_model.confidence_threshold
        }
        self.prediction_history.append(formatted)
        return formatted

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get service statistics.
        
        Returns:
            Dictionary containing service statistics
        """
        return {
            "total_predictions": len(self.prediction_history),
            "error_count": self.error_count,
            "main_model_calls": self.main_model.call_count,
            "fallback_model_calls": self.fallback_model.call_count,
            "emergency_model_calls": self.emergency_model.call_count,
            "last_model_used": self.last_model_used.value if self.last_model_used else None,
            "success_rate": (len(self.prediction_history) - self.error_count) / max(1, len(self.prediction_history)) if self.prediction_history else 0
        }

    def reset_statistics(self):
        """Reset service statistics."""
        self.prediction_history.clear()
        self.error_count = 0
        self.main_model.call_count = 0
        self.fallback_model.call_count = 0
        self.emergency_model.call_count = 0
        self.last_model_used = None


def load_test_data(file_path: str) -> List[List[int]]:
    """
    Load test data from JSON file.
    
    Args:
        file_path: Path to JSON file containing test data
        
    Returns:
        List of test data arrays
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} test cases from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Failed to load test data: {str(e)}")
        return []
