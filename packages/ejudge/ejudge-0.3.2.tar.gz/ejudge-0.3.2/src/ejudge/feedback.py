import decimal
import jinja2
from ejudge.util import tex_escape


# Module constants
error_titles = {
    'error-timeout': 'Timeout Error',
}

jinja_loader = jinja2.PackageLoader('ejudge')
jinja_env = jinja2.Environment(
    loader=jinja_loader,
    trim_blocks=True,
    lstrip_blocks=True
)


latex_env = jinja2.Environment(
    loader=jinja_loader,
    trim_blocks=True,
    lstrip_blocks=True,
    block_start_string='((*',
    block_end_string='*))',
    variable_start_string='\\var{',
    variable_end_string='}'
)
latex_env.filters['escape'] = tex_escape


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
                 title='Correct answer', message=None, hint=None):

        self.case = case
        self.answer_key = answer_key
        self.grade = grade
        self.status = status
        self.title = title
        self.hint = hint
        self.message = message
        if message is None and case.type.startswith('error'):
            self.message = case.error

    @property
    def is_correct(self):
        return self.grade == 1

    def render(self, method='text', **kwds):
        """Render object using the specified method."""

        try:
            render_format = getattr(self, 'as_' + format)
        except AttributeError:
            raise ValueError('unknown format: %r' % format)
        else:
            return render_format(**kwds)

    def as_text(self):
        """Plain text rendering"""

        return self._render('feedback.txt', color=disabled)

    def as_color(self):
        """Plain text rendering with terminal colors."""

        return self._render('feedback.txt', color=color)

    def as_html(self):
        """Render to an html div. Same as as_div()"""

        return self._render('feedback-div.html')

    def as_div(self):
        """Render to an html div."""

        return self._render('feedback-div.html')

    def as_latex(self):
        """Render to latex."""

        return self._render('feedback.tex', latex=True)

    def _render(self, template, latex=False, **kwds):
        ns = {
            'case': self.case,
            'answer_key': self.answer_key,
            'grade': self.grade,
            'status': self.status,
            'title': self.title,
            'hint': self.hint,
            'message': self.message,
            'is_correct': self.is_correct,
            'h1': self._overunderline,
            'h2': self._underline,
        }

        # Get template
        if latex:
            template = latex_env.get_template(template)
        else:
            template = jinja_env.get_template(template)

        # Render it!
        ns.update(kwds)
        data = template.render(**ns)
        if data.endswith('\n'):
            return data[:-1]
        return data

    @staticmethod
    def _overunderline(st, symbol='='):
        st = (st or '   ').replace('\t', '    ')
        size = max(len(line) for line in st.splitlines())
        line = symbol * size
        return '%s\n%s\n%s' % (line, st, line)

    @staticmethod
    def _underline(st, symbol='='):
        st = (st or '   ').replace('\t', '    ')
        size = max(len(line) for line in st.splitlines())
        line = symbol * size
        return '%s\n%s' % (st, line)

    @staticmethod
    def _overline(st, symbol='='):
        st = (st or '   ').replace('\t', '    ')
        size = max(len(line) for line in st.splitlines())
        line = symbol * size
        return '%s\n%s' % (line, st)


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


def get_feedback(case, answer_key):
    """Return a feedback structure that represents the expected error"""

    if list(case) == list(answer_key):
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
            feedback.title = error_titles[case.type]
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
