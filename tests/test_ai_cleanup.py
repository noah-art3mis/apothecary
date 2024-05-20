from utils.query_llm import ai_cleanup
import pytest


@pytest.fixture
def file_handler(log=[]):

    yield log

    # with open("tests/test_logs.json", "w") as file:
    #     json.dump(log, file, indent=2)


def test_cleanup_spaces_period_comma(file_handler):
    data = "It  consists  of  those  beliefs which  people  confidently  hold  to  and  live  by  In  particular  the  so ciologist will be concerned with beliefs which are taken for granted or institutionalised,  or invested with authority by groups of people."
    expected = "It consists of those beliefs which people confidently hold to and live by. In particular, the sociologist will be concerned with beliefs which are taken for granted or institutionalised, or invested with authority by groups of people."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_no_logical_flux_fix(file_handler):
    data = "There are no limitations which lie in the absolute or transcendent character of scientific knowledge itself, or in the special nature of rationality, validity, truth or objectivity."
    expected = "There are no limitations which lie in the absolute or transcendent character of scientific knowledge itself, or in the special nature of rationality, validity, truth or objectivity."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_no_uk_fix(file_handler):
    data = "They all divide behaviour or belief into two types: right and wrong, true or false, rational or irrational."
    expected = "They all divide behaviour or belief into two types: right and wrong, true or false, rational or irrational."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_word_space(file_handler):
    data = "Nature will take on a moral signifi cance, endorsing and embodying truth and right. Those who indulge their tendencies to offer asymmetrical explanations will thus have every opportunity to represent as natural what they take for granted. It is an ideal recipe for turning one's gaze away from one's own society, values and beliefs and attending only to deviations from them."
    expected = "Nature will take on a moral significance, endorsing and embodying truth and right. Those who indulge their tendencies to offer asymmetrical explanations will thus have every opportunity to represent as natural what they take for granted. It is an ideal recipe for turning one's gaze away from one's own society, values and beliefs and attending only to deviations from them."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_unicode(file_handler):
    data = "This would be a cogent objection against any theory that did in deed assert that existential determination implied falsity But its premise should be challenged \u00b7for what it is: a gratuitous assumption and an unrealistic demand. If knowledge does depend on a vantage point outside society and if truth does depend on stepping above the causal nexus of social relations, then we may give them up as lost"
    expected = "This would be a cogent objection against any theory that did indeed assert that existential determination implied falsity. But its premise should be challenged for what it is: a gratuitous assumption and an unrealistic demand. If knowledge does depend on a vantage point outside society and if truth does depend on stepping above the causal nexus of social relations, then we may give them up as lost."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_artifacts(file_handler):
    data = "This praise f<;>r experience as a source of knowledge can be seen as encouraging individuals to rely on their own physical and psycholog ical resources for getting to know the world."
    expected = "This praise for experience as a source of knowledge can be seen as encouraging individuals to rely on their own physical and psychological resources for getting to know the world."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_punctuation_0(file_handler):
    data = "Experience as interpreted by the theory is monitored for such internal consistency as is felt important The process of judging a theory is an internal one"
    expected = "Experience as interpreted by the theory is monitored for such internal consistency as is felt important. The process of judging a theory is an internal one."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_artifact2(file_handler):
    data = "It is now possible to see why the relation ()f correspondence between a theory and reality is vague."
    expected = "It is now possible to see why the relation of correspondence between a theory and reality is vague."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_quotes(file_handler):
    data = r"why should\" the sacred character of scientific knowledge be threatened by a so ciological scrutiny? The answer lies in a further articulation of the idea of the sacred. Religion is essentially a source of strength. When people commu nicate with their gods they are fortified, elevated and protected."
    expected = r"Why should the sacred character of scientific knowledge be threatened by a sociological scrutiny? The answer lies in a further articulation of the idea of the sacred. Religion is essentially a source of strength. When people communicate with their gods they are fortified, elevated and protected."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_colon(file_handler):
    data = "The threat posed by the sociology of knowledge is precisely this it appears to reverse or interfere with the outward flow of energy and inspiration which derives from contact with the basic truths and principles of science and methodology."
    expected = "The threat posed by the sociology of knowledge is precisely this: it appears to reverse or interfere with the outward flow of energy and inspiration which derives from contact with the basic truths and principles of science and methodology."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_l_i(file_handler):
    data = "So far l have only offered an explanation that would apply to scientific enthusiasts."
    expected = "So far I have only offered an explanation that would apply to scientific enthusiasts."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_l_1(file_handler):
    data = "So far 1 have only offered an explanation that would apply to scientific enthusiasts."
    expected = "So far I have only offered an explanation that would apply to scientific enthusiasts."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_remove_from_front(file_handler):
    data = "to As with Popper's work, Kuhn's account of science has a definite flavour which is at least partly caused by the metaphors which the author finds it natural to use. Scientists form a 'community' of practitioners."
    expected = "As with Popper's work, Kuhn's account of science has a definite flavour which is at least partly caused by the metaphors which the author finds it natural to use. Scientists form a 'community' of practitioners."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_capitalize(file_handler):
    data = "the clash between Popper and Kuhn represents an almost pure case of the opposition between what may be called the Enlightenment and Romantic ideologies."
    expected = "The clash between Popper and Kuhn represents an almost pure case of the opposition between what may be called the Enlightenment and Romantic ideologies."

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected


def test_(file_handler):
    data = "information ... This apparatus of scholarly commentary and interpretation unavoidably mediates our grasp of the past. It is a formidable and extensive apparatus. In due proportion to its size is its scope for imposing the standards and preoccupations of the present on to the past. Indeed some such imposition is a neces sary feature of all understanding. The only question is: what standards shall be imposed and what concerns will govern the work which is put into the manufacture of our sense of the past? ... If historians should desire to show the cumulative character of mathematics then their interpretive apparatus will enable them to do so. Counterexamples to this vision of progress will become periods of slow development or deviation into error or wrong turnings. Instead of alternatives being exhibited the task becomes one of sorting out the wheat from the chaff. ... historians ... It would be unjust and too simple to say that in such accounts history had been falsified. No standards of integrity or scholarly in Indeed such virtues are impressively and dustry are violated. abundantly evident. Rather it should be said that these virtues are all employed in the interests of an overall progressivist vision, and it is this which must be challenged."
    expected = "information ... This apparatus of scholarly commentary and interpretation unavoidably mediates our grasp of the past. It is a formidable and extensive apparatus. In due proportion to its size is its scope for imposing the standards and preoccupations of the present onto the past. Indeed some such imposition is a necessary feature of all understanding. The only question is: what standards shall be imposed and what concerns will govern the work which is put into the manufacture of our sense of the past? ... If historians should desire to show the cumulative character of mathematics then their interpretive apparatus will enable them to do so. Counterexamples to this vision of progress will become periods of slow development or deviation into error or wrong turnings. Instead of alternatives being exhibited the task becomes one of sorting out the wheat from the chaff. ... historians ... It would be unjust and too simple to say that in such accounts history had been falsified. No standards of integrity or scholarly industry are violated. Indeed such virtues are impressively and abundantly evident. Rather it should be said that these virtues are all employed in the interests of an overall progressivist vision, and it is this which must be challenged"

    result, _ = ai_cleanup(data)
    log = {"data": data, "expected": expected, "result": result}
    file_handler.append(log)
    assert result == expected
