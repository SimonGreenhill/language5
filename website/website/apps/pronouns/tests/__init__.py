from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun


# Mixin for default test content
class DefaultSettingsMixin(object):
    def add_fixtures(self):
        self.editor = User.objects.create_user('admin', 'admin@admin.com', "test")
        self.lang = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', 
                                             classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year="1991", author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        self.word = Word.objects.create(word='Pronoun', slug='apronoun', 
                                        full='pronoun', editor=self.editor)
                                        
        # add some pronoun types
        for person in [1, 2, 3]:
            w = Word.objects.create(
                word="pronoun-a-%d-sg" % person,
                slug="pronoun-a-%d-sg" % person,
                editor=self.editor
            )
            w.save()
            p = PronounType.objects.create(
                word=w, 
                alignment='A', person=person, number='sg',
                sequence=person, # dummy variable just for sorting
                editor=self.editor
            )
            p.save()
        
        
        # create this here so that _prefill_pronouns() takes advantage of our
        # newly created pronountypes
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                 source=self.source, 
                                 editor=self.editor,
                                 comment="test")
        self.pdm._prefill_pronouns()

    
    def test_have_some_pronoun_types(self):
        # lots of tests will fail bizarrely if we don't have any pronountypes 
        # defined (i.e. those that iterate over PronounType._generate_all*).
        # So here we check that the add_fixtures code has successfully set things
        # up
        assert PronounType.objects.count() == 3