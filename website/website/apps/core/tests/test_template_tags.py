from django.test import TestCase
from django.contrib.auth.models import User
from website.apps.core.templatetags.website_tags import link_ethnologue
from website.apps.core.templatetags.website_tags import link_olac
from website.apps.core.templatetags.website_tags import link_multitree
from website.apps.core.templatetags.website_tags import link_glottolog
from website.apps.core.templatetags.website_tags import link_llmap
from website.apps.core.templatetags.website_tags import link_wikipedia
from website.apps.core.templatetags.website_tags import language_map
from website.apps.core.models import Language

class LanguageMixin(object):
    """
    Mixin for testing the various linking functions
    
    This will test if they handle empty/null values gracefully, and return the
    expected URL for a given isocode
    """
    function = None # Override in child functions
    expected = None # Override in child functions
    
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.language = Language.objects.create(
                        language='A', slug='langa', 
                        information='i.1', classification='a, b',
                        isocode='aaa', editor=self.editor)
    
    def test_empty(self):
        self.assertEqual(self.function(""), "")
        
    def test_null(self):
        self.assertEqual(self.function(None), "")
    
    def test_expected(self):
        f = self.function(self.language).strip()
        self.assertEqual(f, self.expected)
        

class Test_Link_Ethnologue(LanguageMixin, TestCase):
    function = staticmethod(link_ethnologue)
    expected = "http://www.ethnologue.com/language/aaa"


class Test_Link_Olac(LanguageMixin, TestCase):
    function = staticmethod(link_olac)
    expected = "http://search.language-archives.org/search.html?q=aaa"


class Test_Link_Multitree(LanguageMixin, TestCase):
    function = staticmethod(link_multitree)
    expected = "http://multitree.org/codes/aaa"


class Test_Link_LLMap(LanguageMixin, TestCase):
    function = staticmethod(link_llmap)
    expected = "http://llmap.org/languages/aaa.html"


class Test_Link_Glottolog(LanguageMixin, TestCase):
    function = staticmethod(link_glottolog)
    expected = "http://glottolog.org/resource/languoid/iso/aaa"


class Test_Link_Wikipedia(LanguageMixin, TestCase):
    function = staticmethod(link_wikipedia)
    expected = "https://en.wikipedia.org/wiki/ISO_639:aaa"


class Test_Language_Map(LanguageMixin, TestCase):
    function = staticmethod(language_map)
    expected = '<img src="http://llmap.org/language/aaa.png?width=400&height=300" alt="Map of A: courtesy of LL-MAP" />'


