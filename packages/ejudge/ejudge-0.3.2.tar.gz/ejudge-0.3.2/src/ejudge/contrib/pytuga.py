import pytuga
from ejudge.langs import ScriptingLanguage, IntegratedLanguage


class PytugaScriptManager:
    abstract = True
    name = 'pytuga'
    description = 'Pytuguês'
    extensions = ['pytg']
    shellargs = ['pytuga', 'main.pytg']

    def syntax_check(self):
        return NotImplemented


class PytugaIntegradtedManager(IntegratedLanguage):
    name = 'pytuga'
    description = 'Pytuguês'
    extensions = ['pytg']

    def syntax_check(self):
        return NotImplemented

    def exec(self, inputs, context):
        assert context is not None
        pytuga.exec(self.source, context.globals, context.locals,
                    forbidden=True)

    def modules(self):
        return super().modules() + ['pytuga.lib.forbidden']