"""Simple model implementations for the inference service.

These are intentionally lightweight and deterministic so unit tests can exercise
main and fallback logic reliably.
"""
from typing import List, Optional, Any


class ModelError(Exception):
    """Raised when a model cannot handle the provided input."""


class MainModel:
    """A mock "main" model which can be configured to fail on short inputs.

    predict returns a dict with the model name and a simple transformation of
    the input so tests can assert which model produced the result.
    """

    def __init__(self, fail_on_length_lt: Optional[int] = None, name: str = "main"):
        self.fail_on_length_lt = fail_on_length_lt
        self.name = name

    def predict(self, data: List[Any]) -> dict:
        if not isinstance(data, (list, tuple)):
            raise TypeError("data must be a list or tuple")

        if self.fail_on_length_lt is not None and len(data) < self.fail_on_length_lt:
            # Simulate an error when the input is below a configured threshold
            raise ModelError("input too short for main model")

        # Deterministic, simple transformation so tests can verify behavior
        return {"model": self.name, "predictions": [x * 2 for x in data]}


class FallbackModel:
    """A simple fallback model that always succeeds and is deterministic."""

    def __init__(self, name: str = "fallback"):
        self.name = name

    def predict(self, data: List[Any]) -> dict:
        if not isinstance(data, (list, tuple)):
            raise TypeError("data must be a list or tuple")

        # Different transformation so tests can detect fallback usage
        return {"model": self.name, "predictions": [x + 1 for x in data]}
