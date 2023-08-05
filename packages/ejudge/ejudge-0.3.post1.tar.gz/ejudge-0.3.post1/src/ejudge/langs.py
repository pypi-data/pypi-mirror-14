import os
import abc
import tempfile
from iospec import types
from iospec.runners import IoObserver
from ejudge import builtins
from ejudge import util
from ejudge.pinteract import Pinteract


__all__ = ['IntegratedLanguage', 'ScriptingLanguage', 'CompiledLanguage']


class LanguageMeta(abc.ABCMeta):
    def __new__(cls, name, bases, namespace):
        new = type.__new__(cls, name, bases, namespace)
        if not namespace.get('abstract', False):
            new.register(**namespace)
        return new

    def register(cls, *, name, description, extensions=[], **kwds):
        """Register class after creation."""

        for ext in extensions:
            cls.registered_extensions[ext] = name
        if extensions:
            cls.registered_language_extensions[name] = extensions[0]
        cls.supported_languages[name] = cls


class LanguageManager(metaclass=LanguageMeta):
    """
    Support for new languages is done by subclassing this class.

    The LanguageManager automatically register new classes using meta
    information that is passed as class attributes. It requires that the
    following attributes should be defined:

    name:
        Short lowercase name for the language. (e.g.: python)
    description:
        A short description of the language (appending version numbers and
        possibly compile flags). (e.g.: Python 3.x)
    extensions:
        A list of valid extensions associated to that language.

    """
    abstract = True
    supported_languages = {}
    registered_extensions = {}
    registered_language_extensions = {}

    class BuildError(Exception):
        pass

    def __init__(self, source):
        self.source = source
        self.context = None

    @classmethod
    def from_language(cls, lang, source):
        try:
            factory = cls.supported_languages[lang]
        except KeyError:
            raise ValueError('invalid language: %r' % lang)
        return factory(source)

    @abc.abstractmethod
    def build_context(self):
        """Returns the build context for the given manager.

        Subclasses should not need to implement an explicit syntax check in this
        function. Override the syntax_check() for this.

        Failed builds can either return None or raise a BuildError."""

        raise NotImplementedError

    @abc.abstractmethod
    def exec(self, inputs, context):
        """Executes the source code in the given context and return the
        resulting test case object

        The context parameter is the result of calling the build function."""

        raise NotImplementedError

    @abc.abstractmethod
    def syntax_check(self):
        raise SyntaxError('invalid syntax')

    def build(self):
        """Builds and check the source code syntax. Also prepares the
        environment before execution.

        This function can be called multiple times and it will return a cached
        build context."""

        if self.context is None:
            self.syntax_check()
            self.context = self.build_context()
            if self.context is None:
                data = util.indent(self.source)
                raise self.BuildError('cannot build source: \n%s' % data)
        return self.context

    def prepare_error(self, ex):
        """Prepares an exception receiving trying to execute
        manager.exec(ctx, inputs) before it is inserted into the error attribute
        of the returning ErrorTestCase."""

        return str(ex)

    def flush_io(self):
        """Flush all io buffers and return what has been collected so far.

        The resulting value is a list of plain input or output nodes."""

        return []

    def run(self, inputs, *, timeout=None, context=None):
        """Executes the program with the given inputs"""

        if context is None:
            context = self.build()

        try:
            func = self.exec
            return remove_trailing_newline(
                    util.timeout(func, args=(inputs, context), timeout=timeout))

        except TimeoutError as ex:
            msg = 'Maximum execution time exceeded: %s sec' % timeout
            return types.ErrorTestCase(
                type='error-timeout',
                data=self.flush_io(),
                timeout=timeout,
                error=msg)

        except RuntimeError as ex:
            data = self.flush_io()
            return remove_trailing_newline(types.ErrorTestCase(
                type='error-exception',
                error=self.prepare_error(ex),
                data=self.flush_io(),
            ))


class IntegratedLanguage(LanguageManager):
    """Base class for all languages that expose hooks for printing and input
    directly to Python's interpreter itself.

    This runner is the most integrated with the ejudge system. Ideally all
    languages should be implemented as subclasses of IntegratedLanguage.
    This may not be feasible or practical for most programming languages,
    though."""

    abstract = True

    def __init__(self, source, globals={}, locals={}, builtins={}):
        super().__init__(source)
        self.observer = IoObserver()
        self.globals = globals.copy()
        self.locals = locals.copy()
        self.builtins = {
            'print': self.observer.print,
            'input': self.observer.input,
        }
        self.builtins.update(builtins)

    def build_context(self):
        self.syntax_check()

        return types.Node(
            globals=self.globals.copy(),
            locals=self.locals.copy(),
        )

    def run(self, inputs, **kwds):
        builtins.update(self.builtins)
        self.observer.flush()
        self.observer.extend_inputs(inputs)

        try:
            result = super().run(inputs, **kwds)
            if result is None:
                result = types.IoTestCase(type='io-plain',
                                          data=self.observer.flush())
        finally:
            builtins.restore()

        return remove_trailing_newline(result)

    def syntax_check(self):
        raise NotImplementedError


class ScriptingLanguage(LanguageManager):
    """Basic support for scripting language."""

    abstract = True

    @property
    def extension(self):
        return self.extensions[0]

    @property
    def shellargs(self):
        raise RuntimeError('shellargs must be overriden in the subclass')

    def build_context(self):
        """Base buildfunc for source code that can be executed as scripts.

        Concrete implementations must provide a default extension for the script
        files and a syntax_check(src) function, that takes a string of code and
        raise BuildProblem if the syntax is invalid."""

        tmpdir = tempfile.mkdtemp()
        tmppath = os.path.join(tmpdir, 'main.' + self.extension)
        with open(tmppath, 'w') as F:
            F.write(self.source)
        return types.Node(
            tempdir=tmpdir,
            temppath=tmppath,
            shellargs=self.shellargs,
        )

    def exec(self, inputs, context):
        return self.exec_pinteract(inputs, context)

    def exec_pinteract(self, inputs, context):
        """Run script as a subprocess and gather results of execution.

        This is a generic implementation. Specific languages or runtimes are
        supported by fixing the shellargs argument of this function. This function
        uses the PInteract() object for communication with scripts.
        """

        def append_non_empty_out(L):
            data = process.receive()
            if data:
                stream.append(types.Node(type='output', data=data))

        tmpdir = context.tempdir
        currpath = os.getcwd()
        shellargs = self.shellargs
        inputs = list(inputs)
        stream = []
        result = types.Node(type='io', data=stream)

        # Execute script in the tmpdir and than go back once execution has
        # finished
        currpath = os.getcwd()
        os.chdir(tmpdir)
        try:
            process = Pinteract(shellargs)

            # Fetch all In/Out strings
            append_non_empty_out(stream)
            while inputs:
                inpt = inputs.pop(0)
                try:
                    process.send(inpt)
                    stream.append(types.Node(type='input', data=inpt))
                except RuntimeError:
                    inputs.append(inpt)
                    return types.ErrorTestCase(
                            type='error-exception', data=stream)
                append_non_empty_out(stream)
        finally:
            os.chdir(currpath)

        # Finish process
        error_ = process.finish()
        assert not any(error_), error_
        return result


    def exec_popen(self, inputs, context):
        """Run script as a subprocess and gather results of execution.

        This is a generic implementation. Specific languages or runtimes are
        supported by fixing the shellargs argument of this function. This function
        uses a Popen() object to interact with the scripts. It should be avoided
        in favor of the PInteract() version.
        """

        tmpdir, _src = ctx

        # Prepare list of inputs and interactions
        inputs = ''.join(str(x) + '\n' for x in template.inputs())
        template = as_atom(template)
        timeout = None if timeout == float('inf') else timeout

        # Execute script in the tmpdir and than go back once execution has finished
        currpath = os.getcwd()
        os.chdir(tmpdir)
        try:
            PIPE = subprocess.PIPE
            STDOUT = subprocess.STDOUT
            process = subprocess.Popen(shellargs, universal_newlines=True,
                                       stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            out, _error = process.communicate(inputs, timeout=timeout)
        except subprocess.CalledProcessError as ex:
            out = IOAtom([], error=ex)
            out.error = error.RuntimeProblem(template=template,
                                                    interaction=out)
            raise
            return out
        except (TimeoutError, subprocess.TimeoutExpired) as ex:
            out = IOAtom([], error=ex)
            out.error = error.TimeExceeded(template=template,
                                                 interaction=out)
            return out

        finally:
            os.chdir(currpath)

        # Try to guess interaction from inputs and outputs
        # For now, it only attempts to do an exact match.
        queue = list(template)[::-1]
        interaction = []
        while queue:
            elem = queue.pop()
            if isinstance(elem, In):
                interaction.append(elem)
            elif out.startswith(str(elem)):
                out = out[len(out):]
                interaction.append(elem)
            else:
                interaction.extend(x for x in reversed(queue) if isinstance(x, In))
                interaction.append(Out(out))

        return IOAtom(interaction)






class CompiledLanguage(LanguageManager):
    abstract = True


    def compiled_builder(ext, shellargs, src):
        """Base buildfunc for source code that must be compiled as part of the
        build process.

        Pass the list of shell arguments to run a command that takes a "main.ext"
        file and compiles it to "main.exe". Raises a BuildProblem if compilation
        return with a non-zero value."""

        # Save source file in temporary dir
        tmpdir = tempfile.mkdtemp()
        tmppath = os.path.join(tmpdir, 'main' + ext)
        with open(tmppath, 'w') as F:
            F.write(src)

        # Compile and return
        currpath = os.getcwd()
        os.chdir(tmpdir)
        try:
            errmsgs = 'compilation is taking too long'
            errmsgs = subprocess.check_output(shellargs, timeout=10)
        except (subprocess.CalledProcessError, TimeoutError):
            raise error.BuildProblem(errmsgs)
        finally:
            os.chdir(currpath)

        return (tmpdir, src)


    def compiled_runner(ctx, template, *, timeout=None, pinteract=True, **kwds):
        """Base runner of compiled programs. Can be used as-is."""

        path = os.path.join(ctx[0], 'main.exe')
        if pinteract:
            return script_runner_pinteract([path], ctx, template, timeout=timeout, **kwds)
        else:
            warnings.warn('pinteract=False is not recommended. There are fundamental unresolved issues with the popen interface')
            return script_runner_popen([path], ctx, template, timeout=timeout, **kwds)


def remove_trailing_newline(case):
    """Remove a trailing newline from the last output node."""

    if case is None:
        return None

    if case.data:
        last = case.data[-1]
        if last.type == 'output' and last.data.endswith('\n'):
            last.data = last.data[:-1]
    return case


if __name__ == '__main__':
    src = 'print("hello world!")'
    pymgm = PythonManager(src)
    out = pymgm.run([])
    print(out)