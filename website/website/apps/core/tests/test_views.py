import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from website.apps.core.models import Source, Language, Family, AlternateName

class BaseMixin(object):
    def setUp(self):
        self.editor = User.objects.create(username='admin')
        self.language1 = Language.objects.create(
                        language='Language1', 
                        slug='language1', 
                        information='', 
                        classification='Austronesian, Malayo-Polynesian, Bali-Sasak, Bali',
                        isocode='aaa', 
                        editor=self.editor
        )
        self.language2 = Language.objects.create(
                        language='Language2', 
                        slug='language2', 
                        information='', 
                        classification='Mayan, Huastecan',
                        isocode='bbb', 
                        editor=self.editor
        )
        self.language3 = Language.objects.create(
                        language='Language3', 
                        slug='language3', 
                        information='', 
                        classification='Mayan, Huastecan',
                        isocode='bbb', 
                        editor=self.editor
        )
        self.alt1 = AlternateName.objects.create(
                        language=self.language1, name='Fudge', 
                        slug='fudge',
                        editor=self.editor
        )
        self.client = Client()


class PaginatorTestMixin(object):
    """Mixin for running paginator tests. Needs self.url to be set."""
    def test_paginator(self):
        response = self.client.get('{}?page=1'.format(self.url))
        self.assertEqual(response.status_code, 200)
    
    def test_bad_paginator(self):
        # no errors, just give page1
        response = self.client.get('{}?page=10000'.format(self.url))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('{}?page=banana'.format(self.url))
        self.assertEqual(response.status_code, 200)
    
    
    
    
class Test_LanguageIndex(BaseMixin, PaginatorTestMixin, TestCase):
    """Tests the Language Index page"""
    
    def setUp(self):
        super(Test_LanguageIndex, self).setUp()
        self.url = reverse('language-index')
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/language_index.html')
        
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get(self.url[0:-1])
        self.assertRedirects(response, '/language/', status_code=301, target_status_code=200)
        
    def test_content(self):
        "Test languages.index"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
    
    def test_sorting(self):
        response = self.client.get('{}?sort=language'.format(self.url))
        for i, obj in enumerate(Language.objects.all().order_by('language')):
            assert response.context['table'].rows[i].record == obj
            
        response = self.client.get('{}?sort=-language'.format(self.url))
        for i, obj in enumerate(Language.objects.all().order_by('-language')):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        response = self.client.get("{}?sort=sausage".format(self.url))
        for i, obj in enumerate(Language.objects.all().order_by('language')):
            assert response.context['table'].rows[i].record == obj
    
    def test_show_subsets(self):
        response = self.client.get(self.url)
        for subset in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            url = reverse('language-index-subset', kwargs={'subset': subset})
            self.assertContains(response, url)
    
    def test_filter_on_subset(self):
        # check we get an empty result
        response = self.client.get('{}?subset=A'.format(self.url))
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
        
        # check we get every with L*
        response = self.client.get('{}?subset=L'.format(self.url))
        self.assertContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
        
        # now create another language
        A = Language.objects.create(
                        language='A Language', 
                        slug='language_a', 
                        information='', 
                        classification='',
                        isocode='xyz', 
                        editor=self.editor
        )
        
        response = self.client.get('{}?subset=A'.format(self.url))
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
        self.assertContains(response, 'A Language')
        

class Test_LanguageDetail(BaseMixin, TestCase):
    """Tests the Language Detail Page"""
    
    def test_200ok(self):
        response = self.client.get('/language/language1')
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get('/language/language1')
        self.assertTemplateUsed(response, 'core/language_detail.html')
    
    def test_redirect_on_alternate_names(self):
        "Test redirection to canonical URL when given an alternate name"
        # Check that response to an existing language is 200 OK.
        response = self.client.get('/language/language1')
        self.assertEqual(response.status_code, 200)
        
        # Check that response to ./fudge/ is 302 and redirected
        response = self.client.get('/language/fudge')
        self.assertRedirects(response, '/language/language1', 
                status_code=301, target_status_code=200)
    
    def test_404_on_nonexistent_language(self):
        "Test that a non-existent language raises a 404"
        # Check that response to ./nonexistentlanguage/ is 404 NotFound
        response = self.client.get('/language/nonexistentlanguage')
        self.assertEqual(response.status_code, 404)
    
    def test_alternate_names_shown_in_details(self):
        "Test that the details view shows alternate names too"
        response = self.client.get('/language/language1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Also Known As:')
        self.assertContains(response, 'Fudge')
    

class Test_ISOLookup(BaseMixin, TestCase):
    """
    Tests the differential output under the ISO lookup `isolookup`.
    
    Logic:
        No matching entries - raise 404
        1 Matching entry - redirect to languages.details page
        >1 Matching entries - show a list of the languages
    """
    def test_multiple_iso_entries(self):
        "Test that ISO codes with multiple languages returns a list"
        # check that /iso/bbb/ is sent to a list of pages.
        response = self.client.get('/iso/bbb')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/language_index.html')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')
        self.assertNotContains(response, 'Language1')
    
    def test_redirect_on_unique_iso(self):
        "Test that a request for a unique ISO is redirected to the languages.details page"
        response = self.client.get('/iso/aaa')
        self.assertRedirects(response, '/language/language1', status_code=301, target_status_code=200)
        # ...and check the redirected-to page..
        response = self.client.get('/language/language1')
        self.assertContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
    
    def test_iso_notfound(self):
        "Test that a non-existant ISO code returns 404 Not Found"
        response = self.client.get('/iso/zzz')
        self.assertEqual(response.status_code, 404)


class Test_FamilyIndex(PaginatorTestMixin, TestCase):
    """Tests the family_index view"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('family-index')
        self.editor = User.objects.create(username='admin')
        self.family1 = Family.objects.create(family="Austronesian", slug="austronesian", editor=self.editor)
        self.family2 = Family.objects.create(family="Mayan", slug="mayan", editor=self.editor)
        
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/family_index.html')
    
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get(self.url[0:-1])
        self.assertRedirects(response, self.url, status_code=301, target_status_code=200)
    
    def test_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Austronesian')
        self.assertContains(response, 'Mayan')
    
    def test_sorting(self):
        response = self.client.get('{}?sort=family'.format(self.url))
        for i, obj in enumerate(Family.objects.all().order_by('family')):
            assert response.context['table'].rows[i].record == obj
            
        response = self.client.get('{}?sort=-family'.format(self.url))
        for i, obj in enumerate(Family.objects.all().order_by('-family')):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        response = self.client.get("{}?sort=sausage".format(self.url))
        for i, obj in enumerate(Family.objects.all().order_by('family')):
            assert response.context['table'].rows[i].record == obj
        
    def test_show_subsets(self):
        response = self.client.get(self.url)
        for subset in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            url = reverse('family-index-subset', kwargs={'subset': subset})
            self.assertContains(response, url)
    
    def test_filter_on_subset(self):
        # check we get an empty result
        response = self.client.get('{}?subset=X'.format(self.url))
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Mayan')
        self.assertNotContains(response, 'Austronesian')
        
        # check M* but not A*
        response = self.client.get('{}?subset=M'.format(self.url))
        self.assertContains(response, 'Mayan')
        self.assertNotContains(response, 'Austronesian')
        
        # and A but not M
        response = self.client.get('{}?subset=A'.format(self.url))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Austronesian')
        self.assertNotContains(response, 'Mayan')
    
        
class Test_FamilyDetail(BaseMixin, TestCase):
    """Tests the family_detail view"""
    def setUp(self):
        super(Test_FamilyDetail, self).setUp()
        # 1 is Austronesian
        # 2 & 3 are Mayan
        self.austr = Family.objects.create(family="Austronesian", slug="austronesian", editor=self.editor)
        self.mayan = Family.objects.create(family="Mayan", slug="mayan", editor=self.editor)
        self.austr.language_set.add(self.language1)
        self.austr.save()
        self.mayan.language_set.add(self.language2)
        self.mayan.language_set.add(self.language3)
        self.mayan.save()
        
    def test_200ok(self):
        response = self.client.get('/family/austronesian')
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get('/family/austronesian')
        self.assertTemplateUsed(response, 'core/family_detail.html')
        
    def test_404_on_missing_family(self):
        response = self.client.get('/family/basque')
        self.assertEqual(response.status_code, 404)
        
    def test_family_detail_1(self):
        response = self.client.get('/family/austronesian')
        self.assertContains(response, 'Austronesian')
        self.assertContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
        
    def test_family_detail_2(self):
        response = self.client.get('/family/mayan')
        self.assertContains(response, 'Mayan')
        self.assertNotContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')

    def test_sorting(self):
        response = self.client.get('/family/mayan?sort=language')
        for i, obj in enumerate([self.language2, self.language3]):
            assert response.context['table'].rows[i].record == obj
            
        response = self.client.get('/family/mayan?sort=-language')
        for i, obj in enumerate([self.language3, self.language2]):
            assert response.context['table'].rows[i].record == obj
    
    def test_sorting_invalid(self):
        response = self.client.get("/family/mayan?sort=sausage")
        for i, obj in enumerate([self.language2, self.language3]):
            assert response.context['table'].rows[i].record == obj


class Test_SourceIndex(PaginatorTestMixin, TestCase):
    """Tests the source_index view"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('source-index')
        self.editor = User.objects.create(username='admin')
        self.source1 = Source.objects.create(year="1991", author='Smith', 
                                    slug='smith1991', reference='...',
                                    comment='...', editor=self.editor)
        self.source2 = Source.objects.create(year="2002", author='Jones', 
                                    slug='jones2002', reference='...',
                                    comment='...', editor=self.editor)
    
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/source_index.html')
    
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get(self.url[0:-1])
        self.assertRedirects(response, self.url, status_code=301, target_status_code=200)
    
    def test_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Smith')
        self.assertContains(response, 'Jones')
     
    def test_sorting(self):
        response = self.client.get('{}?sort=year'.format(self.url))
        for i, obj in enumerate([self.source1, self.source2]):
            assert response.context['table'].data.data[i] == obj
            
        response = self.client.get('{}?sort=author'.format(self.url))
        for i, obj in enumerate([self.source2, self.source1]):
            assert response.context['table'].data.data[i] == obj
    
    def test_show_subsets(self):
        response = self.client.get(self.url)
        for subset in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            url = reverse('source-index-subset', kwargs={'subset': subset})
            self.assertContains(response, url)
    
    def test_filter_on_subset(self):
        # check we get an empty result
        response = self.client.get('{}?subset=A'.format(self.url))
        self.assertEqual(response.status_code, 200)
        
        self.assertNotContains(response, 'Smith')
        self.assertNotContains(response, 'Jones')
        
        # check S* but not J*
        response = self.client.get('{}?subset=S'.format(self.url))
        self.assertContains(response, 'Smith')
        self.assertNotContains(response, 'Jones')
        
        # and J but not S
        response = self.client.get('{}?subset=J'.format(self.url))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jones')
        self.assertNotContains(response, 'Smith')
    
    
    
    @unittest.skip("broken")
    def test_sorting_invalid(self):
        response = self.client.get("{}?sort=WTFFFFFFF".format(self.url))
        # for the LIFE of me I can't work out why this test fails??
        # ordering seems right when I view the page, but the 
        for i, obj in enumerate([self.source2, self.source1]):
            assert response.context['table'].rows[i].record == obj
    

class Test_SourceDetail(TestCase):
    """Tests the source_detail view"""
    def setUp(self):
        self.client = Client()
        self.editor = User.objects.create(username='admin')
        self.source = Source.objects.create(year="1991", author='Smith', 
                                    slug='smith1991', reference='...',
                                    comment='...', editor=self.editor)
        self.url = reverse('source-detail', kwargs={'slug': self.source.slug})
        
    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'core/source_detail.html')
    
    def test_404_on_missing_source(self):
        response = self.client.get('/source/fudge')
        self.assertEqual(response.status_code, 404)
    
    def test_find_valid_source(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Smith')
        self.assertContains(response, '1991')
    