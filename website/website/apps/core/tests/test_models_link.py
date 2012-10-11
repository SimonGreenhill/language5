from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from website.apps.core.models import Language, Link

class Test_Link(TestCase):
    """Tests the Link Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='b', 
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='a',
                                             isocode='bbb', editor=self.editor)
        Link.objects.create(language=self.lang1, link="http://simon.net.nz", 
                            description="My Website", editor=self.editor)
        Link.objects.create(language=self.lang2, link="http://transnewguinea.org", 
                            description="TNG.org", editor=self.editor)
    
    def test_set_language(self):
        self.assertEquals(Link.objects.get(pk=1).language, self.lang1)
        self.assertEquals(Link.objects.get(pk=2).language, self.lang2)
        
    def test_set_link1(self):
        self.assertEquals(Link.objects.get(pk=1).link, 'http://simon.net.nz')
        self.assertEquals(Link.objects.get(pk=2).link, 'http://transnewguinea.org')
    
    def test_set_link2(self):
        self.assertEquals(Link.objects.get(pk=1).description, 'My Website')
        self.assertEquals(Link.objects.get(pk=2).description, 'TNG.org')
        
    def test_update(self):
        # alter one
        o = Link.objects.get(pk=1)
        self.assertEquals(Link.objects.get(pk=1).language, self.lang1)
        o.language = self.lang2
        o.save()
        self.assertEquals(Link.objects.get(pk=1).language, self.lang2)
    
    def test_delete(self):
        # have got two things
        self.assertEquals(len(Link.objects.all()), 2)
        # delete one
        Link.objects.get(pk=1).delete()
        # now have one thing
        self.assertEquals(len(Link.objects.all()), 1)
        # now have the CORRECT one thing
        self.assertEquals(Link.objects.get(pk=2).language, self.lang2)
        # and we can't get the thing we deleted.
        with self.assertRaises(Link.DoesNotExist):
            Link.objects.get(pk=1)
    
    def test_error_on_empty_link(self):
        with self.assertRaises(IntegrityError):
            Link.objects.create(language=self.lang1, link=None, 
                                description="My Website", editor=self.editor)

    def test_error_on_empty_description(self):
        with self.assertRaises(IntegrityError):
            Link.objects.create(language=self.lang1, link="http://simon.net.nz", 
                                description=None, editor=self.editor)
    
    def test_get_all_links_for_language(self):
        lang = Language.objects.create(language='Test', slug='test',
                                       isocode='ttt', editor=self.editor)
        links = [      
            Link.objects.create(language=lang, link="http://a.com", 
                                description="A", editor=self.editor),
            Link.objects.create(language=lang, link="http://b.com", 
                                description="B", editor=self.editor),
            Link.objects.create(language=lang, link="http://c.com", 
                                description="C", editor=self.editor),
        ]
        db_links = lang.link_set.all()
        self.assertEquals(len(db_links), len(links))
        for db_link in db_links:
            assert db_link in links
        