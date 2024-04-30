import pytest
from utils.query_claude import query_claude, get_model
from configs import MODEL


def test_claude_improper_message_formatting():

    model = get_model(MODEL)

    with pytest.raises(Exception) as e:
        result = query_claude(model, "").content[0].text
        assert e
        assert "Error code:" in result


def test_claude_works():

    model = get_model(MODEL)
    message = "respond 'THIS IS WORKING' to this message and nothing else"
    expected = "THIS IS WORKING"

    assert query_claude(model, message).content[0].text == expected
