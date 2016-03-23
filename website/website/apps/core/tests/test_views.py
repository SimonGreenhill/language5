from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Source, Language, Family, AlternateName
from website.apps.core.tests.utils import PaginatorTestMixin

class BaseMixin(object):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.language1 = Language.objects.create(
            language='Language1',
            slug='language1',
            information='',
            classification='Austronesian, Malayo-Polynesian, Bali-Sasak, Bali',
            isocode='aaa',
            glottocode='aaaa1234',
            editor=self.editor
        )
        self.language2 = Language.objects.create(
            language='Language2',
            slug='language2',
            information='',
            classification='Mayan, Huastecan',
            isocode='bbb',
            glottocode='bbbb1234',
            editor=self.editor
        )
        self.language3 = Language.objects.create(
            language='Language3',
            slug='language3',
            information='',
            classification='Mayan, Huastecan',
            isocode='bbb',
            glottocode='bbbb1234',
            editor=self.editor
        )
        self.alt1 = AlternateName.objects.create(
            language=self.language1,
            name='Fudge',
            slug='fudge',
            editor=self.editor
        )
        
        self.source1 = Source.objects.create(
            year="1991",
            author='Smith',
            slug='smith1991',
            reference='...',
            comment='...',
            editor=self.editor
        )
        self.source2 = Source.objects.create(
            year="2002",
            author='Jones',
            slug='jones2002',
            reference='...',
            comment='...',
            editor=self.editor
        )
        
        self.family1 = Family.objects.create(
            family="Austronesian",
            slug="austronesian",
            editor=self.editor
        )
        self.family2 = Family.objects.create(
            family="Mayan",
            slug="mayan",
            editor=self.editor
        )
        
        self.client = Client()

    
class Test_LanguageIndex(BaseMixin, PaginatorTestMixin, TestCase):
    
    url = reverse('language-index')
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/language_index.html')
        
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get(self.url[0:-1])
        self.assertRedirects(
            response, '/language/', status_code=301, target_status_code=200
        )
        
    def test_content(self):
        "Test languages.index"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
    
    def test_sorting(self):
        response = self.client.get('%s?sort=language' % self.url)
        for i, obj in enumerate(Language.objects.all().order_by('language')):
            assert response.context['table'].rows[i].record == obj
            
        response = self.client.get('%s?sort=-language' % self.url)
        for i, obj in enumerate(Language.objects.all().order_by('-language')):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        response = self.client.get('%s?sort=sausage' % self.url)
        for i, obj in enumerate(Language.objects.all().order_by('language')):
            assert response.context['table'].rows[i].record == obj
    
    def test_show_subsets(self):
        response = self.client.get(self.url)
        for subset in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            url = reverse('language-index-subset', kwargs={'subset': subset})
            self.assertContains(response, url)
    
    def test_filter_on_subset(self):
        # check we get an empty result
        response = self.client.get('%s?subset=A' % self.url)
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
        
        # check we get every with L*
        response = self.client.get('%s?subset=L' % self.url)
        self.assertContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
        
        # now create another language
        Language.objects.create(
            language='A Language',
            slug='language_a',
            information='',
            classification='',
            isocode='xyz',
            editor=self.editor
        )
        
        response = self.client.get('%s?subset=A' % self.url)
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
        self.assertContains(response, 'A Language')
        

class Test_LanguageDetail(BaseMixin, PaginatorTestMixin, TestCase):
    def setUp(self):
        super(Test_LanguageDetail, self).setUp()
        self.url = reverse(
            'language-detail', kwargs={'language': self.language1.slug}
        )
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/language_detail.html')
    
    def test_redirect_on_alternate_names(self):
        # Check that response to an existing language is 200 OK.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Check that response to ./fudge/ is 302 and redirected
        response = self.client.get(
            reverse('language-detail', kwargs={'language': 'fudge'})
        )
        self.assertRedirects(
            response,
            reverse('language-detail', kwargs={'language': 'language1'}),
            status_code=301, target_status_code=200
        )
    
    def test_404_on_nonexistent_language(self):
        # Check that response to ./nonexistentlanguage/ is 404 NotFound
        url = reverse(
            'language-detail', kwargs={'language': 'nonexistentlanguage'}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_alternate_names_shown_in_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Also Known As:')
        self.assertContains(response, 'Fudge')
    

class Test_ISOLookup(BaseMixin, TestCase):
    #Logic:
    #    No matching entries - raise 404
    #    1 Matching entry - redirect to languages.details page
    #    >1 Matching entries - show a list of the languages
    def test_multiple_entries(self):
        # check that /iso/bbb/ is sent to a list of pages.
        url = reverse('iso-lookup', kwargs={'iso': 'bbb'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/language_index.html')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
        self.assertNotContains(response, 'Language1')
    
    def test_redirect_on_unique(self):
        iso_url = reverse('iso-lookup', kwargs={'iso': 'aaa'})
        real_url = reverse(
            'language-detail', kwargs={'language': 'language1'}
        )
        
        response = self.client.get(iso_url)
        
        self.assertRedirects(
            response, real_url, status_code=301, target_status_code=200
        )
        # ...and check the redirected-to page..
        response = self.client.get(real_url)
        self.assertContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
    
    def test_notfound(self):
        url = reverse('iso-lookup', kwargs={'iso': 'zzz'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class Test_GlottoLookup(BaseMixin, TestCase):
    #Logic:
    #    No matching entries - raise 404
    #    1 Matching entry - redirect to languages.details page
    #    >1 Matching entries - show a list of the languages
    def test_multiple_entries(self):
        url = reverse('glotto-lookup', kwargs={'glotto': 'bbbb1234'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/language_index.html')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
        self.assertNotContains(response, 'Language1')
    
    def test_redirect_on_unique(self):
        url = reverse('glotto-lookup', kwargs={'glotto': 'aaaa1234'})
        real_url = reverse(
            'language-detail', kwargs={'language': 'language1'}
        )
        response = self.client.get(url)
        self.assertRedirects(
            response, real_url, status_code=301, target_status_code=200
        )
        # ...and check the redirected-to page..
        response = self.client.get(real_url)
        self.assertContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
    
    def test_notfound(self):
        url = reverse('glotto-lookup', kwargs={'glotto': 'zzzz1234'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class Test_FamilyIndex(BaseMixin, PaginatorTestMixin, TestCase):
    """Tests the family_index view"""
    url = reverse('family-index')
            
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/family_index.html')
    
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get(self.url[0:-1])
        self.assertRedirects(
            response, self.url, status_code=301, target_status_code=200
        )
    
    def test_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Austronesian')
        self.assertContains(response, 'Mayan')
    
    def test_sorting(self):
        response = self.client.get('%s?sort=family' % self.url)
        for i, obj in enumerate(Family.objects.all().order_by('family')):
            assert response.context['table'].rows[i].record == obj
            
        response = self.client.get('%s?sort=-family' % self.url)
        for i, obj in enumerate(Family.objects.all().order_by('-family')):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        response = self.client.get("%s?sort=sausage" % self.url)
        for i, obj in enumerate(Family.objects.all().order_by('family')):
            assert response.context['table'].rows[i].record == obj
        
    def test_show_subsets(self):
        response = self.client.get(self.url)
        for subset in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            url = reverse('family-index-subset', kwargs={'subset': subset})
            self.assertContains(response, url)
    
    def test_filter_on_subset(self):
        # check we get an empty result
        response = self.client.get('%s?subset=X' % self.url)
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Mayan')
        self.assertNotContains(response, 'Austronesian')
        
        # check M* but not A*
        response = self.client.get('%s?subset=M' % self.url)
        self.assertContains(response, 'Mayan')
        self.assertNotContains(response, 'Austronesian')
        
        # and A but not M
        response = self.client.get('%s?subset=A' % self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Austronesian')
        self.assertNotContains(response, 'Mayan')
    
        
class Test_FamilyDetail(BaseMixin, PaginatorTestMixin, TestCase):
    """Tests the family_detail view"""
    def setUp(self):
        super(Test_FamilyDetail, self).setUp()
        # 1 is Austronesian
        # 2 & 3 are Mayan
        self.family1.language_set.add(self.language1)
        self.family1.save()
        self.family2.language_set.add(self.language2)
        self.family2.language_set.add(self.language3)
        self.family2.save()
        self.url = reverse('family-detail', kwargs={'slug': self.family1.slug})
        
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/family_detail.html')
        
    def test_404_on_missing_family(self):
        url = reverse('family-detail', kwargs={'slug': 'basque'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_family_detail_1(self):
        url = reverse('family-detail', kwargs={'slug': 'austronesian'})
        response = self.client.get(url)
        self.assertContains(response, 'Austronesian')
        self.assertContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
        
    def test_family_detail_2(self):
        url = reverse('family-detail', kwargs={'slug': 'mayan'})
        response = self.client.get(url)
        self.assertContains(response, 'Mayan')
        self.assertNotContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
        
    def test_sorting(self):
        url = reverse('family-detail', kwargs={'slug': 'mayan'})
        response = self.client.get('%s?sort=language' % url)
        for i, obj in enumerate([self.language2, self.language3]):
            assert response.context['languages'].rows[i].record == obj
            
        response = self.client.get('%s?sort=-language' % url)
        for i, obj in enumerate([self.language3, self.language2]):
            assert response.context['languages'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        url = reverse('family-detail', kwargs={'slug': 'mayan'})
        response = self.client.get("%s?sort=sausage" % url)
        for i, obj in enumerate([self.language2, self.language3]):
            assert response.context['languages'].rows[i].record == obj


class Test_SourceIndex(BaseMixin, PaginatorTestMixin, TestCase):
    """Tests the source_index view"""
    url = reverse('source-index')
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/source_index.html')
    
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get(self.url[0:-1])
        self.assertRedirects(
            response, self.url, status_code=301, target_status_code=200
        )
    
    def test_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Smith')
        self.assertContains(response, 'Jones')
     
    def test_sorting(self):
        response = self.client.get('%s?sort=year' % self.url)
        for i, obj in enumerate([self.source1, self.source2]):
            assert response.context['table'].data.data[i] == obj
            
        response = self.client.get('%s?sort=author' % self.url)
        for i, obj in enumerate([self.source2, self.source1]):
            assert response.context['table'].data.data[i] == obj
    
    def test_show_subsets(self):
        response = self.client.get(self.url)
        for subset in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            url = reverse('source-index-subset', kwargs={'subset': subset})
            self.assertContains(response, url)
    
    def test_filter_on_subset(self):
        # check we get an empty result
        response = self.client.get('%s?subset=A' % self.url)
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Smith')
        self.assertNotContains(response, 'Jones')
        
        # check S* but not J*
        response = self.client.get('%s?subset=S' % self.url)
        self.assertContains(response, 'Smith')
        self.assertNotContains(response, 'Jones')
        
        # and J but not S
        response = self.client.get('%s?subset=J' % self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jones')
        self.assertNotContains(response, 'Smith')
    

class Test_SourceDetail(BaseMixin, PaginatorTestMixin):
    """Tests the source_detail view"""
    def setUp(self):
        super(Test_SourceDetail, self).setUp()
        self.url = reverse('source-detail', kwargs={'slug': self.source1.slug})
        
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/source_detail.html')
    
    def test_404_on_missing_source(self):
        url = reverse('source-detail', kwargs={'slug': 'fudge'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_find_valid_source(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Smith')
        self.assertContains(response, '1991')
    
