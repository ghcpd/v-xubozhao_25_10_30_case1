import logging
from typing import List, Any

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MainModel:
    """Primary model. For demonstration, it requires at least 3 numeric values.
    If input length < 3 or any negative value found, it raises an exception.
    """

    def predict(self, data: List[float]) -> Any:
        logger.debug("MainModel.predict called with data: %s", data)
        if not data:
            raise ValueError("No input data")
        if any(x < 0 for x in data):
            raise RuntimeError("Main model failure: negative value encountered")
        if len(data) < 3:
            raise RuntimeError("Insufficient data for MainModel")
        # Example output: sum of values
        result = sum(data)
        logger.debug("MainModel result: %s", result)
        return {"model": "main", "value": result}

class FallbackModel:
    """Fallback model used when main model fails or is inappropriate.
    For demonstration, it can work with 1+ values and returns mean. Empty list raises ValueError.
    """

    def predict(self, data: List[float]) -> Any:
        logger.debug("FallbackModel.predict called with data: %s", data)
        if not data:
            raise ValueError("No input data for fallback")
        result = sum(data) / len(data)
        logger.debug("FallbackModel result: %s", result)
        return {"model": "fallback", "value": result}

class InferenceService:
    def __init__(self, main_model=None, fallback_model=None):
        self.main = main_model or MainModel()
        self.fallback = fallback_model or FallbackModel()

    def predict(self, data: List[float]) -> Any:
        logger.debug("InferenceService.predict called with data of length %d", len(data))
        if not data:
            logger.debug("Empty input received")
            raise ValueError("Empty input not allowed")
        try:
            return self.main.predict(data)
        except Exception as e:
            logger.warning("Main model failed with %s. Trying fallback.", e)
            return self.fallback.predict(data)

# Allow module quick test
if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) < 2:
        print("Usage: python model_service.py <json-file>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    svc = InferenceService()
    for item in data:
        try:
            print(svc.predict(item))
        except Exception as e:
            print({"error": str(e)})
