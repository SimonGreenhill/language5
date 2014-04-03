from django.contrib.auth.models import User
from django.test import TestCase
from website.apps.core.models import Language, Source

class Test_Language(TestCase):
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


class Test_Source(TestCase):
    """Tests the Source Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
    
    def test_simple(self):
        s = Source.objects.create(year="1991", author='Smith', 
                                    slug='Smith1991', reference='S2',
                                    comment='c1', editor=self.editor)
        self.assertEquals(s.__unicode__(), "%s (%s)" % (s.author, s.year))

    def test_noyear(self):
        s = Source.objects.create(year=None, author='Smith', 
                                    slug='Smith1991', reference='S2',
                                    comment='c1', editor=self.editor)
        self.assertEquals(s.__unicode__(), s.author)