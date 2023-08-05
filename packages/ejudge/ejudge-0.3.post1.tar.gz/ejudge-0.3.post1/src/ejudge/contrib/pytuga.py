from ejudge.langs import ScriptingLanguage


class Pytuga2Manager(ScriptingLanguage):
    name = 'pytuga'
    description = 'Pytuguês'
    extensions = ['pytg']
    shellargs = ['pytuga', 'main.py']

    def syntax_check(self):
        pass