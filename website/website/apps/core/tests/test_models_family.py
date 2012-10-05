from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from website.apps.core.models import Family

class Test_Family(TestCase):
    """Tests the Family Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        Family.objects.create(family='An', slug='s1', editor=self.editor)
        Family.objects.create(family='My', slug='s2', editor=self.editor)
    
    def test_set_family(self):
        self.assertEquals(Family.objects.get(pk=1).family, 'An')
        self.assertEquals(Family.objects.get(pk=2).family, 'My')
        
    def test_set_slug(self):
        self.assertEquals(Family.objects.get(pk=1).slug, 's1')
        self.assertEquals(Family.objects.get(pk=2).slug, 's2')
        
    def test_update(self):
        # alter one
        f = Family.objects.get(pk=1)
        f.family = 'tng'
        f.save()
        self.assertEquals(Family.objects.get(pk=1).family, 'tng')
    
    def test_delete(self):
        # have got two things
        self.assertEquals(len(Family.objects.all()), 2)
        # delete one
        Family.objects.get(pk=1).delete()
        # now have one thing
        self.assertEquals(len(Family.objects.all()), 1)
        # now have the CORRECT one thing
        self.assertEquals(Family.objects.get(pk=2).family, 'My')
        # and we can't get the thing we deleted.
        with self.assertRaises(Family.DoesNotExist):
            Family.objects.get(pk=1)
    
    def test_error_on_nonunique_family(self):
        with self.assertRaises(IntegrityError):
            Family.objects.create(family='My', slug='s3', editor=self.editor)
            
    def test_error_on_nonunique_slug(self):
        with self.assertRaises(IntegrityError):
            Family.objects.create(family='xx', slug='s2', editor=self.editor)
        
    def test_error_on_empty_family(self):
        with self.assertRaises(IntegrityError):
            Family.objects.create(family=None, slug='s3', editor=self.editor)

    def test_error_on_empty_slug(self):
        with self.assertRaises(IntegrityError):
            Family.objects.create(family='xx', slug=None, editor=self.editor)