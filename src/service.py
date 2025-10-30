"""
Simple inference service that switches between models based on input.
- MainModel: used when an inner array length >= 3
- FallbackModel: used for short arrays or when main model fails
This repository provides unit tests that cover fallback and error paths.
"""
from typing import List, Any

class MainModel:
    def predict(self, data: List[int]) -> int:
        # Simulate main model behaviour
        if not data:
            # Should raise to simulate failure on empty inputs
            raise ValueError("MainModel cannot handle empty input")
        # Return sum as an example
        return sum(data)

class FallbackModel:
    def predict(self, data: List[int]) -> int:
        # Fallback returns length to indicate it processed the sample
        return len(data)

class InferenceService:
    def __init__(self, main_model: Any = None, fallback_model: Any = None, threshold: int = 3):
        self.main_model = main_model or MainModel()
        self.fallback_model = fallback_model or FallbackModel()
        self.threshold = threshold

    def choose_model(self, data: List[int]):
        if len(data) >= self.threshold:
            return self.main_model, 'main'
        return self.fallback_model, 'fallback'

    def infer(self, data: List[int]) -> dict:
        if data is None:
            raise ValueError("Input data is None")
        model, name = self.choose_model(data)
        try:
            result = model.predict(data)
            return {"model": name, "result": result}
        except Exception as e:
            # On failure of the main model, try fallback
            if name == 'main':
                # Switch to fallback
                result = self.fallback_model.predict(data)
                return {"model": 'fallback', "result": result, "error": str(e)}
            raise
