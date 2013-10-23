from django.test import TestCase
from django.contrib.auth.models import User
from website.apps.core.templatetags.website_tags import link_ethnologue
from website.apps.core.templatetags.website_tags import link_olac
from website.apps.core.templatetags.website_tags import link_multitree
from website.apps.core.templatetags.website_tags import link_glottolog
from website.apps.core.templatetags.website_tags import link_llmap
from website.apps.core.templatetags.website_tags import lang_map
from website.apps.core.models import Language

class LanguageMixin(object):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.language = Language.objects.create(
                        language='A', slug='langa', 
                        information='i.1', classification='a, b',
                        isocode='aaa', editor=self.editor)
        

class Test_Link_Ethnologue(LanguageMixin, TestCase):
    def test(self):
        self.assertEqual(
            link_ethnologue(self.language), 
            "http://www.ethnologue.com/language/aaa"
        )
    def test_empty(self):
        self.assertEqual(link_ethnologue(""), "")
    
    def test_empty2(self):
        self.assertEqual(link_ethnologue(None), "")

    

class Test_Link_Olac(LanguageMixin, TestCase):
    def test(self):
        self.assertEqual(
            link_olac(self.language), 
            "http://search.language-archives.org/search.html?q=%s" % self.language.isocode
        )
    def test_empty(self):
        self.assertEqual(link_olac(""), "")

    def test_empty2(self):
        self.assertEqual(link_olac(None), "")
    

class Test_Link_Multitree(LanguageMixin, TestCase):
    def test(self):
        self.assertEqual(
            link_multitree(self.language), 
            "http://multitree.org/codes/%s" % self.language.isocode
        )
    def test_empty(self):
        self.assertEqual(link_multitree(""), "")

    def test_empty2(self):
        self.assertEqual(link_olac(None), "")
    


class Test_Link_LLMap(LanguageMixin, TestCase):
    def test(self):
        self.assertEqual(
            link_llmap(self.language), 
            "http://llmap.org/languages/%s.html" % self.language.isocode
        )
    def test_empty(self):
        self.assertEqual(link_llmap(""), "")

    def test_empty2(self):
        self.assertEqual(link_olac(None), "")


class Test_Link_Glottolog(LanguageMixin, TestCase):
    def test(self):
        self.assertEqual(
            link_glottolog(self.language), 
            "http://glottolog.org/resource/languoid/iso/%s" % self.language.isocode
        )
    def test_empty(self):
        self.assertEqual(link_glottolog(""), "")
    
    def test_empty2(self):
        self.assertEqual(link_olac(None), "")


class Test_Language_Map(LanguageMixin, TestCase):
    def test(self):
        self.assertEqual(
            lang_map(self.language), 
            '<img src="http://llmap.org/language/%s.png?width=%d&height=%d" alt="Map of %s: courtesy of LL-MAP" />' %
            (self.language.isocode, 400, 300, self.language.language)
        )
    def test_empty(self):
        self.assertEqual(lang_map(""), "")
    
    def test_empty2(self):
        self.assertEqual(lang_map(None), "")
        
    

