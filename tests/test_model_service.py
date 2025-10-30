import json
import os
import pytest

# Ensure the repository root is on sys.path so tests can import local modules
import os, sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from model_service import InferenceService, MainModel, FallbackModel

SAMPLE = os.path.join(ROOT, 'sample_input.json')


def load_sample():
    with open(SAMPLE, 'r') as f:
        return json.load(f)


def test_main_model_success():
    data = load_sample()[0]  # [1,2,3,4,5,6]
    svc = InferenceService()
    res = svc.predict(data)
    assert res['model'] == 'main'
    assert res['value'] == sum(data)


def test_fallback_model_used_for_short_input():
    data = load_sample()[1]  # [1,2] => main will raise insufficient data
    svc = InferenceService()
    res = svc.predict(data)
    assert res['model'] == 'fallback'
    assert pytest.approx(res['value'], rel=1e-6) == sum(data) / len(data)


def test_empty_input_raises():
    data = load_sample()[2]  # []
    svc = InferenceService()
    with pytest.raises(ValueError):
        svc.predict(data)


def test_main_exception_triggers_fallback():
    # Create a MainModel that raises for any negative values
    class BrokenMain(MainModel):
        def predict(self, data):
            raise RuntimeError("forced failure")

    svc = InferenceService(main_model=BrokenMain(), fallback_model=FallbackModel())
    data = [10, 20]
    res = svc.predict(data)
    assert res['model'] == 'fallback'


def test_fallback_raises_on_empty():
    # Directly call fallback to assert it raises on empty list
    fb = FallbackModel()
    with pytest.raises(ValueError):
        fb.predict([])


def test_main_model_negative_raises():
    mm = MainModel()
    with pytest.raises(RuntimeError):
        mm.predict([1, -1, 3])


def test_main_model_empty_raises():
    mm = MainModel()
    with pytest.raises(ValueError):
        mm.predict([])


def test_cli_module_runs_and_outputs(tmp_path, capsys):
    # Run the module as a script against sample_input.json to exercise __main__ block
    import runpy
    import sys
    from io import StringIO

    script = os.path.join(ROOT, 'model_service.py')
    sample = os.path.join(ROOT, 'sample_input.json')

    # Replace argv and capture stdout
    old_argv = sys.argv[:]
    old_stdout = sys.stdout
    try:
        sys.argv = [script, sample]
        sys.stdout = StringIO()
        runpy.run_path(script, run_name='__main__')
        out = sys.stdout.getvalue().strip()
    finally:
        sys.argv = old_argv
        sys.stdout = old_stdout

    # The sample has three items. We expect at least two valid outputs and one error for []
    assert 'main' in out or 'fallback' in out
    assert 'error' in out or 'Empty input' in out


def test_cli_no_args_raises_usage(capsys):
    # Simulate running the script without args to hit the usage path that calls sys.exit(1)
    import runpy
    import sys
    from io import StringIO

    script = os.path.join(ROOT, 'model_service.py')
    old_argv = sys.argv[:]
    old_stdout = sys.stdout
    try:
        sys.argv = [script]
        sys.stdout = StringIO()
        with pytest.raises(SystemExit) as se:
            runpy.run_path(script, run_name='__main__')
        assert se.value.code == 1
        out = sys.stdout.getvalue()
        assert 'Usage: python model_service.py' in out
    finally:
        sys.argv = old_argv
        sys.stdout = old_stdout


def test_inference_uses_fallback_on_negative_values():
    data = [1, -1, 3]
    svc = InferenceService()
    res = svc.predict(data)
    # fallback returns mean; main would raise RuntimeError for negative values
    assert res['model'] == 'fallback'
    assert pytest.approx(res['value'], rel=1e-12) == sum(data) / len(data)
