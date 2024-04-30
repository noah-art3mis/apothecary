from utils.query_claude import ai_cleanup
import pytest


def test_claude_improper_message_formatting():
    from utils.query_claude import query_claude, get_model
    from configs import MODEL

    model = get_model(MODEL)

    with pytest.raises(Exception) as e:
        result = query_claude(model, "").content[0].text
        print(result)
        assert not e["error"]


def test_claude_works():
    from utils.query_claude import query_claude, get_model
    from configs import MODEL

    model = get_model(MODEL)

    expected = "THIS IS WORKING"

    assert (
        query_claude(
            model, "respond 'THIS IS WORKING' to this message and nothing else"
        )
        .content[0]
        .text
        == expected
    )


def test_cleanup_spaces_period_comma():
    data = "It  consists  of  those  beliefs which  people  confidently  hold  to  and  live  by  In  particular  the  so ciologist will be concerned with beliefs which are taken for granted or institutionalised,  or invested with authority by groups of people."
    expected = "It consists of those beliefs which people confidently hold to and live by. In particular, the sociologist will be concerned with beliefs which are taken for granted or institutionalised, or invested with authority by groups of people."

    assert ai_cleanup(data, "1") == expected


def test_no_logical_flux_fix():
    data = "There are no limitations which lie in the absolute or transcendent character of scientific knowledge itself, or in the special nature of rationality, validity, truth or objectivity."
    expected = "There are no limitations which lie in the absolute or transcendent character of scientific knowledge itself, or in the special nature of rationality, validity, truth or objectivity."
    assert ai_cleanup(data, "1") == expected


def test_no_uk_fix():
    data = "They all divide behaviour or belief into two types: right and wrong, true or false, rational or irrational."
    expected = "They all divide behaviour or belief into two types: right and wrong, true or false, rational or irrational."
    assert ai_cleanup(data, "1") == expected


def test_word_space():
    data = "Nature will take on a moral signifi cance, endorsing and embodying truth and right. Those who indulge their tendencies to offer asymmetrical explanations will thus have every opportunity to represent as natural what they take for granted. It is an ideal recipe for turning one's gaze away from one's own society, values and beliefs and attending only to deviations from them."
    expected = "Nature will take on a moral significance, endorsing and embodying truth and right. Those who indulge their tendencies to offer asymmetrical explanations will thus have every opportunity to represent as natural what they take for granted. It is an ideal recipe for turning one's gaze away from one's own society, values and beliefs and attending only to deviations from them."
    assert ai_cleanup(data, "1") == expected


def test_ellipses_no_fix():
    data = "Consider the following simple example. A primitive tribesman consults an oracle by administering a herbal substance to a chicken. The chicken dies. The tribesman can clearly see its behaviour and so can we. He says the oracle has answered 'no' to his question. We say the chicken has been poisoned. The same experience impinging on different systems of belief evokes different responses \u2026 There is a social component in all knowledge."
    expected = "Consider the following simple example. A primitive tribesman consults an oracle by administering a herbal substance to a chicken. The chicken dies. The tribesman can clearly see its behaviour and so can we. He says the oracle has answered 'no' to his question. We say the chicken has been poisoned. The same experience impinging on different systems of belief evokes different responses \u2026 There is a social component in all knowledge."
    assert ai_cleanup(data, "1") == expected
