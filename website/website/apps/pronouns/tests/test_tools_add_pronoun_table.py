from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm
from website.apps.pronouns.tools import add_pronoun_table
from website.apps.pronouns.tests import PronounsTestData


class TestFindIdenticals(PronounsTestData, TestCase):
    
    def test_full(self):
        pdm = Paradigm.objects.create(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            comment="TestFindIdenticals"
        )
        pdm._prefill_pronouns()
        
        for counter, pron in enumerate(pdm.pronoun_set.all(), 1):
            lex = Lexicon.objects.create(
                editor=self.editor,
                language=self.lang,
                source=self.source,
                word=self.word,
                entry='fudge-full-%d' % counter
            )
            lex.save()
            pron.entries.add(lex)
            pron.save()
            
        table = add_pronoun_table(
            pdm.pronoun_set.all(), filter_empty_rows=False
        )
        assert len(table) == 3
        for counter, row in enumerate(table, 1):
            expected = 'fudge-full-%d' % counter
            assert row[1].get('A').entries.all()[0].entry == expected

    def test_partial(self):
        pdm = Paradigm.objects.create(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            comment="TestFindIdenticals"
        )
        pdm._prefill_pronouns()
        pron = pdm.pronoun_set.all().order_by('pronountype__person')[0]
        lex = Lexicon.objects.create(
            editor=self.editor,
            language=self.lang,
            source=self.source,
            word=self.word,
            entry='fudge-partial'
        )
        lex.save()
        pron.entries.add(lex)
        pron.save()
        
        table = add_pronoun_table(
            pdm.pronoun_set.all(), filter_empty_rows=True
        )
        assert len(table) == 1
        assert table[0][0] == u'1st (excl) Person Singular'
        assert table[0][1].get('A') == pron
        
    def test_empty(self):
        pdm = Paradigm.objects.create(
            language=self.lang,
            source=self.source,
            editor=self.editor,
            comment="TestFindIdenticals"
        )
        pdm._prefill_pronouns()
        table = add_pronoun_table(
            pdm.pronoun_set.all(), filter_empty_rows=True
        )
        assert table == []
        
        
