from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from website.apps.core.models import Language, AlternateName

class Test_AlternateName(TestCase):
    """Tests the AlternateName Model"""
    
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.alt1 = AlternateName.objects.create(language=self.lang1, name='x',
                                             slug='x', editor=self.editor)

        self.lang2 = Language.objects.create(language='B', slug='langb',
                                          information='i.2', classification='c, d, e',
                                          isocode='bbb', editor=self.editor)
        self.alt2 = AlternateName.objects.create(language=self.lang2, name='y',
                                              slug='y', editor=self.editor)
        self.alt3 = AlternateName.objects.create(language=self.lang2, name='z',
                                            slug='z', editor=self.editor)
    
    def test_set_language(self):
        self.assertEquals(AlternateName.objects.get(pk=1).language, self.lang1)
        self.assertEquals(AlternateName.objects.get(pk=2).language, self.lang2)
        self.assertEquals(AlternateName.objects.get(pk=3).language, self.lang2)
        
    def test_set_name(self):
        self.assertEquals(AlternateName.objects.get(pk=1).name, 'x')
        self.assertEquals(AlternateName.objects.get(pk=2).name, 'y')
        self.assertEquals(AlternateName.objects.get(pk=3).name, 'z')
    
    def test_set_slug(self):
        self.assertEquals(AlternateName.objects.get(pk=1).slug, 'x')
        self.assertEquals(AlternateName.objects.get(pk=2).slug, 'y')
        self.assertEquals(AlternateName.objects.get(pk=3).slug, 'z')
    
    def test_get_altnames_for_language(self):
        self.assertEquals(self.lang1.alternatename_set.all()[0].name, 'x')
        self.assertEquals(self.lang2.alternatename_set.all()[0].name, 'y')
        self.assertEquals(self.lang2.alternatename_set.all()[1].name, 'z')
        
    def test_get_language_from_altname(self):
        self.assertEquals(self.alt1.language, self.lang1)
        self.assertEquals(self.alt2.language, self.lang2)
        self.assertEquals(self.alt3.language, self.lang2)
    
