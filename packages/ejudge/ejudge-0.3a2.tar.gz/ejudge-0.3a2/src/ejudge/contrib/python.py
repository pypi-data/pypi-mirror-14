import io
import traceback
from ejudge.langs import IntegratedLanguage, ScriptingLanguage


class Python3Mixin:
    def syntax_check(self):
        try:
            compile(self.source, '<string>', 'exec')
        except SyntaxError:
            out = io.StringIO()
            traceback.print_exc(file=out, limit=0)
            msg = out.getvalue()
            raise SyntaxError(msg)

    def prepare_error(self, ex):
        """Formats exception"""

        exname = type(ex).__name__
        messages = []
        codelines = self.source.splitlines()
        tb = ex.__traceback__

        tblist = reversed(traceback.extract_tb(tb))
        for (filename, lineno, funcname, text) in tblist:
            if 'judge' in filename:
                break
            if filename == '<string>':
                text = codelines[lineno - 1].strip()
            messages.append((filename, lineno, funcname, text))

        messages.reverse()
        messages = traceback.format_list(messages)
        messages.insert(0, 'Traceback (most recent call last)')
        messages.append('%s: %s' % (exname, ex))
        return '\n'.join(messages)


class PythonManager(Python3Mixin, IntegratedLanguage):
    name = 'python'
    description = 'Python 3.x'
    extensions = ['py', 'py3']

    def exec(self, inputs, context):
        assert context is not None
        code = compile(self.source, '<string>', 'exec')
        exec(code, context.globals, context.locals)


class PythonScriptManager(Python3Mixin, ScriptingLanguage):
    name = 'python3'
    description = 'Python 3.x'
    extension = 'py'
    shellargs = ['python3', 'main.py']


class Python2Manager(ScriptingLanguage):
    name = 'python2'
    description = 'Python 2.7'
    extension = 'py'
    shellargs = ['python2', 'main.py']

    def syntax_check(self):
        pass


def python_io_builder(src):
    """Default buildfunc for python code.

    Checks for syntax errors."""

    try:
        compile(src, '<string>', 'exec')
    except SyntaxError:
        out = io.StringIO()
        traceback.print_exc(file=out, limit=0)
        msg = out.getvalue()
        raise error.BuildProblem(code=src, msg=msg)
    return src



def _format_exception(ex, src):
    """Formats exception"""

    exname = type(ex).__name__
    messages = []
    codelines = src.splitlines()
    tb = ex.__traceback__

    tblist = reversed(traceback.extract_tb(tb))
    for (filename, lineno, funcname, text) in tblist:
        if 'judge' in filename:
            break
        if filename == '<string>':
            text = codelines[lineno - 1].strip()
        messages.append((filename, lineno, funcname, text))

    messages.reverse()
    messages = traceback.format_list(messages)
    messages.insert(0, 'Traceback (most recent call last)')
    messages.append('%s: %s' % (exname, ex))
    return '\n'.join(messages)



"""
#python3_builder = partial(script_builder, '.py', python3_syntax)
python3_runner = partial(script_runner, ['python3', 'main.py'])

#
# Register all python io graders
#
ioregister('python', 'Python 3.x', python_io_builder, python_io_runner,
           ['py', 'py3'])

# Python 2
ioregister('python2', 'Python 2.x',
           partial(script_builder, '.py', python2_syntax),
           partial(script_runner, ['python2', 'main.py']),
           ['py2'])

# Python 3
ioregister('python3', 'Python 3.x',
           partial(script_builder, '.py', python3_syntax),
           partial(script_runner, ['python3', 'main.py']),
           [])


# Pytuga
ioregister('pytuga', 'Pytuguês',
           partial(script_builder, '.pytg', pytuga_syntax),
           partial(script_runner, ['pytuga', 'main.pytg']),
           ['.pytg'])
"""