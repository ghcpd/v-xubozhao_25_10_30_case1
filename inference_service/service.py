import json
from typing import List, Any


class MainModelError(Exception):
    pass


class MainModel:
    """A dummy main model that succeeds for sequences of length >=3 and raises for shorter inputs."""

    def predict(self, inputs: List[int]) -> dict:
        if not isinstance(inputs, list):
            raise MainModelError("Invalid input type")
        if len(inputs) < 3:
            raise MainModelError("Insufficient length for MainModel")
        # pretend to do inference
        return {"model": "main", "sum": sum(inputs), "count": len(inputs)}


class FallbackModel:
    """A simple fallback model that handles short sequences and empty inputs."""

    def predict(self, inputs: List[int]) -> dict:
        if not isinstance(inputs, list):
            return {"model": "fallback", "error": "invalid_type"}
        if len(inputs) == 0:
            return {"model": "fallback", "result": None, "reason": "empty_input"}
        # handle short sequences
        return {"model": "fallback", "sum": sum(inputs), "count": len(inputs)}


class InferenceService:
    def __init__(self, main_model=None, fallback_model=None):
        self.main = main_model or MainModel()
        self.fallback = fallback_model or FallbackModel()

    def infer(self, input_data: Any) -> dict:
        """Attempts to use main model; on failure uses fallback.

        input_data is expected to be a list of ints. Caller may pass raw JSON string or Python object.
        """
        # normalize JSON string input
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError:
                return {"error": "invalid_json"}

        # Validate structure: accept list or raise
        if not isinstance(input_data, list):
            return {"error": "invalid_input_type"}

        # Try main model
        try:
            return self.main.predict(input_data)
        except MainModelError as e:
            # fallback path
            return self.fallback.predict(input_data)


def load_sample(file_path: str) -> List[Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import sys

    svc = InferenceService()
    if len(sys.argv) < 2:
        print("Usage: service.py <input.json>")
        sys.exit(2)
    samples = load_sample(sys.argv[1])
    for s in samples:
        print(svc.infer(s))
