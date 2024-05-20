from utils.query_llm import get_model
import pytest


def test_opus():
    assert get_model("opus") == "claude-3-opus-20240229"


def test_sonnet():
    assert get_model("sonnet") == "claude-3-sonnet-20240229"


def test_haiku():
    assert get_model("haiku") == "claude-3-haiku-20240307"

def test_opus():
    assert get_model("gpt4o") == "gpt4o"


def test_not_found():
    with pytest.raises(ValueError) as e:
        get_model("unknown")
        assert e.type == ValueError
