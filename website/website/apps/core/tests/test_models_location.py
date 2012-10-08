from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from website.apps.core.models import Language, Location

class Test_Location(TestCase):
    """Tests the Location Model"""
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='b', 
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='a',
                                             isocode='bbb', editor=self.editor)
        Location.objects.create(language=self.lang1, longitude=130.1, 
                            latitude=80.2, editor=self.editor)
        Location.objects.create(language=self.lang2, longitude=90.9, 
                            latitude=10.3, editor=self.editor)
    
    def test_set_language(self):
        self.assertEquals(Location.objects.get(pk=1).language, self.lang1)
        self.assertEquals(Location.objects.get(pk=2).language, self.lang2)
        
    def test_set_longitude(self):
        self.assertEquals(Location.objects.get(pk=1).longitude, 130.1)
        self.assertEquals(Location.objects.get(pk=2).longitude, 90.9)
    
    def test_set_latitude(self):
        self.assertEquals(Location.objects.get(pk=1).latitude, 80.2)
        self.assertEquals(Location.objects.get(pk=2).latitude, 10.3)
        
    def test_update(self):
        # alter one
        o = Location.objects.get(pk=1)
        self.assertEquals(Location.objects.get(pk=1).language, self.lang1)
        o.language = self.lang2
        o.save()
        self.assertEquals(Location.objects.get(pk=1).language, self.lang2)
    
    def test_delete(self):
        # have got two things
        self.assertEquals(len(Location.objects.all()), 2)
        # delete one
        Location.objects.get(pk=1).delete()
        # now have one thing
        self.assertEquals(len(Location.objects.all()), 1)
        # now have the CORRECT one thing
        self.assertEquals(Location.objects.get(pk=2).language, self.lang2)
        # and we can't get the thing we deleted.
        with self.assertRaises(Location.DoesNotExist):
            Location.objects.get(pk=1)
    
    def test_error_on_empty_longitude(self):
        with self.assertRaises(IntegrityError):
            Location.objects.create(language=self.lang2, longitude=None, 
                                latitude=10.3, editor=self.editor)
                                
    def test_error_on_empty_latitude(self):
        with self.assertRaises(IntegrityError):
            Location.objects.create(language=self.lang2, longitude=90.9, 
                                latitude=None, editor=self.editor)
                                
    def test_error_on_empty_language(self):
        with self.assertRaises(ValueError):
            Location.objects.create(language=None, longitude=90.9, 
                                latitude=10.3, editor=self.editor)
                                
    def test_error_on_nonfloat_longitude(self):
        with self.assertRaises(ValueError):
            Location.objects.create(language=self.lang1, longitude='hello', 
                                latitude=10.3, editor=self.editor)
                                
    def test_error_on_nonfloat_latitude(self):
        with self.assertRaises(ValueError):
            Location.objects.create(language=self.lang1, longitude=90.9, 
                                latitude='hello', editor=self.editor)
    
    def test_get_locations_for_language(self):
        self.assertEquals(len(self.lang1.location_set.all()), 1)
        self.lang1.location_set.all()[0].latitude = 80.2
        self.lang1.location_set.all()[0].longitude = 130.1
        