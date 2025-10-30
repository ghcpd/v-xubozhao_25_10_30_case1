import json
import os
import pytest

from src.service import InferenceService, MainModel, FallbackModel

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PATH = os.path.join(os.path.dirname(HERE), 'sample_input.json')


def load_sample_list(index):
    with open(SAMPLE_PATH, 'r') as fh:
        lst = json.load(fh)
    return lst[index]


def test_main_model_success_from_sample_input():
    # Use first array in the sample - length 6, should use main model
    data = load_sample_list(0)
    svc = InferenceService()
    out = svc.infer(data)
    assert out['model'] == 'main'
    assert out['result'] == sum(data)


def test_fallback_by_input_length():
    # Use second array - length 2 (< threshold); fallback model should be used
    data = load_sample_list(1)
    svc = InferenceService()
    out = svc.infer(data)
    assert out['model'] == 'fallback'
    assert out['result'] == len(data)


def test_main_model_failure_then_use_fallback(monkeypatch):
    # Force main model to raise when used
    data = load_sample_list(0)  # length >= threshold
    def broken_predict(d):
        raise RuntimeError("simulated crash")
    svc = InferenceService()
    # Replace main model instance with one that will raise
    svc.main_model.predict = broken_predict
    out = svc.infer(data)
    # Should have used fallback because main raised
    assert out['model'] == 'fallback'
    assert out['result'] == len(data)
    assert 'error' in out


def test_none_input_raises():
    svc = InferenceService()
    with pytest.raises(ValueError):
        svc.infer(None)


def test_empty_input_triggers_main_error_and_fallback():
    # empty input - we pick fallback because main will be chosen but raise
    data = load_sample_list(2)
    svc = InferenceService()
    # ensure main model would have been picked when threshold <= 0
    svc.threshold = 0
    out = svc.infer(data)
    # Because main throws ValueError on empty, fallback should be used
    assert out['model'] == 'fallback'
    assert out['result'] == 0
