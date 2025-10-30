import json
import os
import runpy
import sys
import pytest
from inference_service.service import InferenceService, MainModel, FallbackModel, MainModelError


ROOT = os.path.dirname(os.path.dirname(__file__))
SAMPLE = os.path.join(ROOT, "sample_input.json")


def test_main_model_success():
    svc = InferenceService()
    samples = json.load(open(SAMPLE))
    # first sample has 6 items -> main model
    out = svc.infer(samples[0])
    assert out["model"] == "main"
    assert out["count"] == 6
    assert out["sum"] == sum(samples[0])


def test_fallback_for_short_sequence():
    svc = InferenceService()
    samples = json.load(open(SAMPLE))
    # second sample has length 2, main model should raise and fallback used
    out = svc.infer(samples[1])
    assert out["model"] == "fallback"
    assert out["count"] == 2
    assert out["sum"] == sum(samples[1])


def test_fallback_for_empty_sequence():
    svc = InferenceService()
    samples = json.load(open(SAMPLE))
    out = svc.infer(samples[2])
    assert out["model"] == "fallback"
    assert out.get("result") is None
    assert out.get("reason") == "empty_input"


def test_invalid_json_string():
    svc = InferenceService()
    out = svc.infer("{not:valid}")
    assert out == {"error": "invalid_json"}


def test_invalid_type_input():
    svc = InferenceService()
    out = svc.infer({"a": 1})
    assert out == {"error": "invalid_input_type"}


def test_main_model_error_propagation_and_fallback():
    # Create a MainModel that always raises to exercise fallback path
    class BrokenMain:
        def predict(self, inputs):
            raise MainModelError("fail")

    svc = InferenceService(main_model=BrokenMain(), fallback_model=FallbackModel())
    out = svc.infer([9])
    assert out["model"] == "fallback"


def test_mainmodel_predict_invalid_type_raises():
    m = MainModel()
    try:
        m.predict({"a": 1})
        raised = False
    except MainModelError:
        raised = True
    assert raised


def test_fallbackmodel_predict_invalid_type_returns_error():
    f = FallbackModel()
    out = f.predict({"a": 1})
    assert out == {"model": "fallback", "error": "invalid_type"}


def test_infer_json_decodes_to_nonlist_returns_invalid_input_type():
    svc = InferenceService()
    # valid JSON but not a list
    out = svc.infer('{"a": 1}')
    assert out == {"error": "invalid_input_type"}


def test_load_sample_and_cli_execution(tmp_path, capsys):
    # ensure load_sample reads the file and the CLI prints outputs for each sample
    from inference_service.service import load_sample
    root = os.path.dirname(os.path.dirname(__file__))
    sample = os.path.join(root, "sample_input.json")
    data = load_sample(sample)
    assert isinstance(data, list)

    # Run the module as a script in-process to exercise the __main__ block and allow coverage to track it
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["inference_service.service", sample]
        # Ensure module is not present to avoid RuntimeWarning from runpy
        sys.modules.pop("inference_service.service", None)
        sys.modules.pop("inference_service", None)
        runpy.run_module("inference_service.service", run_name="__main__")
    finally:
        sys.argv = orig_argv
    # captured output from pytest capture should include printed dicts; use capsys via pytest to re-run and capture
    # run again but capture stdout programmatically
    from io import StringIO
    old_stdout = sys.stdout
    try:
        sys.stdout = StringIO()
        sys.argv = ["inference_service.service", sample]
        sys.modules.pop("inference_service.service", None)
        sys.modules.pop("inference_service", None)
        runpy.run_module("inference_service.service", run_name="__main__")
        out = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        sys.argv = orig_argv
    assert "model" in out


def test_cli_no_args_returns_usage():
    root = os.path.dirname(os.path.dirname(__file__))
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["inference_service.service"]
        sys.modules.pop("inference_service.service", None)
        sys.modules.pop("inference_service", None)
        with pytest.raises(SystemExit) as se:
            runpy.run_module("inference_service.service", run_name="__main__")
        assert se.value.code == 2
    finally:
        sys.argv = orig_argv

    # Capture printed usage text
    from io import StringIO
    old_stdout = sys.stdout
    try:
        buf = StringIO()
        sys.stdout = buf
        sys.argv = ["inference_service.service"]
        sys.modules.pop("inference_service.service", None)
        sys.modules.pop("inference_service", None)
        with pytest.raises(SystemExit):
            runpy.run_module("inference_service.service", run_name="__main__")
        printed = buf.getvalue()
    finally:
        sys.stdout = old_stdout
        sys.argv = orig_argv
    assert "Usage: service.py <input.json>" in printed
