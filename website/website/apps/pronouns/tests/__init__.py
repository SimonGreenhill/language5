from django.contrib.auth.models import User
from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon
from website.apps.pronouns.models import Paradigm, PronounType, Relationship


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
            comment="test",
            label="label",
            analect="F"
        )
        cls.pdm._prefill_pronouns()
        
        cls.p1, cls.p2, cls.p3 = cls.pdm.pronoun_set.all()
            
        # relationships
        cls.lex1 = Lexicon.objects.create(
            editor=cls.editor,
            source=cls.source,
            language=cls.lang,
            word=cls.word,
            entry='lexicon 1'
        )
        cls.lex2 = Lexicon.objects.create(
            editor=cls.editor,
            source=cls.source,
            language=cls.lang,
            word=cls.word,
            entry='lexicon 2'
        )
        cls.lex3 = Lexicon.objects.create(
            editor=cls.editor,
            source=cls.source,
            language=cls.lang,
            word=cls.word,
            entry='lexicon 3'
        )
        cls.p1.entries.add(cls.lex1)
        cls.p1.save()

        cls.p2.entries.add(cls.lex2)
        cls.p2.save()

        cls.p3.entries.add(cls.lex3)
        cls.p3.save()

        cls.rel = Relationship.objects.create(
            paradigm=cls.pdm,
            pronoun1=cls.p1, pronoun2=cls.p2,
            relationship='TS',
            editor=cls.editor
        )
