"""
Tests for Statistics
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from website.apps.core.models import Language, Family, Source

from website.apps.statistics.models import Statistic, StatisticalValue
from website.apps.statistics.models import AlreadyRegistered
from website.apps.statistics.models import InvalidMethod, InvalidField


class StatisticMixin(object):
    """Mixin for Statistic Tests"""
    @classmethod
    def setUpTestData(cls):
        cls.editor = User.objects.create(username='admin')
        cls.lang1 = Language.objects.create(
            language='A', slug='langa',
            information='i.1', classification='a, b',
            isocode='aaa', editor=cls.editor
        )
        cls.lang2 = Language.objects.create(
            language='B', slug='langb',
            information='i.2', classification='c, d, e',
            isocode='bbb', editor=cls.editor
        )
        cls.fam1 = Family.objects.create(
            family='F', slug='f', editor=cls.editor
        )
        
        # make sure we're clean (i.e. ignore whatever Statistic's are defined
        # in the above imported models)
        cls.statistic = Statistic()
        cls.statistic.register("NLang", Language, graph=True)
        cls.statistic.register("NFam", Family)
        cls.statistic.register("NSource", Source)


class StatisticTest(StatisticMixin, TestCase):
    """Tests the statistics plumbing"""

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
            self.statistic.register(
                "Bad Statistic", Language, method="NOTHING"
            )

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

    def test_get_all(self):
        """Tests the manager method .get_all"""
        self.statistic.update()
        # note the list comprehension is because .values_list returns a
        # django.db.models.query.ValuesListQuerySet which is not a normal list
        assert [_ for _ in StatisticalValue.objects.get_all("NFam")] == [1.0]
        assert [_ for _ in StatisticalValue.objects.get_all("NLang")] == [2.0]

    def test_get_all_ordering(self):
        """Tests the manager method .get_all ordering"""
        # create some
        self.statistic.update()
        for i in range(1, 3):
            StatisticalValue.objects.create(
                label="NLang",
                model="what.ever",
                method="count",
                field="id",
                value=(2 + i)
            )
        # note the list comprehension is because .values_list returns a
        # django.db.models.query.ValuesListQuerySet which is not a normal list
        nlangs = [_ for _ in StatisticalValue.objects.get_all("NLang")]
        assert nlangs == [2.0, 3.0, 4.0]


class Test_StatisticView(StatisticMixin, TestCase):
    """Tests the view."""
    def setUp(self):
        super(Test_StatisticView, self).setUp()
        self.client = Client()
        self.response = self.client.get('/statistics/')
    
    def test_200ok(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'statistics/details.html')
    

