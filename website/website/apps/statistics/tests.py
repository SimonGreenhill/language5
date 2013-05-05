"""
Tests for Statistics
"""
from django.test import TestCase
from django.contrib.auth.models import User
from website.apps.core.models import Language, Family, Source

from website.apps.statistics import Statistic, AlreadyRegistered, InvalidMethod, InvalidField
from website.apps.statistics.models import StatisticalValue

class StatisticTest(TestCase):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.lang1 = Language.objects.create(language='A', slug='langa', 
                                             information='i.1', classification='a, b',
                                             isocode='aaa', editor=self.editor)
        self.lang2 = Language.objects.create(language='B', slug='langb',
                                             information='i.2', classification='c, d, e',
                                             isocode='bbb', editor=self.editor)
        self.fam1 = Family.objects.create(family='F', slug='f', editor=self.editor)
        
        # make sure we're clean (i.e. ignore whatever Statistic's are defined 
        # in the above imported models)
        self.statistic = Statistic()
        self.statistic.register("NLang", Language)
        self.statistic.register("NFam", Family)
        self.statistic.register("NSource", Source)
        
    def test_get_count(self):
        assert self.statistic._get_count(Language, 'id') == 2
        assert self.statistic._get_count(Family, 'id') == 1
        
    def test_get_count_zero(self):
        assert self.statistic._get_count(Source, 'id') == 0
        
    def test_get_count_error(self):
        with self.assertRaises(InvalidField):
            self.statistic._get_count(Source, 'var') == 0
            
    def test_bad_statistic(self):
        with self.assertRaises(InvalidMethod):
            self.statistic.register("Bad Statistic", Language, method="NOTHING")
        
    def test_fail_register(self):
        with self.assertRaises(AlreadyRegistered):
            self.statistic.register("NLang", Language)
        
    def test_update(self):
        assert len(StatisticalValue.objects.all()) == 0
        self.statistic.update()
        assert len(StatisticalValue.objects.all()) == 3
        assert StatisticalValue.objects.filter(label="NLang")[0].value == 2
        assert StatisticalValue.objects.filter(label="NFam")[0].value == 1
        assert StatisticalValue.objects.filter(label="NSource")[0].value == 0
        
