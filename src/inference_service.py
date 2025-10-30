"""Inference service that selects between a main model and a fallback model.

The service exercises several fallback paths:
- use fallback when input is below a configurable length threshold
- use fallback when the main model raises an exception
- use fallback when the main model returns None

Unit tests will target each of these branches.
"""
import logging
from typing import List, Any

from .models import ModelError


class InferenceService:
    """Service which routes requests to a main model and falls back when needed.

    Args:
        main_model: object with a predict(data) method
        fallback_model: object with a predict(data) method
        length_threshold: if len(data) < length_threshold a fallback is used
    """

    def __init__(self, main_model, fallback_model, length_threshold: int = 3, logger: logging.Logger = None):
        self.main_model = main_model
        self.fallback_model = fallback_model
        self.length_threshold = length_threshold
        self.logger = logger or logging.getLogger(__name__)

    def predict(self, data: List[Any]) -> dict:
        # Basic validation
        if not isinstance(data, (list, tuple)):
            raise ValueError("input must be a list or tuple")

        if len(data) == 0:
            raise ValueError("empty input is not allowed")

        # Fallback based on input conditions (unmet conditions)
        if len(data) < self.length_threshold:
            self.logger.info("Input length %d < %d; using fallback model", len(data), self.length_threshold)
            return self.fallback_model.predict(data)

        # Try the main model and fall back on exceptions or unexpected results
        try:
            result = self.main_model.predict(data)

            if result is None:
                self.logger.warning("Main model returned None; falling back")
                return self.fallback_model.predict(data)

            return result
        except Exception as exc:  # include ModelError and other runtime errors
            # Log exception and switch to fallback model
            self.logger.exception("Main model failed, falling back: %s", exc)
            return self.fallback_model.predict(data)
