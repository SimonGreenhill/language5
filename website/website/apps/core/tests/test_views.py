from django.test import TestCase
from django.test.client import Client
from website.apps.core.models import Source

class Test_LanguageIndex(TestCase):
    """Tests the Language Index page"""
    fixtures = ['test_core.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get('/language')
        self.assertRedirects(response, '/language/', status_code=301, target_status_code=200)
    
    def test_index(self):
        "Test languages.index"
        response = self.client.get('/language/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')


class Test_LanguageDetails(TestCase):
    """Tests the Language Details Page"""
    fixtures = ['test_core.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_details(self):
        "Test the default details view"
        response = self.client.get('/language/language1')
        self.assertEqual(response.status_code, 200)

    def test_redirect_on_alternate_names(self):
        "Test redirection to canonical URL when given an alternate name"
        # Check that response to an existing language is 200 OK.
        response = self.client.get('/language/language1')
        self.assertEqual(response.status_code, 200)
        
        # Check that response to ./fudge/ is 302 and redirected
        response = self.client.get('/language/fudge')
        self.assertRedirects(response, '/language/language1', status_code=301, target_status_code=200)
        
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
        self.assertContains(response, 'fudge')

    def test_bad_paginator(self):
        response = self.client.get('/language/language1?page=10000')
        self.assertEqual(response.status_code, 404)
        
    def test_bad_nonint_paginator(self):
        response = self.client.get('/language/language1?page=banana')
        self.assertEqual(response.status_code, 404)



class Test_ISOLookup(TestCase):
    """
    Tests the differential output under the ISO lookup `isolookup`.
    
    Logic:
        No matching entries - raise 404
        1 Matching entry - redirect to languages.details page
        >1 Matching entries - show a list of the languages
    """
    fixtures = ['test_core.json']
    def setUp(self):
        self.client = Client()
    
    def test_multiple_iso_entries(self):
        "Test that ISO codes with multiple languages returns a list"
        # check that /iso/aaa/ is sent to a list of pages.
        response = self.client.get('/iso/aaa')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/language_index.html')
        self.assertContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertNotContains(response, 'Language3')
    
    def test_redirect_on_unique_iso(self):
        "Test that a request for a unique ISO is redirected to the languages.details page"
        response = self.client.get('/iso/bbb')
        self.assertRedirects(response, '/language/language3', status_code=301, target_status_code=200)
        # ...and check the redirected-to page..
        response = self.client.get('/language/language3')
        self.assertContains(response, 'Language3')
        self.assertNotContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
    
    def test_iso_notfound(self):
        "Test that a non-existant ISO code returns 404 Not Found"
        response = self.client.get('/iso/zzz')
        self.assertEqual(response.status_code, 404)



class Test_FamilyIndex(TestCase):
    """Tests the family_index view"""
    fixtures = ['test_core.json']
    def setUp(self):
        self.client = Client()
    
    def missing_trailing_slash(self):
        """index pages should redirect to trailing slash"""
        response = self.client.get('/family')
        self.assertRedirects(response, '/family/', status_code=301, target_status_code=200)
    
    def test_family_index(self):
        response = self.client.get('/family/')
        self.assertContains(response, 'Austronesian')
        self.assertContains(response, 'Mayan')
        
        
        
        
class Test_FamilyDetail(TestCase):
    """Tests the family_detail view"""
    fixtures = ['test_core.json']
    def setUp(self):
        self.client = Client()
    
    def test_404_on_missing_family(self):
        response = self.client.get('/family/basque')
        self.assertEqual(response.status_code, 404)
        
    def test_family_detail_1(self):
        response = self.client.get('/family/austronesian')
        self.assertContains(response, 'Austronesian')
        # 1 & 3 are Austronesian
        self.assertContains(response, 'Language1')
        self.assertNotContains(response, 'Language2')
        self.assertContains(response, 'Language3')
    
    def test_family_detail_2(self):
        response = self.client.get('/family/mayan')
        self.assertContains(response, 'Mayan')
        # 2 & 3 are Mayan
        self.assertNotContains(response, 'Language1')
        self.assertContains(response, 'Language2')
        self.assertContains(response, 'Language3')



class Test_SourceDetail(TestCase):
    """Tests the source_detail view"""
    fixtures = ['test_core.json']
    def setUp(self):
        self.client = Client()
        
    def test_404_on_missing_source(self):
        response = self.client.get('/source/fudge')
        self.assertEqual(response.status_code, 404)
        
    def test_find_valid_source(self):
        response = self.client.get('/source/testsource')
        self.assertContains(response, 'Greenhill')
        
    def test_paginator(self):
        response = self.client.get('/source/testsource?page=1')
        self.assertContains(response, 'Greenhill')
        
    def test_bad_paginator(self):
        response = self.client.get('/source/testsource?page=10000')
        self.assertEqual(response.status_code, 404)
        
    def test_bad_nonint_paginator(self):
        response = self.client.get('/source/testsource?page=banana')
        self.assertEqual(response.status_code, 404)
