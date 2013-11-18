from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun, Relationship
from website.apps.pronouns.tests import DefaultSettingsMixin

class Test_Index(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
        self.url = reverse('pronouns:index')
        self.client = Client()
        self.response = self.client.get(self.url)
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'pronouns/index.html')
    
    def test_shows_paradigms(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Smith (1991)')
        


class Test_Detail(DefaultSettingsMixin, TestCase):
    def setUp(self):
        self.add_fixtures()
        
        # add some entries so we have something to see
        for counter, pron in enumerate(self.pdm.pronoun_set.all(), 1):
            lex = Lexicon.objects.create(
                editor=self.editor,
                language=self.lang,
                source=self.source,
                word=self.word,
                entry='fudge-%d' % counter
            )
            lex.save()
            pron.entries.add(lex)
            
        self.url = reverse('pronouns:detail', kwargs={'paradigm_id': 1})
        self.client = Client()
        self.response = self.client.get(self.url)
    
    def _create_relationship(self):
        "Simple helper function to add a relationship"
        p1, p2 = self.pdm.pronoun_set.all()[0:2]
        lexs = []
        for p in (p1, p2):
            lex = Lexicon.objects.create(
                editor=self.editor,
                language=self.lang,
                source=self.source,
                word=self.word,
                entry='fudge-%d' % p.id
            )
            lex.save()
            lexs.append(lex)
            p.entries.add(lex)
        
        rel = Relationship.objects.create(
            editor=self.editor,
            paradigm=self.pdm,
            pronoun1=p1, pronoun2=p2,
            relationship="TS",
            comment="a note"
        )
        rel.save()
        return rel
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'pronouns/detail.html')
    
    def test_language_in_content(self):
        self.assertContains(self.response, '/language/langa')
    
    def test_comment_in_content(self):
        self.assertContains(self.response, 'test')
        
    def test_content_rows(self):
        for p in self.pdm.pronoun_set.all():
            self.assertContains(self.response, full_repr_row(p))
    
    def test_content_values(self):
        for p in self.pdm.pronoun_set.all():
            self.assertContains(self.response, p.entries.all()[0].entry)
        
    def test_content_multiple_values(self):
        for counter, p in enumerate(self.pdm.pronoun_set.all(), 1):
            lex = Lexicon.objects.create(
                editor=self.editor,
                language=self.lang,
                source=self.source,
                word=self.word,
                entry='cake-%d' % counter
            )
            lex.save()
            p.entries.add(lex)
        
        response = self.client.get(self.url)
        for p in self.pdm.pronoun_set.all():
            for e in p.entries.all():
                self.assertContains(response, e.entry)
    
    def test_shows_relationships(self):
        """Should show defined relationships if present"""
        rel = self._create_relationship()
        assert self.pdm.relationship_set.count() == 1, \
            "I was expecting one relationship to be defined!"
        
        # re-call the view.
        response = self.client.get(self.url)
        import IPython; IPython.embed()
        
        # test
        assert response.context['relationship_table'] is not None, \
            "Template variable relationship_table should be initialised"
        self.assertContains(response, "Relationships")
        
    def test_hides_relationships(self):
        """Should NOT show relationships block if none are given"""
        assert self.pdm.relationship_set.count() == 0, \
            "I was expecting NO relationships to be defined!"
        self.assertNotContains(self.response, "Relationships")
        
    def test_relationship_details(self):
        rel = self._create_relationship()
        assert self.pdm.relationship_set.count() == 1, \
            "I was expecting one relationship to be defined!"
        
        # re-call the view.
        response = self.client.get(self.url)
        self.assertContains(response, "fudge-%d" % rel.pronoun1.id)
        self.assertContains(response, "fudge-%d" % rel.pronoun2.id)

        

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
        self.assertEqual(Pronoun.objects.count(), count+len(PronounType._generate_all_combinations()))
        
