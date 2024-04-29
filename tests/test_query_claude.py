from utils.query_claude import ai_cleanup


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
