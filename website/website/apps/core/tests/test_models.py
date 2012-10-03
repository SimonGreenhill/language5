from django.contrib.auth.models import User
from django.test import TestCase
from website.apps.core.models import Family, Language, AlternateNames, Links, Locations

class GenericCRUDTestMixin(object):
    """Generic tests of CRUD functionality"""
    vars = {}    # Override
    model = None # Override
    
    fields_to_skip = ['editor'] # fields to skip in update tests
    
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='admin')
        self.vars['editor'] = self.user
        self.model.objects.create(**self.vars)
    
    def test_create(self):
        in_db = self.model.objects.all()
        self.assertEquals(in_db.count(), 1)
        
        # check the values stored
        for k, v in self.vars.items():
            self.assertEquals(getattr(in_db[0], k), v)
    
    def test_update(self):
        obj = self.model.objects.all()[0]
        # permute
        for k, v in self.vars.items():
            if k not in self.fields_to_skip:
                setattr(obj, k, v[::-1]) # reverse
        obj.save()
        # get back from database and check the values stored
        obj = self.model.objects.all()[0]
        for k, v in self.vars.items():
            if k not in self.fields_to_skip:
                self.assertEquals(getattr(obj, k), v[::-1])
        
    def test_delete(self):
        obj = self.model.objects.all()[0]
        obj.delete()
        self.assertEquals(len(self.model.objects.all()), 0)


class GenericCRUDTestMixinWithLanguage(GenericCRUDTestMixin):
    
    fields_to_skip = ['editor', 'language']
    
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='admin')
        self.vars['editor'] = self.user
        self.vars['language'] = Language.objects.create(language="TestLang", 
                                                        slug="test",
                                                        isocode="xxx",
                                                        classification="a,b,c",
                                                        information="",
                                                        editor=self.vars['editor']
                                                        )
        self.model.objects.create(**self.vars)
  

        
class Test_Family(GenericCRUDTestMixin, TestCase):
    """Tests the Family Model"""
    
    vars = {
        'family': "Austronesian",
        'slug': 'austronesian'
    }
    
    model = Family


class Test_Language(GenericCRUDTestMixin, TestCase):
    """Tests the Language Model"""

    vars = {
        'language': "Maori",
        'slug': 'maori',
        'isocode': 'mri',
        'classification': 'aa, bb, cc',
        'information': "something",
        # ignore family
    }

    model = Language


class Test_AlternateNames(GenericCRUDTestMixinWithLanguage, TestCase):
    """Tests the AlternateNames Model"""

    vars = {
        'name': "NZ Maori",
        'slug': 'nzmaori',
    }

    model = AlternateNames
    

class Test_Links(GenericCRUDTestMixinWithLanguage, TestCase):
    """Tests the Links Model"""

    vars = {
        'link': "http://simon.net.nz",
        'description': 'good website',
    }

    model = Links


class Test_Locations(GenericCRUDTestMixinWithLanguage, TestCase):
    """Tests the Locations Model"""

    vars = {
        'longitude': 200,
        'latitude': 100,
    }

    model = Locations

    def test_update(self):
        obj = self.model.objects.all()[0]
        # permute
        for k, v in self.vars.items():
            if k not in self.fields_to_skip:
                setattr(obj, k, v+100) # reverse
        obj.save()
        # get back from database and check the values stored
        obj = self.model.objects.all()[0]
        for k, v in self.vars.items():
            if k not in self.fields_to_skip:
                self.assertEquals(getattr(obj, k), v+100)
