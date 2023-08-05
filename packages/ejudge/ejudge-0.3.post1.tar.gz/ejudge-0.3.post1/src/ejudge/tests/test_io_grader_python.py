import pytest
from ejudge import io
from iospec import parse_string, types


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
    cases = io.run(src_ok, ['foo'], lang='python', sandbox=False).cases
    data = cases[0].data
    assert cases
    assert len(cases) == 1
    assert data[0].data == 'name: '
    assert data[1].data == 'foo'
    assert data[2].data == 'hello foo!'


def test_simple_case_success_timeout(src_ok):
    cases = io.run(src_ok, ['foo'], lang='python', timeout=0.5, sandbox=False).cases
    data = cases[0].data
    assert len(cases) == 1
    assert data[0].data == 'name: '
    assert data[1].data == 'foo'
    assert data[2].data == 'hello foo!'


def test_simple_case_success_sandbox(src_ok):
    cases = io.run(src_ok, ['foo'], lang='python', sandbox=True).cases
    data = cases[0].data
    assert len(cases) == 1
    assert data[0].data == 'name: '
    assert data[1].data == 'foo'
    assert data[2].data == 'hello foo!'


def test_grading_correct_answer(iospec, src_ok):
    feedback = io.grade(src_ok, iospec, lang='python', sandbox=False)
    assert isinstance(feedback.answer_key, types.TestCaseNode)
    assert isinstance(feedback.case, types.TestCaseNode)
    assert feedback.grade == 1
    assert feedback.message is None
    assert feedback.status == 'ok'


def test_grading_incorrect_answer(iospec, src_bad):
    feedback = io.grade(src_bad, iospec, lang='python', sandbox=False)
    assert feedback.grade == 0
    assert feedback.status == 'wrong-answer'
    assert feedback.title == 'Wrong Answer'


def test_python_script_run(src_ok):
    cases = io.run(src_ok, ['foo'], lang='python3', sandbox=False).cases
    data = cases[0].data
    assert len(cases) == 1
    assert data[0].data == 'name: '
    assert data[1].data == 'foo'
    assert data[2].data == 'hello foo!'


if __name__ == '__main__':
    pytest.main('test_io_grader_python.py')
