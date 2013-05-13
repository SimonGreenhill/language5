from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Language, Source
from website.apps.pronouns.models import Paradigm, Pronoun
from website.apps.pronouns.tools import repr_row

# Mixin for default test content
class DefaultSettingsMixin(object):
    def add_fixtures(self):
        self.editor = User.objects.create_user('admin', 'admin@admin.com', "test")
        self.lang = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', 
                                             classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.source = Source.objects.create(year=1991, author='Smith', 
                                 slug='Smith1991', reference='S2',
                                 comment='c1', editor=self.editor)
        

# test tools.repr_row
class Test_Tools_repr_row(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
        self.pdm = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
    
    def test_obj(self):
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor,
                            number='sg', alignment="A", person="1", gender=None)
        assert repr_row(p) == "1st (excl) Person Singular"
    
    def test_dict(self):
        d = {
             'number': ('sg', 'Singular'), 
             'alignment': ('A', 'A'), 
             'person': ('1', '1st (excl) Person'),
             'gender': None,
        }
        assert repr_row(d) == "1st (excl) Person Singular"
        
    def test_obj_no_gender(self):
        p = Pronoun.objects.create(paradigm=self.pdm, editor=self.editor,
                            number='sg', alignment="A", person="1", gender="M")
        assert repr_row(p) == "1st (excl) Person Singular Masculine"
        
    def test_dict_no_gender(self):
        d = {
             'number': ('sg', 'Singular'), 
             'alignment': ('A', 'A'), 
             'person': ('1', '1st (excl) Person'),
             'gender': ('M', 'Masculine'),
        }
        assert repr_row(d) == "1st (excl) Person Singular Masculine"
        
    def test_no_errors(self):
        for row in Pronoun._generate_all_combinations():
            repr_row(row)


# test Paradigm
class Test_Paradigm(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
        
    def test_create(self):
        p = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test").save()
        del(p)
        p = Paradigm.objects.get(pk=1)
        assert p.language == self.lang
        assert p.source == self.source
        assert p.comment == 'test'
    
    def test_prefill(self):
        p = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        p.save()
        
        # make sure the correct number of pronouns is there..
        assert len(p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        # check the pronouns themselves...
        for comb in Pronoun._generate_all_combinations():
            queryset = Pronoun.objects.filter(
                paradigm = p,
                gender = None if comb['gender'] is None else comb['gender'][0],
                number = comb['number'][0],
                alignment = comb['alignment'][0],
                person = comb['person'][0]
            )
            assert len(queryset) == 1
        
        
    def test_partial_prefill(self):
        p = Paradigm.objects.create(language=self.lang, 
                                    source=self.source, 
                                    editor=self.editor,
                                    comment="test")
        p.save()
        # we should have a full complement. 
        assert len(p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        # Let's delete some...
        for pron in p.pronoun_set.all():
            if pron.alignment == 'A':
                pron.delete()
            else:
                # modify the stored entries so we can identify them later.
                pron.form = "old"
                pron.save()
            
        # how many should we have deleted
        missing = [_ for _ in Pronoun._generate_all_combinations() if _['alignment'][0] == 'A']
        assert len(p.pronoun_set.all()) == (len(Pronoun._generate_all_combinations()) - len(missing))
        
        # re-run prefill
        p._prefill_pronouns()
        
        # we should now have a full complement again.
        assert len(p.pronoun_set.all()) == len(Pronoun._generate_all_combinations())
        
        for pron in p.pronoun_set.all():
            if pron.alignment == 'A':
                assert pron.form == ''
            else:
                assert pron.form == 'old'
        
    
# Test View: Add paradigm
class Test_AddParadigmView(DefaultSettingsMixin, TestCase):
    
    def setUp(self):
        self.add_fixtures()
        self.url = reverse('pronouns:add')
        self.client = Client()
        self.client.login(username='admin', password='test')
        self.response = self.client.get(self.url)
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'pronouns/add.html')
    
    def test_fail_when_not_logged_in(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse("pronouns:add")))
        
    def test_paradigm_save(self):
        count = Paradigm.objects.count()
        response = self.client.post(self.url, {
            'language': self.lang.id, 'source': self.source.id, 'comment': 'foo'
        }, follow=True)
        self.assertEqual(Paradigm.objects.count(), count+1)
        self.assertContains(response, 'foo')
        
    def test_paradigm_creates_pronouns(self):
        count = Pronoun.objects.count()
        response = self.client.post(self.url, {
            'language': self.lang.id,
            'source': self.source.id,
            'comment': 'foo'
        }, follow=True)
        self.assertEqual(Pronoun.objects.count(), count+len(Pronoun._generate_all_combinations()))
        