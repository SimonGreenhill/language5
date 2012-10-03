import re

from unittest import expectedFailure

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.conf import settings

from core.models import *

from olac.views import parse_time

TEST_DOMAIN = settings.WEBSITE_DOMAIN #'example.com'
OLAC_SETTINGS = {
    'oai_url': TEST_DOMAIN,
    'repositoryName': 'repos_name',
    'description': 'Generic OLAC repository',
    'repositoryIdentifier': TEST_DOMAIN,
    'baseURL': 'http://%s/oai' % TEST_DOMAIN,
    'adminEmail': ['bob@example.com'],
    'admins': [('Bob. G. Admin', 'bob@example.com')],
    'deletedRecord': 'no', # deletedRecord policy
    'protocolVersion': '2.0', # the version of the OAI-PMH supported by the repository;
    '_identifier': re.compile(r"""oai:%s:(\w{3})\.(\d+)""" % TEST_DOMAIN.replace(".", "\.")),
    'institution': 'Test, Inc',
    'institutionURL': 'http://example.com',
    'shortLocation': 'Auckland, New Zealand',
}
OLAC_SETTINGS['depositor'] = OLAC_SETTINGS['admins']

def url(token):
    return 'http://%s/language/%s' % (TEST_DOMAIN, token)
    
    
class TestDateTimeParsing(TestCase):
    def test_one(self):
        from django.utils.timezone import utc
        t = parse_time('2011-01-01')
        assert t.tzinfo == utc
        assert t.year == 2011
        assert t.month == 01
        assert t.day == 01
        

@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class TestValidIdentifiers(TestCase):
    def setUp(self):
        self.pattern = OLAC_SETTINGS.get('_identifier')
        
    def test_one(self):
        assert self.pattern.match('oai:%s:aaa.1' % TEST_DOMAIN)
        assert self.pattern.match('oai:%s:aaa.1' % TEST_DOMAIN).groups()[0] == 'aaa'
        assert self.pattern.match('oai:%s:aaa.1' % TEST_DOMAIN).groups()[1] == '1'
        
    def test_two(self):
        assert self.pattern.match('oai:%s:bbb.2' % TEST_DOMAIN)
        assert self.pattern.match('oai:%s:bbb.2' % TEST_DOMAIN).groups()[0] == 'bbb'
        assert self.pattern.match('oai:%s:bbb.2' % TEST_DOMAIN).groups()[1] == '2'
        
    def test_real(self):
        assert self.pattern.match('oai:%s:mri.75' % TEST_DOMAIN)
        assert self.pattern.match('oai:%s:mri.75' % TEST_DOMAIN).groups()[0] == 'mri'
        assert self.pattern.match('oai:%s:mri.75' % TEST_DOMAIN).groups()[1] == '75'


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_Identify(TestCase):
    #This verb takes no arguments and returns information about a repository 
    fixtures = ['testdata.json']
    
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/oai/?verb=Identify')
        
    def test_identify(self):
        assert "<Identify>" in self.response.content
    
    def test_identify_noargs(self):
        # Identify should also be generated if no verb is given
        response = self.client.get('/oai/')
        assert "<Identify>" in response.content
        
    def test_has_repositoryName(self):
        # `repositoryName`:   a human readable name for the repository;
        assert re.search(r"<repositoryName>(.*)</repositoryName>", self.response.content)
        
    def test_has_baseURL(self):
        # `baseURL`:          the base URL of the repository;
        assert re.search(r"<baseURL>(.*)</baseURL>", self.response.content)
        
    def test_has_protocolVersion(self):
        # `protocolVersion`:  the version of the OAI-PMH supported by the repository;
        assert '<protocolVersion>2.0</protocolVersion>' in self.response.content
        
    def test_has_earliestDatestamp(self):
        # `earliestDatestamp`: a UTCdatetime that is the guaranteed lower limit 
        #   of all datestamps recording changes, modifications, or deletions in the 
        #   repository. A repository must not use datestamps lower than the one 
        #   specified by the content of the earliestDatestamp element. 
        #   earliestDatestamp must be expressed at the finest granularity 
        #   supported by the repository.
        assert re.search(r"<earliestDatestamp>(.*)</earliestDatestamp>", self.response.content)
        
    def test_has_deletedRecord(self):
        # `deletedRecord`:    the manner in which the repository supports the notion 
        #     of deleted records. Legitimate values are no ; transient ; 
        #     persistent with meanings defined in the section on deletion.
        assert re.search(r"<deletedRecord>(.*)</deletedRecord>", self.response.content)
        
    def test_has_granularity(self):
        # `granularity`:      the finest harvesting granularity supported by the 
        #     repository. The legitimate values are YYYY-MM-DD and 
        #     YYYY-MM-DDThh:mm:ssZ with meanings as defined in ISO8601.
        assert "<granularity>YYYY-MM-DD</granularity>" in self.response.content
        
    def test_has_adminEmail(self):
        # The response must include one or more instances of the following element:
        # `adminEmail` : the e-mail address of an administrator of the repository.
        assert re.search(r"<adminEmail>(.*)</adminEmail>", self.response.content)
        
    def test_identify_error_with_extra_args(self):
        # Identify should NOT accept any other arguments
        response = self.client.get('/oai/?verb=Identify&test=test')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListIdentifiers(TestCase):
    # This verb is an abbreviated form of ListRecords, retrieving only headers 
    # rather than records. Optional arguments permit selective harvesting of 
    # headers based on set membership and/or datestamp. Depending on the 
    # repository's support for deletions, a returned header may have a status 
    # attribute of "deleted" if a record matching the arguments specified in 
    # the request has been deleted.
    fixtures = ['testdata.json']
    
    def setUp(self):
        self.client = Client()
        
    def test_listidentifiers(self):
        # Identify should also be generated if no verb is given
        response = self.client.get('/oai/?verb=ListIdentifiers&metadataPrefix=olac')
        assert response.status_code == 200
        assert len(response.context['object_list']) == 3
        assert response.context['object_list'][0].language == 'Language1'
        assert response.context['object_list'][1].language == 'Language2'
        assert response.context['object_list'][2].language == 'Language3'
        
    def test_from_nochange(self):
        # `from`:      an optional argument with a UTCdatetime value, which specifies
        #                 a lower bound for datestamp-based selective harvesting.
        # `until`:     an optional argument with a UTCdatetime value, which specifies 
        #                 a upper bound for datestamp-based selective harvesting.
        # Language1 added on 2010-01-15 03:10:51
        # Language2 added on 2010-02-15 03:10:51
        
        # use `from` parameter but no filtering
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2010-01-01&metadataPrefix=olac')
        assert len(response.context['object_list']) == 3
        
    def test_until_nochange(self):
        # use `until` parameter, but no filtering
        response = self.client.get('/oai/?verb=ListIdentifiers&until=2012-12-31&metadataPrefix=olac')
        assert len(response.context['object_list']) == 3
        
    def test_from(self):
        # filter on `from`, ignoring Language 1 & 2
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2012-01-01&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'
        
    def test_until(self):
        # filter on `until` ignoring language 2 & 3
        response = self.client.get('/oai/?verb=ListIdentifiers&until=2011-01-01&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language1'
        
    def test_from_until(self):
        # filter with `from` and `until`, ignoring Language 1 & 3
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2011-01-01&until=2011-12-30&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language2'
        
    def test_from_until_top(self):
        # filter with `from` and `until`, ignoring all languages before 2012 (1,2)
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2012-01-01&until=2012-12-30&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'
        
    def test_from_until_bottom(self):
        # filter with `from` and `until`, ignoring all languages after 2011 (2,3)
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2011-12-30&until=2012-12-30&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'
        
    def test_bad_from_arg(self):
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2009-SS-0asf&metadataPrefix=olac')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
        
    def test_bad_until_arg(self):
        response = self.client.get('/oai/?verb=ListIdentifiers&until=asdasdad&metadataPrefix=olac')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
        
    def test_error_on_no_metadataPrefix(self):
        # `metadataPrefix`:   a required argument, which specifies that headers should
        #                 be returned only if the metadata format matching the supplied
        #                 metadataPrefix is available or, depending on the repository's
        #                 support for deletions, has been deleted. The metadata formats
        #                 supported by a repository and for a particular item can be
        #                 retrieved using the ListMetadataFormats request.
        response = self.client.get('/oai/?verb=ListIdentifiers')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
        
    def test_error_on_invalid_metadataPrefix(self):
        #     `cannotDisseminateFormat` - The value of the metadataPrefix argument is not
        #         supported by the repository.
        response = self.client.get('/oai/?verb=ListIdentifiers&until=asdasdad&metadataPrefix=fudge')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="cannotDisseminateFormat">' in response.content
    
    def test_error_with_conflicting_metadataPrefix(self):
        response = self.client.get('/oai/?verb=ListIdentifiers&metadataPrefix=oai_dc&metadataPrefix=oai_dc')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
    
    def test_set_raises_error(self):
        # `set`:      an optional argument with a setSpec value, which specifies set
        #                 criteria for selective harvesting.
        #     `noSetHierarchy` - The repository does not support sets.
        # Have not implemented this as unnecessary
        response = self.client.get('/oai/?verb=ListIdentifiers&set=foo&metadataPrefix=olac')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="noSetHierarchy">' in response.content
        
    def test_norecordsmatch(self):
        #     `noRecordsMatch` - The combination of the values of the from, until, and set
        #         arguments results in an empty list.
        response = self.client.get('/oai/?verb=ListIdentifiers&from=2010-05-01&until=2010-05-02&metadataPrefix=olac')
        assert '<error code="noRecordsMatch">' in response.content
        
    def test_error_on_resumptionToken(self):
        # `resumptionToken`:   an exclusive argument with a value that is the flow 
        #             control token returned by a previous ListIdentifiers request 
        #             that issued an incomplete list.
        #     `badResumptionToken` - The value of the resumptionToken argument is invalid or
        #         expired.
        # NOT Implemented as unnecessary
        response = self.client.get('/oai/?verb=ListIdentifiers&resumptionToken=foo&metadataPrefix=olac')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badResumptionToken">' in response.content
        
    def test_multiple_errors(self):
        response = self.client.get('/oai/?verb=ListIdentifiers&resumptionToken=junktoken')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badResumptionToken">' in response.content
        assert '<error code="badArgument">' in response.content
        
    def test_not_return_languages_with_missing_isocodes(self):
        l = Language.objects.get(pk=2)
        l.isocode = ''
        l.save()
        response = self.client.get('/oai/?verb=ListIdentifiers&metadataPrefix=olac')
        assert len(response.context['object_list']) == 2
        assert response.context['object_list'][0].language == 'Language1'


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListSets(TestCase):
    # Not Implemented as no set hierarchy available.
    def test_listSets(self):
        # Identify should also be generated if no verb is given
        response = Client().get('/oai/?verb=ListSets')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="noSetHierarchy">' in response.content
    


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListRecords(TestCase):
    """General tests for ListRecords"""
    fixtures = ['testdata.json']
    
    def setUp(self):
        self.client = Client()
        
    def test_error_on_no_metadataPrefix(self):
        response = self.client.get('/oai/?verb=ListRecords')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
        
    def test_error_on_bad_metadataPrefix(self):
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=fudge')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="cannotDisseminateFormat">' in response.content
    
    def test_error_on_set(self):
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac&set=foo')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="noSetHierarchy">' in response.content
    
    def test_error_on_resumptionToken(self):
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac&resumptionToken=foo')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badResumptionToken">' in response.content
    
    def test_until(self):
        # filter on `until` ignoring language 2 & 3
        response = self.client.get('/oai/?verb=ListRecords&until=2011-01-30&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language1'
    
    def test_from_until(self):
        # filter with `from` and `until`, ignoring Language 1 & 3
        response = self.client.get('/oai/?verb=ListRecords&from=2011-01-01&until=2011-12-31&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language2'
        
    def test_from_until_top(self):
        # filter with `from` and `until`, ignoring all languages before 2012 (1,2)
        response = self.client.get('/oai/?verb=ListRecords&from=2012-01-01&until=2012-12-30&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'
        
    def test_from_until_bottom(self):
        # filter with `from` and `until`, ignoring all languages after 2011 (2,3)
        response = self.client.get('/oai/?verb=ListRecords&from=2011-12-30&until=2012-12-30&metadataPrefix=olac')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'
        
    def test_multiple_errors(self):
        response = self.client.get('/oai/?verb=ListRecords&resumptionToken=junktoken')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badResumptionToken">' in response.content
        assert '<error code="badArgument">' in response.content
        
    def test_not_return_languages_with_missing_isocodes(self):
        l = Language.objects.get(pk=2)
        l.isocode = ''
        l.save()
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac')
        assert len(response.context['object_list']) == 2


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListRecords_metadataPrefix_oai_dc(TestCase):
    """Test the metadata for the `ListRecords` command under the oai_dc mode"""
    fixtures = ['testdata.json']
    
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=oai_dc')
    
    def test_oai_dc(self):
        self.assertContains(self.response, '<oai_dc:dc', count=3)
    
    def test_dc_title(self):
        self.assertContains(self.response, '<dc:title', count=3)
    
    def test_dc_description(self):
        self.assertContains(self.response, '<dc:description', count=3)
    
    def test_dc_publisher(self):
        self.assertContains(self.response, '<dc:publisher', count=3)
    
    def test_dc_date(self):
        self.assertContains(self.response, '<dc:date', count=3)
        
    def test_dc_date_W3CDTF(self):
        self.assertContains(self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=3)
    
    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=3)
    
    def test_dc_identifier_is_correct_url(self):
        self.assertContains(self.response, 
            '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>' % url('language1'),
             count=1)
        self.assertContains(self.response, 
            '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>' % url('language2'), 
            count=1)
        self.assertContains(self.response, 
            '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>' % url('language3'), 
            count=1)
    
    def test_dc_type_dcterms(self):
        self.assertContains(self.response, '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>', count=3)
        

@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListRecords_metadataPrefix_olac(TestCase):
    """Test the metadata for the `ListRecords` command under the olac mode"""
    fixtures = ['testdata.json']

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac')
        
    def test_olac(self):
        self.assertContains(self.response, '<olac:olac', count=3)

    def test_dc_title(self):
        self.assertContains(self.response, '<dc:title', count=3)

    def test_dc_description(self):
        self.assertContains(self.response, '<dc:description', count=3)

    def test_dc_publisher(self):
        self.assertContains(self.response, '<dc:publisher', count=3)

    def test_dc_date(self):
        self.assertContains(self.response, '<dc:date', count=3)

    def test_dc_date_W3CDTF(self):
        self.assertContains(self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=3)

    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=3)
    
    def test_dc_identifier_is_correct_url(self):
        self.assertContains(self.response, 'language/language1</dc:identifier>', count=1)
        self.assertContains(self.response, 'language/language2</dc:identifier>', count=1)
        self.assertContains(self.response, 'language/language3</dc:identifier>', count=1)
        
    def test_dc_type_dcterms(self):
        self.assertContains(self.response, '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>', count=3)
        
    def test_dc_type_lexicon(self):
        self.assertContains(self.response, '<dc:type xsi:type="olac:linguistic-type" olac:code="lexicon"/>', count=3)
    
    @expectedFailure # NEED TO IMPLEMENT DATA MODEL
    def test_dcterms_extent(self):
        # 3 for L1, 4 for L2
        self.assertContains(self.response, '<dcterms:extent>3 entries</dcterms:extent>', count=1)
        self.assertContains(self.response, '<dcterms:extent>4 entries</dcterms:extent>', count=1)
    
    
@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_GetRecord(TestCase):
    """General tests for GetRecord"""
    fixtures = ['testdata.json']

    def setUp(self):
        self.client = Client()

    def test_error_on_no_metadataPrefix(self):
        response = self.client.get('/oai/?verb=GetRecord')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
        
    def test_error_on_bad_metadataPrefix(self):
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=fudge')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="cannotDisseminateFormat">' in response.content
    
    def test_error_on_no_identifier(self):
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=olac')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="badArgument">' in response.content
    
    def test_error_on_bad_identifier(self):
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=olac&identifier=simonrocks!')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        assert '<error code="idDoesNotExist">' in response.content



@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_GetRecord_metadataPrefix_oai_dc(TestCase):
    """Test the metadata for the `GetRecord` command under the oai_dc mode"""
    fixtures = ['testdata.json']
    
    def setUp(self):
        self.client = Client()
        id = 'oai:xxx:aaa.1'
        self.response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s' % id)
    
    def test_oai_dc(self):
        self.assertContains(self.response, '<oai_dc:dc', count=1)

    def test_dc_title(self):
        self.assertContains(self.response, '<dc:title', count=1)

    def test_dc_description(self):
        self.assertContains(self.response, '<dc:description', count=1)

    def test_dc_publisher(self):
        self.assertContains(self.response, '<dc:publisher', count=1)

    def test_dc_date(self):
        self.assertContains(self.response, '<dc:date', count=1)

    def test_dc_date_W3CDTF(self):
        self.assertContains(self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=1)

    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=1)
    
    def test_dc_identifier_is_correct_url(self):
        self.assertContains(self.response, 
            '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>' % url('language1'), count=1)
        
    def test_dc_type_dcterms(self):
        self.assertContains(self.response, '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>', count=1)

    def test_dc_description(self):
        self.assertContains(self.response, '<dc:description>Vocabulary for Language1', count=1)
    
 
@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_GetRecord_metadataPrefix_olac(TestCase):
    """Test the metadata for the `GetRecord` command under the olac mode"""
    fixtures = ['testdata.json']

    def setUp(self):
        self.client = Client()
        id = 'oai:%s:bbb.2'
        self.response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=olac&identifier=%s' % id)
    
    def test_olac(self):
        self.assertContains(self.response, '<olac:olac', count=1)

    def test_dc_title(self):
        self.assertContains(self.response, '<dc:title', count=1)

    def test_dc_description(self):
        self.assertContains(self.response, '<dc:description', count=1)

    def test_dc_publisher(self):
        self.assertContains(self.response, '<dc:publisher', count=1)

    def test_dc_date(self):
        self.assertContains(self.response, '<dc:date', count=1)
    
    def test_dc_date_W3CDTF(self):
        self.assertContains(self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=1)
        
    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=1)
        
    def test_dc_identifier_is_correct_url(self):
        self.assertContains(self.response, 
            '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>' % url('language2'), count=1)

    def test_dc_type_dcterms(self):
        self.assertContains(self.response, '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>', count=1)

    def test_dc_type_lexicon(self):
        self.assertContains(self.response, '<dc:type xsi:type="olac:linguistic-type" olac:code="lexicon"/>', count=1)
    
    def test_dc_description(self):
        self.assertContains(self.response, '<dc:description>Vocabulary for Language2', count=1)
    
    @expectedFailure # NEED TO IMPLEMENT DATA MODEL
    def test_dcterms_extent(self):
        # 3 for L1, 4 for L2
        self.assertContains(self.response, '<dcterms:extent>4 entries</dcterms:extent>', count=1)


class TestNoHTML(TestCase):
    """Test that the XML output does not contain html entities."""
    
    fixtures = ['testdata.json']
    
    def test_one(self):
        l = Language.objects.get(pk=2)
        l.language = '<language2'
        l.save()
        client = Client()
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:%s:aaa.%d' % (TEST_DOMAIN, l.id))
        self.assertNotContains(response, '&lt;')
        self.assertNotContains(response, '&gt;')
        
    def test_two(self):
        l = Language.objects.get(pk=2)
        l.language = 'lang&uage2'
        l.save()
        client = Client()
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:%s:aaa.%d' % (TEST_DOMAIN, l.id))
        self.assertNotContains(response, '&amp;')
