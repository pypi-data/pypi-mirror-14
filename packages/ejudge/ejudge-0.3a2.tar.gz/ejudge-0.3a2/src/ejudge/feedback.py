import decimal
from ejudge.util import html_escape, indent


ERROR_TITLES = {
    'error-timeout': 'Timeout Error',
}


def get_feedback(case, answer_key):
    """Return a feedback structure that represents the expected error"""

    if case == answer_key:
        return Feedback(case, answer_key)

    feedback = Feedback(case, answer_key, grade=decimal.Decimal(0))

    # Presentation errors
    if presentation_equal(case, answer_key):
        feedback.title = 'Presentation Error'
        feedback.status = 'presentation-error'
        feedback.grade = decimal.Decimal(0.5)

    # Wrong answer
    elif case.type.startswith('io'):
        feedback.status = 'wrong-answer'
        feedback.title = 'Wrong Answer'

    # Error messages
    elif case.type.startswith('error'):
        feedback.status = case.type
        try:
            feedback.title = ERROR_TITLES[case.type]
        except KeyError:
            title = ' '.join(reversed(case.title.split('-')))
            feedback.title = title.title()

    else:
        raise ValueError('invalid testcase type: %r' % case.type)

    return feedback


def presentation_equal(case1, case2):
    """Return True if both cases are equal after casefolding and stripping all
    spaces"""

    #TODO: implement
    return case1 == case2


#
# Error message classes
#
class Feedback:
    """User feedback.

    Parameters
    ----------

    value : TestCase
        pass
    title: str
        Title of the message (e.g., Wrong answer)
    """
    
    def __init__(self, case, answer_key,
                 grade=decimal.Decimal(1), status='ok',
                 title=None, message=None, hint=None):

        self.case = case
        self.answer_key = answer_key
        self.grade = grade
        self.status = status
        self.title = title
        self.hint = hint
        self.message = message
        if message is None and case.type.startswith('error'):
            self.message = case.error

    def render_testcase(self, default='', *, format=None):
        """Render the interaction attribute with the given format.

        An optional default can be given if no response exists."""

        format = format or self.format
        if self.interaction is None:
            return default
        else:
            return self.interaction.format(format)

    def render_template(self, default='', format=None):
        """Render the template attribute with the given format

        An optional default can be given if no template exists."""

        format = format or self.format
        if self.template is None:
            return default
        else:
            return self.template.format(format)

    def name(self):
        """A string with the error name"""

        return type(self.error).__name__


    def title_text(self, format='plain'):  # @ReservedAssignment
        """Return a formatted text representing the title"""

        if format == 'plain':
            title = self.title()
            line = '-' * len(title)
            return '\n'.join([line, title, line])
        elif format == 'html':
            title = self.title()
            return '<strong>%s</strong>' % html_escape(title)
        else:
            return self.title_text('plain')

    def render_plain(self, color=None):
        """Generic formatter of plain text messages"""

        title = self.title_text()
        method = 'color' if color else 'plain'
        template = indent(self.render_template(method) or '')
        interaction = indent(self.render_interaction(method) or '')
        message = self.message_color() if color else self.message_plain()
        message = indent(message or '')
        feedback_title = self.FEEDBACK_TITLE

        # Get colors
        color = color or disabled
        H = color.HEADER
        B = color.BOLD
        I = color.INPUTVALUE
        E = color.ENDC

        # Formatted strings
        D = locals()
        title = '%(H)s%(title)s%(E)s\n\n' % D
        expected = '%(B)sExpected answer:%(E)s\n%(template)s\n\n' % D
        obtained = '%(B)sObtained:%(E)s\n%(interaction)s\n\n' % D
        hint = '%(B)s%(feedback_title)s:%(E)s\n%(message)s\n\n' % D

        # Remove empty parts
        if not self.template:
            expected = ''
        if not self.interaction:
            obtained = ''
        if not message.strip():
            hint = ''

        return ''.join([title, expected, obtained, hint])

    def render_color(self):
        """Generic formatter of plain text messages"""

        return self.render_plain(color=color)

    def render_html(self):
        """Generic formatter of html messages"""

        title = self.title()
        template = indent(self.render_template('html'))
        interaction = indent(self.render_interaction('html'))
        hint = indent(self.message_html())
        feedback_title = self.FEEDBACK_TITLE
        has_message = bool(self.message_plain())

        # Pieces
        D = locals()
        title = (
        '<div class="pyjudge-error-box">\n'
        '<div class="pyjudge-error-title">%(title)s</div>\n'
        ) % D
        expected = ((
        '<div class="pyjudge-example">\n'
        '  <p class="pyjudge-example-title">Expected answer (inputs in red):</p>\n'
        '  <div class="pyjudge-example-data">\n'
        '%(template)s\n'
        '  </div>\n'
        '</div>\n'
        ) % D) if self.template else ''
        obtained = ((
        '<div class="pyjudge-example">\n'
        '  <p class="pyjudge-example-title">Obtained:</p>\n'
        '  <div class="pyjudge-example-data">\n'
        '%(interaction)s\n'
        '  </div>\n'
        '</div>\n'
        ) % D) if self.interaction else ''
        hint = ((
        '<div class="pyjudge-hint">\n'
        '  <p class="pyjudge-example-title">%(feedback_title)s:</p>\n'
        '  <div class="pyjudge-hint-data">\n'
        '%(hint)s\n'
        '  </div>\n'
        '</div>\n'
        ) % D) if has_message else ''

        return ''.join([title, expected, obtained, hint, '</div>'])

    def message_plain(self):
        return ''

    def message_color(self):
        return self.message_plain()

    def message_html(self):
        plain = self.message_plain()
        return ('<pre>%s</pre>' % plain if plain is not None else None)

    @property
    def data(self):
        try:
            return self._data
        except AttributeError:
            try:
                self._data = self.render_page()
            except Exception as ex:
                raise RuntimeError('exception caught when rendering message: %r' % ex)
            return self._data
        
    @data.setter
    def data(self, value):
        self._data = value

    def render(self, format=None):  # @ReservedAssignment
        """Render object by the specified format.

        If no format is given, use the default format defined in the
        constructor."""
        
        if format is None:
            format = self.format  # @ReservedAssignment
        try:
            render_format = getattr(self, 'render_' + format)
        except AttributeError:
            raise ValueError('unknown format: %r' % format)
        else:
            return render_format()
            
    def render_plain(self):
        """Plain text rendering"""
        
        return self.args[0]
        
    def render_html(self):
        """HTML rendering.

        The default behavior is to put the html-escaped contents of plain text
        rendering inside <pre> </pre> tags.
        """
        
        plain = self.render_plain()
        return '<pre>\n%s\n</pre>' % html_escape(plain)
    
    def render_latex(self):
        """LaTeX rendering.

        The default behavior is to put the contents of plain text rendering into
        a verbatim environment."""
        
        return '\\begin{verbatim}\n%s\n\end{verbatim}' % self.render_plain()

#
# Color support
# See: https://en.wikipedia.org/wiki/ANSI_escape_code
#
class color:
    HEADER = '\033[1m\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INPUTVALUE = BOLD + FAIL

class disabled:
    BOLD = ''
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''
    INPUTVALUE = ''
