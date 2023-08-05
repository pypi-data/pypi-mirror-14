import pytest
from ejudge import io
from iospec import parse_string, iotypes


@pytest.fixture
def iospec():
    return parse_string(
        'name: <foo>\n'
        'hello foo!\n'
        '\n'
        'name: <bar>\n'
        'hello bar!'
    )


@pytest.fixture
def src_ok():
    return (
        'name = input("name: ")\n'
        'print("hello %s!" % name)'
    )


@pytest.fixture
def src_bad():
    return (
        'name = input("name: ")\n'
        'print("hello %s." % name)'
    )


def test_simple_case_success_run(src_ok):
    tree = io.run(src_ok, ['foo'], lang='python', sandbox=False)
    case = tree[0]
    assert tree
    assert len(tree) == 1
    assert case[0] == 'name: '
    assert case[1] == 'foo'
    assert case[2] == 'hello foo!'


def test_simple_case_success_timeout(src_ok):
    tree = io.run(src_ok, ['foo'], lang='python', timeout=0.5, sandbox=False)
    case = tree[0]
    assert len(tree) == 1
    assert case[0] == 'name: '
    assert case[1] == 'foo'
    assert case[2] == 'hello foo!'


def test_simple_case_success_sandbox(src_ok):
    tree = io.run(src_ok, ['foo'], lang='python', sandbox=True)
    case = tree[0]
    assert len(tree) == 1
    assert case[0] == 'name: '
    assert case[1] == 'foo'
    assert case[2] == 'hello foo!'


def test_grading_correct_answer(iospec, src_ok):
    feedback = io.grade(src_ok, iospec, lang='python', sandbox=False)
    assert isinstance(feedback.answer_key, iotypes.LinearNode)
    assert isinstance(feedback.case, iotypes.LinearNode)
    assert feedback.grade == 1
    assert feedback.message is None
    assert feedback.status == 'ok'


def test_grading_incorrect_answer(iospec, src_bad):
    feedback = io.grade(src_bad, iospec, lang='python', sandbox=False)
    assert feedback.grade == 0
    assert feedback.status == 'wrong-answer'
    assert feedback.title == 'Wrong Answer'


def test_python_script_run(src_ok):
    tree = io.run(src_ok, ['foo'], lang='python3', sandbox=False)
    tree.pprint()
    case = tree[0]
    assert len(tree) == 1
    assert case[0] == 'name: '
    assert case[1] == 'foo'
    assert case[2] == 'hello foo!'


if __name__ == '__main__':
    pytest.main('test_io_grader_python.py')
