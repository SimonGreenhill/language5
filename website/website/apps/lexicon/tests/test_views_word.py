from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from website.apps.lexicon.tests import DataMixin
from website.apps.lexicon.models import WordSubset, Lexicon

from website.apps.core.tests.utils import PaginatorTestMixin

class Test_WordIndex(DataMixin, PaginatorTestMixin, TestCase):
    """Tests the Word Index page"""
    
    @classmethod
    def setUpTestData(cls):
        super(Test_WordIndex, cls).setUpTestData()
        cls.client = Client()
        cls.url = reverse('word-index')
        cls.response = cls.client.get(cls.url)

    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'lexicon/word_index.html')

    def test_get_all_words(self):
        # just getting the words index should get all words.
        assert 'table' in self.response.context
        self.assertEquals(len(self.response.context['table'].rows), 3)

    def test_get_has_subsets(self):
        # page should have subsets listed
        self.assertEquals(len(self.response.context['subsets']), 3)
        self.assertEquals(
            len(self.response.context['subsets']),
            WordSubset.objects.count()
        )
    
    def test_get_renders_subsets_correctly(self):
        assert b'<a href="/word/?subset=all">' in self.response.content
    
    def test_get_no_subset_context_is_none(self):
        # if there's no subset requested then the var `subset` will be None
        self.assertEquals(self.response.context['subset'], None)

    def test_get_subset(self):
        # if a subset is requested...
        response = self.client.get(self.url, {'subset': 'numbers'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'], 'numbers')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 2)

    def test_get_letter(self):
        # if a letter is requested...
        response = self.client.get(self.url, {'subset': 'H'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'], 'H')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 1)
        assert response.context['table'].rows[0].record == self.word1

    def test_get_empty_subset(self):
        # if a subset is requested...
        response = self.client.get(self.url, {'subset': 'nothing'})
        # ... then the var `subset` will be the same as the GET request
        self.assertEquals(response.context['subset'], 'nothing')
        # ...and the number of words will change.
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 0)

    def test_invalid_subset_is_empty(self):
        response = self.client.get(self.url, {'subset': 'fudge'})
        self.assertEquals(response.context['subset'], 'fudge')
        assert 'table' in response.context
        self.assertEquals(len(response.context['table'].rows), 0)

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


class Test_WordDetail(DataMixin, PaginatorTestMixin, TestCase):

    def setUp(self):
        super(Test_WordDetail, self).setUp()
        self.url = reverse('word-detail', kwargs={'slug': self.word1.slug})
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'lexicon/word_detail.html')

    def test_get_all_words(self):
        response = self.client.get(self.url)
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
    @classmethod
    def setUpTestData(cls):
        super(Test_WordEdit, cls).setUpTestData()
        cls.lex1 = Lexicon.objects.create(
            language=cls.lang1,
            word=cls.word1,
            source=cls.source1,
            editor=cls.editor,
            entry="sausage",
            annotation=""
        )
        cls.lex2 = Lexicon.objects.create(
            language=cls.lang1,
            word=cls.word1,
            source=cls.source1,
            editor=cls.editor,
            entry="banana",
            annotation=""
        )
        cls.items = [cls.lex1, cls.lex2]
        cls.url = reverse('word-edit', kwargs={'slug': cls.word1.slug})

    def get_post_data(self, objects):
        postdata = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'2',
            'form-MAX_NUM_FORMS': u'1000',
            'submit': 'true',
        }
        skip = ('added', 'editor_id', 'loan_source_id', 'loan')
        
        for i, obj in enumerate(objects):
            for k, v in obj.__dict__.items():
                if not k.startswith("_") and k not in skip:
                    k = k.replace("_id", "")
                    postdata["form-%d-%s" % (i, k)] = v
        return postdata

    def test_error_on_notlogged_in(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=%s" % self.url,
            status_code=302, target_status_code=200
        )

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
        response = self.client.get(
            reverse('word-edit', kwargs={'slug': 'sausage'})
        )
        self.assertEquals(response.status_code, 404)

    def test_get(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert b'sausage' in response.content
        assert b'banana' in response.content
    
    def test_post(self):
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        response = self.client.post(self.url, postdata, follow=True)
        # redirects?
        redir_url = reverse('word-detail', kwargs={'slug': self.word1.slug})
        self.assertRedirects(
            response, redir_url, status_code=302, target_status_code=200
        )
        self.assertEquals(response.status_code, 200)
        # updated?
        assert b'sausage' in response.content
        assert b'banana' in response.content

    def test_update_entry(self):
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        # replace 'sausage' with 'apricot'
        postdata['form-0-entry'] = 'apricot'
        response = self.client.post(self.url, postdata, follow=True)
        # redirects?
        redir_url = reverse('word-detail', kwargs={'slug': self.word1.slug})
        self.assertRedirects(
            response, redir_url, status_code=302, target_status_code=200
        )
        self.assertEquals(response.status_code, 200)
        # updated?
        assert b'apricot' in response.content
        assert b'banana' in response.content
        assert b'sausage' not in response.content

    def test_update_editor(self):
        newuser = User.objects.create_user(
            'dave', 'dave@example.com', 'secret'
        )
        self.client.login(username="dave", password="secret")
        postdata = self.get_post_data(self.items)
        # replace 'sausage' with 'apricot'
        postdata['form-0-entry'] = 'apricot'
        response = self.client.post(self.url, postdata, follow=True)
        self.assertEquals(response.status_code, 200)
        
        if Lexicon.objects.get(pk=self.lex1.id).editor != newuser:
            raise AssertionError("Have not updated editor!")

    def test_update_added(self):
        added = self.lex1.added
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        # replace 'sausage' with 'apricot'
        postdata['form-0-entry'] = 'apricot'
        self.client.post(self.url, postdata, follow=True)
        now = Lexicon.objects.get(pk=self.lex1.id).added
        assert now > added, "%r is not larger than %r" % (now, added)

    def test_create_revision(self):
        from reversion.models import Version
        version_list = Version.objects.get_for_object(self.lex1)
        assert len(version_list) == 0
        self.client.login(username="admin", password="test")
        postdata = self.get_post_data(self.items)
        # replace 'sausage' with 'apricot'
        postdata['form-0-entry'] = 'apricot'
        self.client.post(self.url, postdata, follow=True)
        version_list = Version.objects.get_for_object(self.lex1)
        assert len(version_list) == 1

