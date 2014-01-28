from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from test_models import TestSetup
from website.apps.lexicon.models import Word, WordSubset, Lexicon

class Test_WordIndex(TestSetup, TestCase):
    """Tests the Word Index page"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('word-index')
        super(Test_WordIndex, self).setUp()
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'lexicon/word_index.html')
    
    def test_get_all_words(self):
        # just getting the words index should get all words.
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 3)
    
    def test_get_has_subsets(self):
        # page should have subsets listed
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['subsets']), 3)
        self.assertEquals(len(response.context['subsets']), len(WordSubset.objects.all()))
        
    def test_get_no_subset_context_is_none(self):
        # if there's no subset requested then the var `subset` will be None
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['subset'], None)
        
    def test_get_subset(self):
        # if a subset is requested...
        response = self.client.get(self.url, {'subset': 'numbers'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'].slug, 'numbers')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 2)
        
    def test_get_empty_subset(self):
        # if a subset is requested...
        response = self.client.get(self.url, {'subset': 'nothing'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'].slug, 'nothing')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 0)
        
    def test_invalid_subset_raises_404(self):
        response = self.client.get(self.url, {'subset': 'fudge'})
        self.assertEquals(response.status_code, 404)
    
    def test_ordering_on_count(self):
        response = self.client.get(self.url, {'sort': 'count'})
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 3)
    
    def test_ordering_on_fullword(self):
        # just getting the words index should get all words.
        response = self.client.get(self.url, {'sort': 'fullword'})
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 3)
    

class Test_WordDetail(TestSetup, TestCase):
    def test_200ok(self):
        response = self.client.get(reverse('word-detail', kwargs={'slug': self.word1.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_template(self):
        response = self.client.get(reverse('word-detail', kwargs={'slug': self.word1.slug}))
        self.assertTemplateUsed(response, 'lexicon/word_detail.html')
    
    def test_get_all_words(self):
        url = reverse('word-detail', kwargs={'slug': self.word1.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 1)
        
    def test_get_all_words_two(self):
        url = reverse('word-detail', kwargs={'slug': self.word2.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 2)

    def test_bad_paginator(self):
        response = self.client.get('/word/hand?page=10000')
        self.assertEqual(response.status_code, 404)
        
    def test_bad_nonint_paginator(self):
        response = self.client.get('/word/hand?page=banana')
        self.assertEqual(response.status_code, 404)


class Test_LexiconDetail(TestSetup, TestCase):
    def setUp(self):
        super(Test_LexiconDetail, self).setUp()
        self.lex = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="sausage",
            annotation="eggs"
        )
        self.url = reverse('lexicon-detail', kwargs={'pk': self.lex.id})
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'lexicon/lexicon_detail.html')
    
    def test_get_missing(self):
        response = self.client.get(reverse('lexicon-detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)
    
    def test_get_data(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'sausage' in response.content
        assert 'eggs' in response.content
        

class Test_LexiconEdit(TestSetup, TestCase):
    def setUp(self):
        super(Test_LexiconEdit, self).setUp()
        self.lex = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="sausage",
            annotation="eggs"
        )
        self.url = reverse('lexicon-edit', kwargs={'pk': self.lex.id})
    
    def get_post_data(self, obj):
        return dict(
            [(k.replace("_id", ""),v) for k,v in obj.__dict__.items() \
                if not k.startswith("_") and k not in ('added', 'editor_id', 'loan_source_id', 'loan')
            ]
        )
        
    
    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=%s" % self.url, 
                                    status_code=302, target_status_code=200)
        
    def test_200ok_logged_in(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_template(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'lexicon/lexicon_edit.html')
    
    def test_error_on_missing(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(reverse('lexicon-detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)
        
    def test_get(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'sausage' in response.content
        assert 'eggs' in response.content
        
    def test_post(self):
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.lex)
        postdata['entry'] = 'banana'
        response = self.client.post(self.url, postdata, follow=True)
        self.assertEquals(response.status_code, 200)
        assert 'banana' in response.content
        assert 'sausage' not in response.content
        assert 'eggs' in response.content
        
    def test_update_editor(self):
        from django.contrib.auth.models import User
        assert self.lex.editor == self.editor
        newuser = User.objects.create_user('dave', 'dave@example.com', 'secret')
        self.client.login(username="dave", password="secret")
        response = self.client.post(self.url, self.get_post_data(self.lex), follow=True)
        self.assertEquals(response.status_code, 200)
        assert Lexicon.objects.get(pk=self.lex.id).editor == newuser, "Have not updated editor!"
        
    def test_update_added(self):
        added = self.lex.added
        self.client.login(username="admin", password="test")
        response = self.client.post(self.url, self.get_post_data(self.lex), follow=True)
        now = Lexicon.objects.get(pk=self.lex.id).added
        assert now > added, "%r is not larger than %r" % (now, added)
        
    def test_create_revision(self):
        import reversion
        version_list = reversion.get_for_object(self.lex)
        assert len(version_list) == 0
        self.client.login(username="admin", password="test")
        response = self.client.post(self.url, self.get_post_data(self.lex), follow=True)
        version_list = reversion.get_for_object(self.lex)
        assert len(version_list) == 1
    
    