import json
import os
from pathlib import Path
from unittest.mock import Mock

import pytest

import logging

from src.models import MainModel, FallbackModel, ModelError
from src.inference_service import InferenceService


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_INPUT = REPO_ROOT / "sample_input.json"


def load_sample_inputs():
    with open(SAMPLE_INPUT, "r", encoding="utf-8") as fh:
        return json.load(fh)


def test_main_model_used_for_large_input():
    data = load_sample_inputs()[0]

    # Main model should handle this input (length >= 3)
    main = MainModel(fail_on_length_lt=3)
    fallback = Mock(spec=FallbackModel)

    service = InferenceService(main, fallback, length_threshold=3)
    result = service.predict(data)

    assert isinstance(result, dict)
    assert result["model"] == "main"
    # Fallback should not have been called
    fallback.predict.assert_not_called()


def test_fallback_used_for_short_input_without_calling_main():
    data = load_sample_inputs()[1]  # short input

    main = Mock(spec=MainModel)
    fallback = Mock(spec=FallbackModel)
    fallback.predict.return_value = {"model": "fallback", "predictions": [x + 1 for x in data]}

    service = InferenceService(main, fallback, length_threshold=3)
    result = service.predict(data)

    # Because the input is short, main should not be called and fallback should be used
    main.predict.assert_not_called()
    fallback.predict.assert_called_once_with(data)
    assert result["model"] == "fallback"


def test_fallback_used_when_main_raises_exception():
    data = load_sample_inputs()[0]

    main = Mock(spec=MainModel)
    main.predict.side_effect = RuntimeError("main model crashed")

    fallback = Mock(spec=FallbackModel)
    fallback.predict.return_value = {"model": "fallback", "predictions": [x + 1 for x in data]}

    service = InferenceService(main, fallback, length_threshold=3)
    result = service.predict(data)

    # Main was attempted and raised; fallback should be used
    main.predict.assert_called_once_with(data)
    fallback.predict.assert_called_once_with(data)
    assert result["model"] == "fallback"


def test_empty_input_raises_value_error():
    data = load_sample_inputs()[2]  # empty list

    main = MainModel()
    fallback = FallbackModel()
    service = InferenceService(main, fallback, length_threshold=3)

    with pytest.raises(ValueError):
        service.predict(data)


def test_fallback_used_when_main_returns_none():
    data = load_sample_inputs()[0]

    main = Mock(spec=MainModel)
    main.predict.return_value = None

    fallback = Mock(spec=FallbackModel)
    fallback.predict.return_value = {"model": "fallback", "predictions": [x + 1 for x in data]}

    service = InferenceService(main, fallback, length_threshold=3)
    result = service.predict(data)

    main.predict.assert_called_once_with(data)
    fallback.predict.assert_called_once_with(data)
    assert result["model"] == "fallback"


def test_both_models_raising_propagates_exception():
    data = load_sample_inputs()[0]

    main = Mock(spec=MainModel)
    main.predict.side_effect = RuntimeError("main fail")

    fallback = Mock(spec=FallbackModel)
    fallback.predict.side_effect = RuntimeError("fallback fail")

    service = InferenceService(main, fallback, length_threshold=3)

    with pytest.raises(RuntimeError):
        service.predict(data)


def test_invalid_input_type_raises_value_error():
    """Passing a non-list/tuple should raise a ValueError from the service.

    The service validates the input type before calling either model.
    """
    data = "not-a-list"

    main = MainModel()
    fallback = FallbackModel()
    service = InferenceService(main, fallback, length_threshold=3)

    with pytest.raises(ValueError) as excinfo:
        service.predict(data)

    assert "input must be a list or tuple" in str(excinfo.value)


def test_main_model_modelerror_triggers_fallback():
    """If the concrete MainModel raises ModelError the service should fall back."""
    # Use the provided sample inputs (first entry) and configure MainModel to
    # raise ModelError for that length by setting a high fail_on_length_lt.
    data = load_sample_inputs()[0]

    main = MainModel(fail_on_length_lt=100)  # len(data) < 100 -> will raise ModelError
    fallback = Mock(spec=FallbackModel)
    fallback.predict.return_value = {"model": "fallback", "predictions": [x + 1 for x in data]}

    service = InferenceService(main, fallback, length_threshold=3)
    result = service.predict(data)

    # MainModel.predict raised ModelError and fallback was used
    fallback.predict.assert_called_once_with(data)
    assert result["model"] == "fallback"


def test_length_threshold_equal_uses_main():
    """Boundary condition: when len(data) == length_threshold the main model is used."""
    # Build a length-3 input from the provided sample (satisfies requirement to use the sample file)
    data = load_sample_inputs()[0][:3]

    main = Mock(spec=MainModel)
    main.predict.return_value = {"model": "main", "predictions": [x * 2 for x in data]}
    fallback = Mock(spec=FallbackModel)

    service = InferenceService(main, fallback, length_threshold=3)
    result = service.predict(data)

    main.predict.assert_called_once_with(data)
    fallback.predict.assert_not_called()
    assert result["model"] == "main"


def test_logging_on_main_returns_none(caplog):
    """When the main model returns None the service logs a warning and falls back."""
    data = load_sample_inputs()[0]

    main = Mock(spec=MainModel)
    main.predict.return_value = None
    fallback = Mock(spec=FallbackModel)
    fallback.predict.return_value = {"model": "fallback", "predictions": [x + 1 for x in data]}

    logger = logging.getLogger("test_logger_main_none")
    service = InferenceService(main, fallback, length_threshold=3, logger=logger)

    with caplog.at_level(logging.WARNING, logger=logger.name):
        result = service.predict(data)

    assert "Main model returned None; falling back" in caplog.text
    assert result["model"] == "fallback"


def test_logging_on_main_exception(caplog):
    """When the main model raises, the service logs an exception and falls back."""
    data = load_sample_inputs()[0]

    main = Mock(spec=MainModel)
    main.predict.side_effect = ModelError("boom")
    fallback = Mock(spec=FallbackModel)
    fallback.predict.return_value = {"model": "fallback", "predictions": [x + 1 for x in data]}

    logger = logging.getLogger("test_logger_main_exception")
    service = InferenceService(main, fallback, length_threshold=3, logger=logger)

    with caplog.at_level(logging.ERROR, logger=logger.name):
        result = service.predict(data)

    assert "Main model failed, falling back" in caplog.text
    assert result["model"] == "fallback"


def test_models_type_and_transforms():
    """Direct unit tests for MainModel and FallbackModel behavior and type checks."""
    main = MainModel()
    fallback = FallbackModel()

    # Valid transformations
    res_main = main.predict([1, 2, 3])
    assert res_main["model"] == "main"
    assert res_main["predictions"] == [2, 4, 6]

    res_fb = fallback.predict([1, 2, 3])
    assert res_fb["model"] == "fallback"
    assert res_fb["predictions"] == [2, 3, 4]

    # Type checks raise TypeError on wrong input types
    with pytest.raises(TypeError):
        main.predict("not-a-list")

    with pytest.raises(TypeError):
        fallback.predict({"not": "a list"})


def test_both_models_raising_modelerror_propagates():
    """If both the main and fallback models raise ModelError it should propagate."""
    data = load_sample_inputs()[0]

    main = Mock(spec=MainModel)
    main.predict.side_effect = ModelError("main error")

    fallback = Mock(spec=FallbackModel)
    fallback.predict.side_effect = ModelError("fallback error")

    service = InferenceService(main, fallback, length_threshold=3)

    with pytest.raises(ModelError):
        service.predict(data)
