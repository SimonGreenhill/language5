from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word
from website.apps.pronouns.models import Paradigm, Pronoun


# Mixin for default test content
class DefaultSettingsMixin(object):
    def add_fixtures(self):
        self.editor = User.objects.create_user('admin', 'admin@admin.com', "test")
        self.lang = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', 
                                             classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year=1991, author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                 source=self.source, 
                                 editor=self.editor,
                                 comment="test")
        self.word = Word.objects.create(word='Pronoun', slug='apronoun', 
                                        full='pronoun', editor=self.editor)