from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from website.apps.core.models import Language, Family

class Test_Language_Repr(TestCase):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
    
    def test_simple(self):
        l = Language.objects.create(language='A', 
                                    slug='a', 
                                    information='', classification='',
                                    isocode='aaa', editor=self.editor)
        assert unicode(l) == u'A'

    def test_dialect(self):
        l = Language.objects.create(language='A', dialect="B",
                                    slug='a', 
                                    information='', classification='',
                                    isocode='aaa', editor=self.editor)
        assert unicode(l) == u'A (B Dialect)'
    
    def test_dialect_equals_none(self):
        l = Language.objects.create(language='A', dialect=None,
                                    slug='a', 
                                    information='', classification='',
                                    isocode='aaa', editor=self.editor)
        assert unicode(l) == u'A'
        
    def test_empty_dialect(self):
        l = Language.objects.create(language='A', dialect=u"",
                                    slug='a', 
                                    information='', classification='',
                                    isocode='aaa', editor=self.editor)
        assert unicode(l) == u'A'



class Test_Language(TestCase):
    """Tests the Language Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='langb',
                                             information='i.2', classification='c, d, e',
                                             isocode='bbb', editor=self.editor)
    
    def test_set_language(self):
        self.assertEquals(Language.objects.get(pk=1).language, self.lang1.language)
        self.assertEquals(Language.objects.get(pk=2).language, self.lang2.language)
        
    def test_set_isocode(self):
        self.assertEquals(Language.objects.get(pk=1).isocode, self.lang1.isocode)
        self.assertEquals(Language.objects.get(pk=2).isocode, self.lang2.isocode)
    
    def test_set_slug(self):
        self.assertEquals(Language.objects.get(pk=1).slug, self.lang1.slug)
        self.assertEquals(Language.objects.get(pk=2).slug, self.lang2.slug)
        
    def test_set_information(self):
        self.assertEquals(Language.objects.get(pk=1).information, self.lang1.information)
        self.assertEquals(Language.objects.get(pk=2).information, self.lang2.information)

    def test_set_classification(self):
        self.assertEquals(Language.objects.get(pk=1).classification, self.lang1.classification)
        self.assertEquals(Language.objects.get(pk=2).classification, self.lang2.classification)
        
    def test_update(self):
        self.lang1.language = "C"
        self.lang1.save()
        self.assertEquals(Language.objects.get(pk=1).language, "C")
    
    def test_delete(self):
        # have got two things
        self.assertEquals(len(Language.objects.all()), 2)
        # delete one
        Language.objects.get(pk=1).delete()
        # now have one thing
        self.assertEquals(len(Language.objects.all()), 1)
        # now have the CORRECT one thing
        self.assertEquals(Language.objects.get(pk=2).language, self.lang2.language)
        # and we can't get the thing we deleted.
        with self.assertRaises(Language.DoesNotExist):
            Language.objects.get(pk=1)
    
    def test_blank_classification(self):
        l = Language.objects.get(pk=1)
        l.classification = None
        l.save()
        
    def test_blank_information(self):
        l = Language.objects.get(pk=1)
        l.information = None
        l.save()


class Test_LanguageAndFamily(TestCase):
    """Tests the Language Family Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='langb',
                                             information='i.2', classification='c, d, e',
                                             isocode='bbb', editor=self.editor)
        self.fam1 = Family.objects.create(family='F', slug='f', editor=self.editor)
        self.fam2 = Family.objects.create(family='G', slug='g', editor=self.editor)
        
    def test_adding_family(self):
        self.lang1.family.add(self.fam1)
        self.lang1.save()
        self.assertEquals(Language.objects.get(pk=self.lang1.id).family.all()[0].family, 'F')
        
    def test_multiple_families(self):
        self.lang1.family.add(self.fam1)
        self.lang1.family.add(self.fam2)
        self.lang1.save()
        
        db_obj = Language.objects.get(pk=self.lang1.id)
        self.assertEquals(db_obj.family.all()[0].family, 'F')
        self.assertEquals(db_obj.family.all()[1].family, 'G')
        
    def test_finding_language_via_family(self):
        self.lang1.family.add(self.fam1)
        self.lang1.save()
        self.lang2.family.add(self.fam1)
        self.lang2.save()
        
        f = Family.objects.get(pk=self.fam1.id)
        self.assertEquals(len(f.language_set.all()), 2)
        assert self.lang1 in f.language_set.all()
        assert self.lang2 in f.language_set.all()
        
        
        
        