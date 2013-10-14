from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon

from website.apps.lexicon.management.commands import hygiene


class HygieneDataMixin(TestCase):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.word = Word.objects.create(word='Hand', slug='hand', 
                                        full='a hand', editor=self.editor)
        self.lang = Language.objects.create(language='A', slug='lang', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year=1991, author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        
        # some ok entries;
        self.good1 = Lexicon.objects.create(
            language=self.lang, 
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="not empty"
        )
        self.good2 = Lexicon.objects.create(
            language=self.lang, 
            word=self.word,
            source=self.source,
            editor=self.editor,
            entry="a word"
        )
    
    
class Test_Empty(HygieneDataMixin):
    """Tests the hygiene management command - find-empty"""
    
    def setUp(self):
        super(Test_Empty, self).setUp()
        
        self.empty = {
            'dash': Lexicon.objects.create(
                language=self.lang, 
                word=self.word,
                source=self.source,
                editor=self.editor,
                entry="-"
            ),
            'dashdash': Lexicon.objects.create(
                language=self.lang, 
                word=self.word,
                source=self.source,
                editor=self.editor,
                entry="--"
            ),
            'dashdashdash': Lexicon.objects.create(
                language=self.lang, 
                word=self.word,
                source=self.source,
                editor=self.editor,
                entry="---"
            ),
            'empty': Lexicon.objects.create(
                language=self.lang, 
                word=self.word,
                source=self.source,
                editor=self.editor,
                entry=""
            ),
        }
        
    def test_find_missing(self):
        cmd = hygiene.Command()
        assert self.empty['empty'] in cmd.find_empty()
    
    def test_find_dash(self):
        cmd = hygiene.Command()
        assert self.empty['dash'] in cmd.find_empty()
    
    def test_find_dashdash(self):
        cmd = hygiene.Command()
        assert self.empty['dashdash'] in cmd.find_empty()
    
    def test_find_dashdashdash(self):
        cmd = hygiene.Command()
        assert self.empty['dashdashdash'] in cmd.find_empty()
        
    def test_find_all(self):
        cmd = hygiene.Command()
        for d in self.empty:
            assert self.empty[d] in cmd.find_empty()
        
    def test_delete(self):
        assert len(Lexicon.objects.all()) == 6
        cmd = hygiene.Command()
        cmd.delete(cmd.find_empty())
        assert len(Lexicon.objects.all()) == 2, "Expected 2 got: %d" % len(Lexicon.objects.all())
        assert Lexicon.objects.get(pk=self.good1.pk)
        assert Lexicon.objects.get(pk=self.good2.pk)
        

class Test_Duplicates(HygieneDataMixin):
    """Tests the hygiene management command - find-duplicates"""
    
    def test_find(self):
        dupe1 = Lexicon.objects.create(
                language=self.good1.language, 
                word=self.good1.word,
                source=self.good1.source,
                editor=self.good1.editor,
                entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 1
        assert dupes[0].id == dupe1.id
    
    def test_delete(self):
        dupe1 = Lexicon.objects.create(
                language=self.good1.language, 
                word=self.good1.word,
                source=self.good1.source,
                editor=self.good1.editor,
                entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        cmd.delete(cmd.find_duplicates())
        assert len(Lexicon.objects.all()) == 2, "Expected 2 got: %d" % len(Lexicon.objects.all())
        assert Lexicon.objects.get(pk=self.good1.pk)
        assert Lexicon.objects.get(pk=self.good2.pk)
      
    def test_not_duplicate_if_different_word(self):
        newword = Word.objects.create(word='Banana', slug='banana', 
                                        full='Yum', editor=self.editor)
        o = Lexicon.objects.create(
                language=self.good1.language, 
                word=newword,
                source=self.good1.source,
                editor=self.good1.editor,
                entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 0
    
    def test_not_duplicate_if_different_source(self):
        newsource = Source.objects.create(year=2013, author='Greenhill', 
                                 slug='Greenhill2013', reference='...',
                                 comment='', editor=self.editor)
        o = Lexicon.objects.create(
                language=self.good1.language, 
                word=self.good1.word,
                source=newsource,
                editor=self.good1.editor,
                entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 0
        
    def test_not_duplicate_if_different_language(self):
        newlang = Language.objects.create(language='B', slug='langb', 
                                             information='', classification='',
                                             isocode='bbb', editor=self.editor)
        o = Lexicon.objects.create(
                language=newlang, 
                word=self.good1.word,
                source=self.good1.source,
                editor=self.good1.editor,
                entry=self.good1.entry
        )
        
        cmd = hygiene.Command()
        dupes = cmd.find_duplicates()
        assert len(dupes) == 0
