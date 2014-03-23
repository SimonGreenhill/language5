from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.lexicon.tests import DataMixin, DataMixinLexicon
from website.apps.lexicon.models import Word, WordSubset, Lexicon


class Test_WordIndex(DataMixin, TestCase):
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
    
    def test_sorting(self):
        response = self.client.get(self.url, {'sort': 'fullword'})
        self.assertEquals(response.status_code, 200)
        for i, obj in enumerate([self.word1, self.word2, self.word3]):
            assert response.context['table'].rows[i].record == obj
        response = self.client.get(self.url, {'sort': '-fullword'})
        self.assertEquals(response.status_code, 200)
        for i, obj in enumerate([self.word3, self.word2, self.word1]):
            assert response.context['table'].rows[i].record == obj
    
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
    
    def test_sorting_invalid(self):
        response = self.client.get(self.url, {'sort': 'sausage'})
        for i, obj in enumerate([self.word1, self.word2, self.word3]):
            assert response.context['table'].rows[i].record == obj
    

class Test_WordDetail(DataMixinLexicon, TestCase):
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
    
    def test_sorting(self):
        url = reverse('word-detail', kwargs={'slug': self.word2.slug})
        response = self.client.get(url, {'sort': 'language'})
        for i, obj in enumerate([self.lexicon3, self.lexicon2]):
            assert response.context['table'].rows[i].record == obj
        response = self.client.get(url, {'sort': '-language'})
        for i, obj in enumerate([self.lexicon2, self.lexicon3]):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        url = reverse('word-detail', kwargs={'slug': self.word2.slug})
        response = self.client.get(url, {'sort': 'sausage'})
        for i, obj in enumerate([self.lexicon2, self.lexicon3]):
            assert response.context['table'].rows[i].record == obj


class Test_WordEdit(DataMixin, TestCase):
    def setUp(self):
        super(Test_WordEdit, self).setUp()
        self.lex1 = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="sausage",
            annotation=""
        )
        self.lex2 = Lexicon.objects.create(
            language=self.lang1, 
            word=self.word1,
            source=self.source1,
            editor=self.editor,
            entry="banana",
            annotation=""
        )
        self.items = [self.lex1, self.lex2]
        self.url = reverse('word-edit', kwargs={'slug': self.word1.slug})
    
    def get_post_data(self, objects):
        postdata = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'2',
            'form-MAX_NUM_FORMS': u'1000',
            'submit': 'true',
        }
        
        for i, obj in enumerate(objects):
            for k, v in obj.__dict__.items():
                if not k.startswith("_") and k not in ('added', 'editor_id', 'loan_source_id', 'loan'):
                    k = k.replace("_id", "")
                    postdata["form-%d-%s" % (i, k)] = v
        return postdata
    
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
        self.assertTemplateUsed(response, 'lexicon/word_edit.html')
    
    def test_error_on_missing(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(reverse('word-edit', kwargs={'slug': 'sausage'}))
        self.assertEquals(response.status_code, 404)
        
    def test_get(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'sausage' in response.content
        assert 'banana' in response.content
        
    def test_post(self):
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        response = self.client.post(self.url, postdata, follow=True)
        self.assertRedirects(response, reverse('word-detail', 
                                    kwargs={'slug': self.word1.slug}),
                                    status_code=302, target_status_code=200)
        self.assertEquals(response.status_code, 200)
        assert 'sausage' in response.content
        assert 'banana' in response.content
    
    def test_update_entry(self):
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        postdata['form-0-entry'] = 'apricot' # replace 'sausage' with 'apricot'
        response = self.client.post(self.url, postdata, follow=True)
        self.assertRedirects(response, reverse('word-detail', 
                                    kwargs={'slug': self.word1.slug}),
                                    status_code=302, target_status_code=200)
        self.assertEquals(response.status_code, 200)
        assert 'apricot' in response.content
        assert 'banana' in response.content
        assert 'sausage' not in response.content
        
    def test_update_editor(self):
        from django.contrib.auth.models import User
        newuser = User.objects.create_user('dave', 'dave@example.com', 'secret')
        self.client.login(username="dave", password="secret")
        postdata = self.get_post_data(self.items)
        postdata['form-0-entry'] = 'apricot' # replace 'sausage' with 'apricot'
        response = self.client.post(self.url, postdata, follow=True)
        self.assertEquals(response.status_code, 200)
        assert Lexicon.objects.get(pk=self.lex1.id).editor == newuser, "Have not updated editor!"
        
    def test_update_added(self):
        added = self.lex1.added
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        postdata['form-0-entry'] = 'apricot' # replace 'sausage' with 'apricot'
        response = self.client.post(self.url, postdata, follow=True)
        now = Lexicon.objects.get(pk=self.lex1.id).added
        assert now > added, "%r is not larger than %r" % (now, added)
        
    def test_create_revision(self):
        import reversion
        version_list = reversion.get_for_object(self.lex1)
        assert len(version_list) == 0
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        postdata['form-0-entry'] = 'apricot' # replace 'sausage' with 'apricot'
        response = self.client.post(self.url, postdata, follow=True)
        version_list = reversion.get_for_object(self.lex1)
        assert len(version_list) == 1

