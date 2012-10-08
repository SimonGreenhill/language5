from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from website.apps.core.models import Language, Source, Note

class Test_Note(TestCase):
    """Tests the Note Model"""
    
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='langb',
                                             information='i.2', classification='c, d, e',
                                             isocode='bbb', editor=self.editor)
        self.source1 = Source.objects.create(year=1991, author='Smith', 
                                             slug='Smith1991', reference='S2',
                                             comment='c1', editor=self.editor)
        self.source2 = Source.objects.create(year=2002, author='Jones', 
                                 slug='Jones2002', reference='J2',
                                 comment='c2', editor=self.editor)
        # NOTE 1 belongs to Source 1 and Language 2
        self.note1 = Note.objects.create(language=self.lang1, source=self.source1,
                                             note='one', location="p1",
                                             editor=self.editor)
        # NOTE 2 belongs to Source 1 and Language 2
        self.note2 = Note.objects.create(language=self.lang2, source=self.source1,
                                             note='two', location="p2",
                                             editor=self.editor)
        # NOTE 3 belongs to Source 2 and Language 2
        self.note3 = Note.objects.create(language=self.lang2, source=self.source2,
                                             note='three', location="p3",
                                             editor=self.editor)

    def test_set_language(self):
        self.assertEquals(Note.objects.get(pk=1).language, self.lang1)
        self.assertEquals(Note.objects.get(pk=2).language, self.lang2)
        self.assertEquals(Note.objects.get(pk=3).language, self.lang2)
        
    def test_set_source(self):
        self.assertEquals(Note.objects.get(pk=1).source, self.source1)
        self.assertEquals(Note.objects.get(pk=2).source, self.source1)
        self.assertEquals(Note.objects.get(pk=3).source, self.source2)
        
    def test_set_note(self):
        self.assertEquals(Note.objects.get(pk=1).note, 'one')
        self.assertEquals(Note.objects.get(pk=2).note, 'two')
        self.assertEquals(Note.objects.get(pk=3).note, 'three')
    
    def test_set_location(self):
        self.assertEquals(Note.objects.get(pk=1).location, 'p1')
        self.assertEquals(Note.objects.get(pk=2).location, 'p2')
        self.assertEquals(Note.objects.get(pk=3).location, 'p3')
    
    def test_get_notes_for_language(self):
        self.assertEquals(len(self.lang1.note_set.all()), 1)
        self.assertEquals(len(self.lang2.note_set.all()), 2)

        self.assertEquals(self.lang1.note_set.all()[0].note, 'one')
        self.assertEquals(self.lang2.note_set.all()[0].note, 'two')
        self.assertEquals(self.lang2.note_set.all()[1].note, 'three')
        
    def test_get_notes_for_source(self):
        self.assertEquals(len(self.source1.note_set.all()), 2)
        self.assertEquals(len(self.source2.note_set.all()), 1)
        
        self.assertEquals(self.source1.note_set.all()[0].note, 'one')
        self.assertEquals(self.source1.note_set.all()[1].note, 'two')
        self.assertEquals(self.source2.note_set.all()[0].note, 'three')
        
