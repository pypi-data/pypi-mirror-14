import os
import decimal
import functools
from boxed import run as run_sandboxed
from iospec.parser import ErrorTestCase
from iospec import iotypes
from ejudge import util
from ejudge.feedback import get_feedback
from ejudge.langs import LanguageManager


# Python print function using the standard stdout
__all__ = ['grade', 'run', 'BuildError']
BuildError = LanguageManager.BuildError
grade = run = None


def prepare_manager(func):
    """Decorate functions in this block to receive a configured manager"""

    @functools.wraps(func)
    def decorated(src, *args, path=None, lang=None, manager=None, raises=False,
                  sandbox=False, timeout=None, **kwds):
        # Fix language
        if manager is None:
            if lang is None:
                ext = os.path.splitext(path or src.name)[1] or '.'
                try:
                    lang = LanguageManager.registered_extensions[ext[1:]]
                except KeyError:
                    raise ValueError('unknown extension: %r' % ext)

            # Normalize source string
            if not isinstance(src, str):
                src = src.read()
            manager = LanguageManager.from_language(lang, src)

        # Build
        try:
            manager.build()
        except BuildError as ex:
            if raises:
                raise
            return build_error_tree(ex)

        # Run task
        args += (manager,)
        if sandbox:
            return run_sandboxed(func, args=args, kwargs=kwds, timeout=timeout,
                                 imports=manager.modules())
        elif timeout:
            return util.timeout(func, args=args, kwargs=kwds, timeout=timeout)
        else:
            return func(*args, **kwds)

    globals()[func.__name__[1:]] = decorated
    return func


@prepare_manager
def _grade(iospec, manager, fast=True):
    """
    Grade the string of source code by comparing the results of all inputs and
    outputs in the given template structure.


    Parameters
    ----------

    src : str or file object
        The source string for the code or a file object
    iospec : IOSpec parse tree
        The expected template for correct answers
    lang : str
        Programming language for the given source code. The judge accepts the
        following languages. Users can register plugins to support additional
        languages or to override the default behavior or accepted languages.

        +===========+==========================================================+
        | Value     | Description                                              |
        +===========+==========================================================+
        | python    | For Python 3.x code. Default runner.                     |
        +-----------+----------------------------------------------------------+
        | python2   | Executes in a separate Python 2 interpreter.             |
        +-----------+----------------------------------------------------------+
        | python3   | Executes in a separate Python 3 interpreter. Used mostly |
        |           | for debuging since it lack in features and performance   |
        |           | compared to the default "python" runner.                 |
        +-----------+----------------------------------------------------------+
        | tcc       | Compile C code with the tiny C compiler                  |
        +-----------+----------------------------------------------------------+
        | clang     | Compile C code with clang                                |
        +-----------+----------------------------------------------------------+
        | gcc       | Compile C code with gcc                                  |
        +-----------+----------------------------------------------------------+
        | C         | Uses the first method available: tcc, clang or gcc       |
        +-----------+----------------------------------------------------------+

    sandbox : bool
        If True, code will run in a sandboxed environment as the `nobody` user.
        It is necessary to have your system properly configured in order to do
        this.
    timeout : float
        Maximum time (in seconds) for the complete test to run.

    Specific backends may support additional keyword arguments. The most common
    ones are shown bellow

    namespace (python): dict
        The globals() namespace used to run a python script.


    Returns
    -------

    A named tuple of (grade, feedback) with a decimal grade normalized to 1 and
    None or a feedback structure.
    """

    if not iospec:
        raise ValueError('cannot grade an iospec that has no cases')

    value = decimal.Decimal(1)
    feedback = None

    for answer_key in iospec:
        inputs = answer_key.inputs()
        case = manager.run(inputs)
        curr_feedback = get_feedback(case, answer_key)

        if feedback is None:
            feedback = curr_feedback

        if curr_feedback.grade < value:
            feedback = curr_feedback
            value = curr_feedback.grade

            if value == 0 and fast:
                break

    return feedback


@prepare_manager
def _run(inputs, manager=None):

    """Runs program with the given list of inputs and returns the
    corresponding IoSpecTree.

    Parameters
    ----------

    src : str or file
        The source code for the test program
    inputs : sequence
        A sequence of input strings. If input is a sequence of sequences,
        this function will perform multiple test cases.
    lang : str
        The name for the source code language. See :func:`ejudge.graders.io.grade`
        for more details.
    timeout : float
        A time limit for the entire run (in seconds). If this attribute is not
        given, the program will run without any timeout. This can be potentially
        dangerous if the input program has an infinite loop.
    sandbox : bool
        Controls if code is run in sandboxed mode or not. Sandbox protection
        is the default behavior on supported platforms.
    raises : bool
        If True, raise a BuildError if the build process fails. The default
        behavior is to return a IoSpecTree with a single test case of type
        'error-build'.
    path : str
        The absolute file path for the input string or file object.

    Returns
    -------

    A :cls:`iospec.IoSpecTree structure. If inputs is a sequence of strings,
    the resulting tree will have a single test case in its "cases" attribute.
    """

    inputs = util.pushbackiter(inputs)
    first = next(inputs)
    inputs.push(first)

    if isinstance(first, str):
        cases = [manager.run(inputs)]
    else:
        cases = [manager.run(values) for values in inputs]
    return iotypes.IoSpec(cases)


def build_error_tree(msg):
    return iotypes.IoSpec([ErrorTestCase(type='error-build', message=msg)])


if __name__ == '__main__':
    from iospec import parse
    from pprint import pprint


    template = parse('../tests/examples/simple.iospec')
    with open('../tests/examples/simple_wrong.py') as F:
        g = grade(F, template, timeout=None, sandbox=False)
    pprint(g)
