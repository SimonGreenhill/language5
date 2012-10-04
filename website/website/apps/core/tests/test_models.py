from django.contrib.auth.models import User
from django.test import TestCase
from website.apps.core.models import Family, Language, Source, Note
from website.apps.core.models import AlternateNames, Links, Locations

class GenericCRUDTestMixin(object):
    """Generic tests of CRUD functionality"""
    vars = {}    # Override
    model = None # Override
    
    def _permute(self, value):
        if isinstance(value, (str, unicode)):
            return value[::-1]
        elif isinstance(value, (int, float)):
            return value + 1
        else:
            return value
        
    def setUp(self):
        self.vars['editor'], created = User.objects.get_or_create(username='admin')
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
            setattr(obj, k, self._permute(v)) # change the varible somehoe
        obj.save()
        # get back from database and check the values stored
        obj = self.model.objects.all()[0]
        for k, v in self.vars.items():
            self.assertEquals(getattr(obj, k), self._permute(v))
        
    def test_delete(self):
        obj = self.model.objects.all()[0]
        obj.delete()
        self.assertEquals(len(self.model.objects.all()), 0)


class GenericCRUDTestMixinWithLanguage(GenericCRUDTestMixin):
    
    def setUp(self):
        if 'editor' not in self.vars:
            self.vars['editor'], created = User.objects.get_or_create(username='admin')
        self.vars['language'] = Language.objects.create(language="TestLang", 
                                                        slug="test",
                                                        isocode="xxx",
                                                        classification="a,b,c",
                                                        information="",
                                                        editor=self.vars['editor']
                                                        )
        super(GenericCRUDTestMixinWithLanguage, self).setUp()
        
class GenericCRUDTestMixinWithSource(GenericCRUDTestMixin):

    def setUp(self):
        if 'editor' not in self.vars:
            self.vars['editor'], created = User.objects.get_or_create(username='admin')
        self.vars['source'] = Source.objects.create(year=1999, 
                                                        slug='greenhill2001',
                                                        author='Greenhill et al.',
                                                        reference='',
                                                        comment='',
                                                        editor=self.vars['editor']
                                                        )
        super(GenericCRUDTestMixinWithSource, self).setUp()



class Test_Family(GenericCRUDTestMixin, TestCase):
    """Tests the Family Model"""
    vars = {
        'family': 'Austronesian',
        'slug': 'austronesian'
    }
    model = Family



class Test_Source(GenericCRUDTestMixin, TestCase):
    """Tests the Source Model"""
    vars = {
        'year': 1999,
        'author': 'Greenhill et al.',
        'slug': 'greenhill1999',
        'reference': 'Greenhill, S. J. & Author, A. 1999. Interesting paper. Good Journal, 1:2-10',
        'comment': 'A very good paper'
    }
    model = Source
    
    def test_repr(self):
        """Test source's special handling of repr"""
        s = Source.objects.get(pk=1)
        self.assertEquals(unicode(s), "%s (%d)" % (self.vars['author'], self.vars['year']))
        s.year = None
        self.assertEquals(unicode(s), self.vars['author'])
        



class Test_Language(GenericCRUDTestMixin, TestCase):
    """Tests the Language Model"""
    vars = {
        'language': 'Maori',
        'slug': 'maori',
        'isocode': 'mri',
        'classification': 'aa, bb, cc',
        'information': 'something',
        # ignore family
    }
    model = Language



class Test_Notes(GenericCRUDTestMixinWithSource, GenericCRUDTestMixinWithLanguage, TestCase):
    """Tests the Notes Model"""
    vars = {
        'note': 'a note', 
        'location': 'p.1',
    }
    model = Note
        

class Test_AlternateNames(GenericCRUDTestMixinWithLanguage, TestCase):
    """Tests the AlternateNames Model"""
    vars = {
        'name': 'NZ Maori',
        'slug': 'nzmaori',
    }
    model = AlternateNames
    

class Test_Links(GenericCRUDTestMixinWithLanguage, TestCase):
    """Tests the Links Model"""
    vars = {
        'link': 'http://simon.net.nz',
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

