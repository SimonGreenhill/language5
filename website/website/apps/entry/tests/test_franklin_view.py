# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from website.apps.core.models import Source, Language
from website.apps.lexicon.models import Word, Lexicon
from website.apps.entry.models import Task
from website.apps.entry.dataentry import available_views
from website.apps.entry.views import decode_checkpoint

from website.apps.entry.tests import DataMixin

class Test_FranklinView(DataMixin):
    """Tests the Franklin View"""

    def setUp(self):
        super(Test_FranklinView, self).setUp()
        self.task.language = self.lang
        self.task.view = "FranklinView"
        self.task.records = 100
        self.task.save()
        self.word.word = 'man'
        self.word.slug = 'man'
        self.word.save()
        
        #Word.objects.create(id=1, word="man", slug="man", editor=self.editor)
        Word.objects.create(id=2, word="woman", slug="woman", editor=self.editor)
        Word.objects.create(id=3, word="i", slug="i", editor=self.editor)
        Word.objects.create(id=4, word="thou", slug="thou", editor=self.editor)
        Word.objects.create(id=5, word="we-incl", slug="we-incl", editor=self.editor)
        Word.objects.create(id=6, word="all", slug="all", editor=self.editor)
        Word.objects.create(id=7, word="head", slug="head", editor=self.editor)
        Word.objects.create(id=8, word="hair", slug="hair", editor=self.editor)
        Word.objects.create(id=9, word="eye", slug="eye", editor=self.editor)
        Word.objects.create(id=10, word="nose", slug="nose", editor=self.editor)
        Word.objects.create(id=11, word="ear", slug="ear", editor=self.editor)
        Word.objects.create(id=12, word="tooth", slug="tooth", editor=self.editor)
        Word.objects.create(id=13, word="tongue", slug="tongue", editor=self.editor)
        Word.objects.create(id=14, word="neck", slug="neck", editor=self.editor)
        Word.objects.create(id=15, word="mouth", slug="mouth", editor=self.editor)
        Word.objects.create(id=16, word="arm", slug="arm", editor=self.editor)
        Word.objects.create(id=17, word="breast", slug="breast", editor=self.editor)
        Word.objects.create(id=18, word="belly", slug="belly", editor=self.editor)
        Word.objects.create(id=19, word="leg", slug="leg", editor=self.editor)
        Word.objects.create(id=20, word="knee", slug="knee", editor=self.editor)
        Word.objects.create(id=21, word="skin", slug="skin", editor=self.editor)
        Word.objects.create(id=22, word="blood", slug="blood", editor=self.editor)
        Word.objects.create(id=23, word="fat", slug="fat", editor=self.editor)
        Word.objects.create(id=24, word="bone", slug="bone", editor=self.editor)
        Word.objects.create(id=25, word="heart", slug="heart", editor=self.editor)
        Word.objects.create(id=26, word="liver", slug="liver", editor=self.editor)
        Word.objects.create(id=27, word="sun", slug="sun", editor=self.editor)
        Word.objects.create(id=28, word="moon", slug="moon", editor=self.editor)
        Word.objects.create(id=29, word="star", slug="star", editor=self.editor)
        Word.objects.create(id=30, word="cloud", slug="cloud", editor=self.editor)
        Word.objects.create(id=31, word="rain", slug="rain", editor=self.editor)
        Word.objects.create(id=32, word="night", slug="night", editor=self.editor)
        Word.objects.create(id=33, word="water", slug="water", editor=self.editor)
        Word.objects.create(id=34, word="ground", slug="ground", editor=self.editor)
        Word.objects.create(id=35, word="stone", slug="stone", editor=self.editor)
        Word.objects.create(id=36, word="sand", slug="sand", editor=self.editor)
        Word.objects.create(id=37, word="mountain", slug="mountain", editor=self.editor)
        Word.objects.create(id=38, word="fire", slug="fire", editor=self.editor)
        Word.objects.create(id=39, word="smoke", slug="smoke", editor=self.editor)
        Word.objects.create(id=40, word="ashes", slug="ashes", editor=self.editor)
        Word.objects.create(id=41, word="road", slug="road", editor=self.editor)
        Word.objects.create(id=42, word="tree", slug="tree", editor=self.editor)
        Word.objects.create(id=43, word="root", slug="root", editor=self.editor)
        Word.objects.create(id=44, word="bark", slug="bark", editor=self.editor)
        Word.objects.create(id=45, word="dog", slug="dog", editor=self.editor)
        Word.objects.create(id=46, word="tail", slug="tail", editor=self.editor)
        Word.objects.create(id=47, word="bird", slug="bird", editor=self.editor)
        Word.objects.create(id=48, word="feather", slug="feather", editor=self.editor)
        Word.objects.create(id=49, word="egg", slug="egg", editor=self.editor)
        Word.objects.create(id=50, word="fish", slug="fish", editor=self.editor)
        Word.objects.create(id=51, word="big", slug="big", editor=self.editor)
        Word.objects.create(id=52, word="small", slug="small", editor=self.editor)
        Word.objects.create(id=53, word="good", slug="good", editor=self.editor)
        Word.objects.create(id=54, word="long", slug="long", editor=self.editor)
        Word.objects.create(id=55, word="red", slug="red", editor=self.editor)
        Word.objects.create(id=56, word="white", slug="white", editor=self.editor)
        Word.objects.create(id=57, word="black", slug="black", editor=self.editor)
        Word.objects.create(id=58, word="yellow", slug="yellow", editor=self.editor)
        Word.objects.create(id=59, word="green", slug="green", editor=self.editor)
        Word.objects.create(id=60, word="warm", slug="warm", editor=self.editor)
        Word.objects.create(id=61, word="cold", slug="cold", editor=self.editor)
        Word.objects.create(id=62, word="full", slug="full", editor=self.editor)
        Word.objects.create(id=63, word="new", slug="new", editor=self.editor)
        Word.objects.create(id=64, word="to-eat", slug="to-eat", editor=self.editor)
        Word.objects.create(id=65, word="to-drink", slug="to-drink", editor=self.editor)
        Word.objects.create(id=66, word="to-stand", slug="to-stand", editor=self.editor)
        Word.objects.create(id=67, word="to-sit", slug="to-sit", editor=self.editor)
        Word.objects.create(id=68, word="to-speak", slug="to-speak", editor=self.editor)
        Word.objects.create(id=69, word="to-walk", slug="to-walk", editor=self.editor)
        Word.objects.create(id=70, word="to-give", slug="to-give", editor=self.editor)
        Word.objects.create(id=71, word="to-sleep", slug="to-sleep", editor=self.editor)
        Word.objects.create(id=72, word="to-lie", slug="to-lie", editor=self.editor)
        Word.objects.create(id=73, word="to-see", slug="to-see", editor=self.editor)
        Word.objects.create(id=74, word="to-hear", slug="to-hear", editor=self.editor)
        Word.objects.create(id=75, word="to-swim", slug="to-swim", editor=self.editor)
        Word.objects.create(id=76, word="to-come", slug="to-come", editor=self.editor)
        Word.objects.create(id=77, word="to-fly", slug="to-fly", editor=self.editor)
        Word.objects.create(id=78, word="to-bite", slug="to-bite", editor=self.editor)
        Word.objects.create(id=79, word="name", slug="name", editor=self.editor)
        Word.objects.create(id=80, word="dry", slug="dry", editor=self.editor)
        Word.objects.create(id=81, word="who", slug="who", editor=self.editor)
        Word.objects.create(id=82, word="what", slug="what", editor=self.editor)
        Word.objects.create(id=83, word="to-burn", slug="to-burn", editor=self.editor)
        Word.objects.create(id=84, word="louse", slug="louse", editor=self.editor)
        Word.objects.create(id=85, word="many", slug="many", editor=self.editor)
        Word.objects.create(id=86, word="this", slug="this", editor=self.editor)
        Word.objects.create(id=87, word="that", slug="that", editor=self.editor)
        Word.objects.create(id=88, word="one", slug="one", editor=self.editor)
        Word.objects.create(id=89, word="two", slug="two", editor=self.editor)
        Word.objects.create(id=90, word="to-know", slug="to-know", editor=self.editor)
        Word.objects.create(id=91, word="to-kill", slug="to-kill", editor=self.editor)
        Word.objects.create(id=92, word="not", slug="not", editor=self.editor)
        Word.objects.create(id=93, word="leaf", slug="leaf", editor=self.editor)
        Word.objects.create(id=94, word="meat", slug="meat", editor=self.editor)
        Word.objects.create(id=95, word="horn", slug="horn", editor=self.editor)
        Word.objects.create(id=96, word="claw", slug="claw", editor=self.editor)
        Word.objects.create(id=97, word="person", slug="person", editor=self.editor)
        Word.objects.create(id=98, word="seed", slug="seed", editor=self.editor)
        Word.objects.create(id=99, word="round", slug="round", editor=self.editor)
        Word.objects.create(id=100, word="to-die", slug="to-die", editor=self.editor)
        
        #go through and set to slug + something
        self.form_data = {
            'form-TOTAL_FORMS': u'100',
            'form-INITIAL_FORMS': u'100',
            'form-MAX_NUM_FORMS': u'1000',
            'submit': 'true',
        }
        self.expected = {}
        for i, w in enumerate(Word.objects.all().order_by('id')):
            # str() all the id's as the should be strings
            self.form_data['form-%d-language' % i] = str(self.task.language.id)
            self.form_data['form-%d-source' % i] = str(self.task.source.id)
            self.form_data['form-%d-word' % i] = str(w.id)
            self.form_data['form-%d-entry' % i] = "%s-xxx" % w.slug
            self.expected[w.id] = (w, self.form_data['form-%d-entry' % i])
    
    def test_number_of_entries(self):
        assert len(Word.objects.all()) == 100
    
    def test_checkpoint_works(self):
        # need to be missing one..
        del(self.form_data['form-50-entry'])
        
        # don't have a checkpoint already...
        assert self.task.checkpoint is None
        
        self.client.login(username="admin", password="test")
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None, "Expecting a checkpoint"
        
        restored = decode_checkpoint(t.checkpoint)
        for k, v in self.form_data.items():
            assert k in restored, "Missing %s from checkpoint" % k
            assert restored[k] == v, "Expected %s to be %s not %r" % (k, v, restored[k])
        
    def test_words_save_correctly(self):
        # don't have a checkpoint already...
        assert self.task.checkpoint is None
        
        # don't have any stored lexical items
        assert len(Lexicon.objects.all()) == 0
        
        # POST form data
        self.client.login(username="admin", password="test")
        response = self.client.post(self.task.get_absolute_url(), self.form_data)
        self.assertEqual(response.status_code, 200)
        
        # do we have a checkpoint?
        t = Task.objects.get(pk=self.task.id)
        assert t.checkpoint is not None, "Expecting a checkpoint"
        
        # test view has redirected..
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry/done.html')
        
        # test view has completed the task
        assert Task.objects.get(pk=self.task.id).done
        
        # test that we have 100 lexical items saved.
        assert len(Lexicon.objects.all()) == 100, "Should have 100 items stored."
        
        for word_id in self.expected:
            word, entry = self.expected[word_id]
            L = Lexicon.objects.filter(word=word)
            assert len(L) == 1, "Expected 1 record"
            assert L[0].entry == entry, "Expected entry to be %s not %s" % (entry, L[0].entry)
        
