from django.test import TestCase

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import add_pronoun_table

from website.apps.pronouns.tests import DefaultSettingsMixin


class TestFindIdenticals(DefaultSettingsMixin, TestCase):

    def setUp(self):
        self.add_fixtures()
        
    def test_full(self):
        for counter, pron in enumerate(self.pdm.pronoun_set.all(), 1):
            lex = Lexicon.objects.create(
                editor=self.editor,
                language=self.lang,
                source=self.source,
                word=self.word,
                entry='fudge-%d' % counter
            )
            lex.save()
            pron.entries.add(lex)
            pron.save()
            
        table = add_pronoun_table(self.pdm.pronoun_set.all(), filter_empty_rows=False)
        assert len(table) == 3
        for counter, row in enumerate(table, 1):
            assert row[1].get('A').entries.all()[0].entry == 'fudge-%d' % counter
        
    def test_partial(self):
        pron = self.pdm.pronoun_set.all()[0]
        lex = Lexicon.objects.create(
            editor=self.editor,
            language=self.lang,
            source=self.source,
            word=self.word,
            entry='fudge'
        )
        lex.save()
        pron.entries.add(lex)
        pron.save()
        
        table = add_pronoun_table(self.pdm.pronoun_set.all(), filter_empty_rows=True)
        assert len(table) == 1
        assert table[0][0] == u'1st (excl) Person Singular'
        assert table[0][1].get('A') == pron
        
    def test_empty(self):
        table = add_pronoun_table(self.pdm.pronoun_set.all(), filter_empty_rows=True)
        assert table == []
        