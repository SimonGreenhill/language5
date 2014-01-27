# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task, Wordlist, WordlistMember
from website.apps.entry.dataentry import available_views
from website.apps.entry.views import decode_checkpoint

class WordlistMixin(TestCase):
    def setUp(self, *args):
        self.client = Client()
        self.editor = User.objects.create_user('admin',
                                               'admin@example.com', "test")
        self.source = Source.objects.create(
                year=1991,
                author='Smith',
                slug='Smith1991',
                reference='S2',
                comment='c1',
                editor=self.editor
        )
        self.lang = Language.objects.create(language='A', slug='langa', 
            information='i.1', classification='a, b',
            isocode='aaa', editor=self.editor)
        
        self.words = []
        self.words_in_wordlist = []
        self.wordlist = Wordlist.objects.create(name="test", editor=self.editor)
        for i in range(5):
            w = Word.objects.create(
                editor=self.editor, 
                word="WORD %d" % i,
                slug=str(i)
            )
            self.words.append(w)
            # BUT only add the first 3 words to wordlist
            if i < 3:
                m = WordlistMember(wordlist=self.wordlist, word=w, order=i)
                m.save()
                self.words_in_wordlist.append(w)
                
        self.task = Task.objects.create(
            editor=self.editor,
            name="Test Task",
            description="A Test of Data Entry",
            source=self.source,
            wordlist=self.wordlist,
            done=False,
            view="WordlistView",
            records=1, 
        )
        
        # for formset validation
        self.form_data = {
            'form-TOTAL_FORMS': u'3',
            'form-INITIAL_FORMS': u'3',
            'form-MAX_NUM_FORMS': u'1000',
            # form 0
            'form-0-language': self.lang.id,
            'form-0-source': self.source.id,
            'form-0-word': self.words[0].id,
            'form-0-entry': 'entry-0',
            'form-0-annotation': 'comment-0',
            # form 1
            'form-1-language': self.lang.id,
            'form-1-source': self.source.id,
            'form-1-word': self.words[1].id,
            'form-1-entry': 'entry-1',
            'form-1-annotation': 'comment-1',
            # form 2
            'form-2-language': self.lang.id,
            'form-2-source': self.source.id,
            'form-2-word': self.words[2].id,
            'form-2-entry': 'entry-2',
            'form-2-annotation': 'comment-2',
            'submit': 'true',
        }
        # and for partial validation...
        self.bad_form_data = self.form_data.copy()
        del(self.bad_form_data['form-2-language'])


class TestWordlist(WordlistMixin):
    def test_create_wordlist(self):
        assert len(self.wordlist.words.all()) == 3
    
    def test_wordlist_overrides_records_in_model(self):
        """
        Tests that the number of records is set to the number of items
        """
        assert self.task.records == self.wordlist.words.count()
        m = WordlistMember(wordlist=self.wordlist, word=self.words[0], order=5) # add another
        m.save()
        self.task.save() # need to save to update.
        assert self.task.records == len(self.wordlist.words.all())


class Test_WordlistView(WordlistMixin):
    """Tests the WordlistView Detail Page"""
    
    def test_template_used(self):
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        self.assertTemplateUsed(response, 'entry/detail.html')
    
    def test_wordlist_overrides_records(self):
        """
        Tests that the number of items in a wordlist is used instead of 
        number of records
        """
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        assert len(response.context['formset'].forms) == 3, "Should get 3 forms in formset"
        
    def test_wordlist_only_shows_words_in_list(self):
        """Tests WordlistView only shows words in wordlist"""
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        words = [f.initial['word'] for f in response.context['formset'].forms]
        assert len(words) == 3, "Expecting 3 words not %d" % len(words)
        for word in words:
            assert word in self.words_in_wordlist
        
    def test_wordlist_ordering(self):
        """Tests WordlistView handles ordering correctly"""
        self.client.login(username="admin", password="test")
        response = self.client.get(self.task.get_absolute_url())
        for form_id, word in enumerate(self.wordlist.words.all()):
            assert response.context['formset'].forms[form_id].initial['word'] == word
        
    def test_wordlist_checkpoints(self):
        """Test WordlistView checkpoints correctly"""
        self.client.login(username="admin", password="test")
        response = self.client.post(self.task.get_absolute_url(), self.bad_form_data)
        self.assertEqual(response.status_code, 200)
        
        # does task have a checkpoint?
        assert Task.objects.get(pk=self.task.pk).checkpoint
        # can we reload it? 
        response = self.client.get(self.task.get_absolute_url())
        formdata = [f.clean() for f in response.context['formset'].forms]
        
        # and is it correct?
        for i in range(len(self.words_in_wordlist)):
            assert formdata[i]['entry'] == 'entry-%d' % i
            assert formdata[i]['annotation'] == 'comment-%d' % i
            assert formdata[i]['word'] == self.words_in_wordlist[i]
        
    def test_wordlist_saves(self):
        """Test WordlistView saves correctly"""
        self.client.login(username="admin", password="test")
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/done.html')
        # is task completed
        assert Task.objects.get(pk=self.task.pk).done
        
        # have we got three entries saved correctly? 
        for i, w in enumerate(self.wordlist.words.all()):
            found = Lexicon.objects.filter(word=w)
            assert found[0].entry == 'entry-%d' % i
            assert found[0].annotation == 'comment-%d' % i
            assert found[0].language == self.lang
            assert found[0].source == self.source
        
    def test_wordlist_handles_extras_in_view(self):
        """Tests WordlistView handles extra things appropriately in view"""
        self.client.login(username="admin", password="test")
        # add extra row to form_data
        self.bad_form_data['form-3-language'] = self.lang.id
        self.bad_form_data['form-3-source'] = self.source.id
        self.bad_form_data['form-3-word'] = self.words_in_wordlist[0].id
        self.bad_form_data['form-3-entry'] = 'entry-3'
        self.bad_form_data['form-3-annotation'] = 'comment-3'
        self.bad_form_data['form-TOTAL_FORMS'] =  u'4'
        
        # post...
        response = self.client.post(self.task.get_absolute_url(), self.bad_form_data)
        self.assertEqual(response.status_code, 200)
        
        # does task have a checkpoint?
        assert Task.objects.get(pk=self.task.pk).checkpoint
        # can we reload it? 
        response = self.client.get(self.task.get_absolute_url())
        formdata = [f.clean() for f in response.context['formset'].forms]
        
        assert len(formdata) == 4, "Expected four forms in formset"
        
        # and is it correct?
        for i in range(4):
            assert formdata[i]['entry'] == 'entry-%d' % i
            assert formdata[i]['annotation'] == 'comment-%d' % i
            if i == 3:
                expected_word = self.words_in_wordlist[0]
            else:
                expected_word = self.words_in_wordlist[i]
            assert formdata[i]['word'] == expected_word
        
    def test_wordlist_handles_extras_in_checkpoint_load(self):
        """Tests WordlistView handles extra things appropriately on checkpoint load"""
        self.client.login(username="admin", password="test")

        self.bad_form_data['form-3-language'] = self.lang.id
        self.bad_form_data['form-3-source'] = self.source.id
        self.bad_form_data['form-3-word'] = self.words_in_wordlist[0].id
        self.bad_form_data['form-3-entry'] = 'entry-3'
        self.bad_form_data['form-3-annotation'] = 'comment-3'
        self.bad_form_data['form-TOTAL_FORMS'] =  u'4'
        
        # post...
        response = self.client.post(self.task.get_absolute_url(), self.bad_form_data)
        
        # does task have a checkpoint?
        assert Task.objects.get(pk=self.task.pk).checkpoint
        
        # come back again later.
        del(self.client)
        newclient = Client()
        newclient.login(username="admin", password="test")
        response = newclient.get(self.task.get_absolute_url())
        
        formdata = [f.clean() for f in response.context['formset'].forms]
        assert len(formdata) == 4, "Expected four forms in formset"
        
        # and is it correct?
        for i in range(4):
            assert formdata[i]['entry'] == 'entry-%d' % i
            assert formdata[i]['annotation'] == 'comment-%d' % i
            if i == 3:
                expected_word = self.words_in_wordlist[0]
            else:
                expected_word = self.words_in_wordlist[i]
            assert formdata[i]['word'] == expected_word

        
    def test_wordlist_handles_extras_on_save(self):
        """Tests WordlistView handles extra things appropriately on save"""
        self.client.login(username="admin", password="test")
        
        self.form_data['form-3-language'] = self.lang.id
        self.form_data['form-3-source'] = self.source.id
        self.form_data['form-3-word'] = self.words_in_wordlist[0].id
        self.form_data['form-3-entry'] = 'entry-3'
        self.form_data['form-3-annotation'] = 'comment-3'
        self.form_data['form-TOTAL_FORMS'] =  u'4'
        
        # post...
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'entry/done.html')
        # is task completed
        assert Task.objects.get(pk=self.task.pk).done
        
        # have we got *four* entries saved correctly?
        assert len(Lexicon.objects.filter(word=self.words_in_wordlist[0])) == 2
        assert len(Lexicon.objects.filter(word=self.words_in_wordlist[1])) == 1
        assert len(Lexicon.objects.filter(word=self.words_in_wordlist[2])) == 1
        
        for i in range(4):
            key = 'entry-%d' % i
            lex = Lexicon.objects.filter(entry__exact=key)
            assert len(lex) == 1, 'Expected 1 entry for %s' % key
            assert lex[0].language == self.lang
            assert lex[0].source == self.source
            
            if i == 3:
                expected_word = self.words_in_wordlist[0]
            else:
                expected_word = self.words_in_wordlist[i]
            assert lex[0].word == expected_word
            
    def test_wordlist_orders_not_by_id(self):
        WL = Wordlist.objects.create(name="test2", editor=self.editor)
        WL.save()
        
        words = self.words[:]
        words.reverse()
        assert words != self.words
        
        for i, w in enumerate(words, 1):
            m = WordlistMember(wordlist=WL, word=w, order=i)
            m.save()
        
        t = Task.objects.create(
            editor=self.editor,
            name="Test Task 2",
            description=" ",
            source=self.source,
            wordlist=WL,
            done=False,
            view="WordlistView",
            records=1, 
        )
        t.save()
        
        self.client.login(username="admin", password="test")
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        formdata = [f.initial for f in response.context['formset'].forms]
                
        # and is it correct?
        for i in range(len(words)):
            assert formdata[i]['order_id'] == i + 1 # ordering starts at 1 not 0
            assert formdata[i]['word'] == words[i]
        
        

