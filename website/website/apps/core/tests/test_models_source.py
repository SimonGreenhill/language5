from django.contrib.auth.models import User
from django.test import TestCase
from website.apps.core.models import Source

class Test_Source(TestCase):
    """Tests the Source Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.source1 = Source.objects.create(year=1991, author='Smith', 
                                    slug='Smith1991', reference='S2',
                                    comment='c1', editor=self.editor)
        self.source2 = Source.objects.create(year=2002, author='Jones', 
                                    slug='Jones2002', reference='J2',
                                    comment='c2', editor=self.editor)
    
    def test_set_year(self):
        self.assertEquals(Source.objects.get(pk=1).year, 1991)
        self.assertEquals(Source.objects.get(pk=2).year, 2002)
    
    def test_set_year_to_none(self):
        self.source1.year = None
        self.source1.save()
        
    def test_fail_on_nonyear(self):
        self.source1.year = 'aaa'
        with self.assertRaises(ValueError):
            self.source1.save()
    
    def test_set_author(self):
        self.assertEquals(Source.objects.get(pk=1).author, 'Smith')
        self.assertEquals(Source.objects.get(pk=2).author, 'Jones')
    
    def test_set_slug(self):
        self.assertEquals(Source.objects.get(pk=1).slug, 'Smith1991')
        self.assertEquals(Source.objects.get(pk=2).slug, 'Jones2002')
        
    def test_set_reference(self):
        self.assertEquals(Source.objects.get(pk=1).reference, 'S2')
        self.assertEquals(Source.objects.get(pk=2).reference, 'J2')
    
    def test_set_comment(self):
        self.assertEquals(Source.objects.get(pk=1).comment, 'c1')
        self.assertEquals(Source.objects.get(pk=2).comment, 'c2')
    
    def test_comment_can_be_blank(self):
        self.source1.comment = None
        self.source1.save()
        
    def test_delete(self):
        # have got two things
        self.assertEquals(len(Source.objects.all()), 2)
        # delete one
        Source.objects.get(pk=1).delete()
        # now have one thing
        self.assertEquals(len(Source.objects.all()), 1)
        # now have the CORRECT one thing
        self.assertEquals(Source.objects.get(pk=2).year, 2002)
        # and we can't get the thing we deleted.
        with self.assertRaises(Source.DoesNotExist):
            Source.objects.get(pk=1)
    
    def test_repr(self):
        """Test source's special handling of repr"""
        s = Source.objects.get(pk=1)
        self.assertEquals(s.__unicode__(), "%s (%d)" % (self.source1.author, self.source1.year))
        s.year = None
        self.assertEquals(s.__unicode__(), self.source1.author)