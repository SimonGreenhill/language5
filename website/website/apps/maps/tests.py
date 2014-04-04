from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from website.apps.core.models import Location, Language
from website.apps.lexicon.models import Word, CognateSet, Cognate, Lexicon
from website.apps.lexicon.tests import DataMixinLexicon
from website.apps.maps.views import prepare_map_data


class DataMixinLexiconLocations(DataMixinLexicon):
    def setUp(self):
        super(DataMixinLexiconLocations, self).setUp()
        self.loc1 = Location.objects.create(
            isocode=self.lang1.isocode,
            latitude=1.0,
            longitude=-5.6,
            editor=self.editor
        )
        self.loc2 = Location.objects.create(
            isocode=self.lang2.isocode,
            latitude=-20.0,
            longitude=100.1,
            editor=self.editor
        )

    def compare(self, result, **kwargs):
        # little helper for comparing a dict with the kwargs
        for k, v in kwargs.items():
            assert k in result, 'No key for %s' % k
            assert result[k] == v, "%s is not %r but %r" % (k, v, result[k])
    

class TestPrepareMapDataUtility(DataMixinLexiconLocations, TestCase):
    def test_one(self):
        result = prepare_map_data(
            Word.objects.get(pk=1).lexicon_set.select_related('language').all()
        )
        assert len(result) == 1
        self.compare(result[0], 
            language=self.lang1,
            label=self.lexicon1.entry,
            isocode=self.lang1.isocode,
            latitude=self.loc1.latitude,
            longitude=self.loc1.longitude
        )
    
    def test_two(self):
        result = prepare_map_data(
            Word.objects.get(pk=2).lexicon_set.select_related('language').all()
        )
        assert len(result) == 2
        self.compare(result[0],
            language=self.lang2,
            label=self.lexicon2.entry,
            isocode=self.lang2.isocode,
            latitude=self.loc2.latitude,
            longitude=self.loc2.longitude
        )
        self.compare(result[1],
            language=self.lang1,
            label=self.lexicon3.entry,
            isocode=self.lang1.isocode,
            latitude=self.loc1.latitude,
            longitude=self.loc1.longitude
        )
    
    def test_missing_isocode(self):
        lang3 = Language.objects.create(language='C', slug='langc', 
                                        information='i.1', classification='a, b',
                                        isocode=None, editor=self.editor)
        lexicon4 = Lexicon.objects.create(language=lang3, 
            source=self.source1, word=self.word1, entry="X", phon_entry="x", 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        # no isocode but create a spare location just in case.
        loc4 = Location.objects.create(
                isocode='xxx',
                latitude=-292.4,
                longitude=221.09,
                editor=self.editor
        )
        result = prepare_map_data(
            Word.objects.get(pk=self.word1.pk).lexicon_set.select_related('language').all()
        )
        assert len(result) == 1
        assert result[0]['label'] == self.lexicon1.entry
        
    def test_invalid_isocode(self):
        lang3 = Language.objects.create(language='C', slug='langc', 
                                        information='i.1', classification='a, b',
                                        isocode='XXXXXXX', editor=self.editor)
        lexicon4 = Lexicon.objects.create(language=lang3, 
            source=self.source1, word=self.word1, entry="X", phon_entry="x", 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        # create a location for this one - should NOT show up.
        loc4 = Location.objects.create(
                isocode=lang3.isocode,
                latitude=-292.4,
                longitude=221.09,
                editor=self.editor
        )
        result = prepare_map_data(
            Word.objects.get(pk=self.word1.pk).lexicon_set.select_related('language').all()
        )
        assert len(result) == 1
        assert result[0]['label'] == self.lexicon1.entry
    
    def test_missing_location(self):
        lang3 = Language.objects.create(language='C', slug='langc', 
                                        information='i.1', classification='a, b',
                                        isocode='XXX', editor=self.editor)
        lexicon4 = Lexicon.objects.create(language=lang3, 
            source=self.source1, word=self.word1, entry="X", phon_entry="x", 
            annotation="", loan=False, loan_source=None, editor=self.editor)
        # NOTE: No extra location this time.
        result = prepare_map_data(
            Word.objects.get(pk=self.word1.pk).lexicon_set.select_related('language').all()
        )
        assert len(result) == 1
        assert result[0]['label'] == self.lexicon1.entry


class TestViewWordMap(DataMixinLexiconLocations, TestCase):
    def test_404(self):
        response = self.client.get(reverse('maps:word-map', kwargs={'slug': 'elvis'}))
        self.assertEquals(response.status_code, 404)
    
    def test_context(self):
        # what entries are in context['records']
        response = self.client.get(reverse('maps:word-map', kwargs={'slug': self.word2.slug}))
        self.assertEquals(response.status_code, 200)
        assert 'records' in response.context
        result = response.context['records']
        assert len(result) == 2
        self.compare(result[0],
            language=self.lang2,
            label=self.lexicon2.entry,
            isocode=self.lang2.isocode,
            latitude=self.loc2.latitude,
            longitude=self.loc2.longitude
        )
        self.compare(result[1],
            language=self.lang1,
            label=self.lexicon3.entry,
            isocode=self.lang1.isocode,
            latitude=self.loc1.latitude,
            longitude=self.loc1.longitude
        )
    
    
class TestViewCognateSetMap(DataMixinLexiconLocations, TestCase):
    def test_404(self):
        response = self.client.get(reverse('maps:cognate-map', kwargs={'pk': '404'}))
        self.assertEquals(response.status_code, 404)
    
    def test_context(self):
        cogset1 = CognateSet.objects.create(
            protoform = "*xx",
            gloss = "proto-world!",
            editor=self.editor
        )
        
        Cognate.objects.create(lexicon=self.lexicon1, cognateset=cogset1, editor=self.editor)
        Cognate.objects.create(lexicon=self.lexicon2, cognateset=cogset1, editor=self.editor)

        # what entries are in context['records']
        response = self.client.get(reverse('maps:cognate-map', kwargs={'pk': cogset1.pk}))
        self.assertEquals(response.status_code, 200)
        assert 'records' in response.context
        result = response.context['records']
        assert len(result) == 2
        
        self.compare(result[0],
            language=self.lang1,
            label=self.lexicon1.entry,
            isocode=self.lang1.isocode,
            latitude=self.loc1.latitude,
            longitude=self.loc1.longitude
        )
        self.compare(result[1],
            language=self.lang2,
            label=self.lexicon2.entry,
            isocode=self.lang2.isocode,
            latitude=self.loc2.latitude,
            longitude=self.loc2.longitude
        )
    
