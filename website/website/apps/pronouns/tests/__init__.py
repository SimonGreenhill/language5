from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word
from website.apps.pronouns.models import Paradigm, PronounType


# Mixin for default test content
class PronounsTestData(object):
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create_user(
            'admin', 'admin@admin.com', "test"
        )
        cls.lang = Language.objects.create(
            language='A', slug='langa',
            information='i.1',
            classification='a, b',
            isocode='aaa', editor=cls.editor
        )
        cls.source = Source.objects.create(
            year="1991", author='Smith',
            slug='Smith1991', reference='S2',
            comment='c1', editor=cls.editor
        )
        cls.word = Word.objects.create(
            word='Pronoun', slug='apronoun',
            full='pronoun', editor=cls.editor
        )
        
        # add some pronoun types
        for person in [1, 2, 3]:
            w = Word.objects.create(
                word="pronoun-a-%d-sg" % person,
                slug="pronoun-a-%d-sg" % person,
                editor=cls.editor
            )
            w.save()
            p = PronounType.objects.create(
                word=w,
                alignment='A', person=person, number='sg',
                sequence=person,  # dummy variable just for sorting
                editor=cls.editor
            )
            p.save()
            
        # create this here so that _prefill_pronouns() takes advantage of our
        # newly created pronountypes
        cls.pdm = Paradigm.objects.create(
            language=cls.lang,
            source=cls.source,
            editor=cls.editor,
            comment="test"
        )
        cls.pdm._prefill_pronouns()

