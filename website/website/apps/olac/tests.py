import re
from xml.dom import minidom

from django.test import TestCase, override_settings
from django.test.client import Client

from website.apps.core.models import Language

from website.apps.olac.views import parse_time, check_ident

# NOTE: as at Oct 2010, the override_settings decorator doesn't seem to
# work if defined at the class level.
#
# >>> @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
#
# It does seem to work if placed on the setUp() function


TEST_DOMAIN = 'myolacsite.com'
TEST_SITENAME = 'My Olac Site'
TEST_ADMINS = [('Bob. G. Admin', 'bob@example.com')]

OLAC_SETTINGS = {
    'sitename': TEST_SITENAME,
    'repositoryName': TEST_SITENAME,
    'sitedomain': TEST_DOMAIN,
    'oai_url': TEST_DOMAIN,
    'repositoryIdentifier': TEST_DOMAIN,
    'baseURL': 'http://%s/oai' % TEST_DOMAIN,
    'description': 'Generic OLAC repository',
    'adminEmail': ['bob@example.com'],
    'admins': TEST_ADMINS,
    'depositor': TEST_ADMINS,
    'deletedRecord': 'no',
    'protocolVersion': '2.0',
    '_identifier': re.compile(
        r"""oai:%s:(\w{3})\.(\d+)""" % TEST_DOMAIN.replace(".", "\.")
    ),
    'institution': 'Test, Inc',
    'institutionURL': 'http://example.com',
    'shortLocation': 'Auckland, New Zealand',
}

def url(token):
    return 'http://%s/language/%s' % (TEST_DOMAIN, token)

class TestSiteNameSetProperly(TestCase):
    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get('/oai/?verb=Identify')

    def test_sitename(self):
        self.assertEquals(
            TEST_SITENAME,
            self.response.context['OLAC']['sitename']
        )
        self.assertEquals(
            OLAC_SETTINGS['sitename'],
            self.response.context['OLAC']['sitename']
        )

    def test_sitedomain(self):
        self.assertEquals(
            TEST_DOMAIN,
            self.response.context['OLAC']['sitedomain']
        )
        self.assertEquals(
            OLAC_SETTINGS['sitedomain'],
            self.response.context['OLAC']['sitedomain']
        )


class TestValidIdentifiers(TestCase):
    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.pattern = OLAC_SETTINGS.get('_identifier')

    def test_one(self):
        match = self.pattern.match('oai:%s:aaa.1' % TEST_DOMAIN)
        assert match.groups()[0] == 'aaa'
        assert match.groups()[1] == '1'

    def test_two(self):
        match = self.pattern.match('oai:%s:bbb.27' % TEST_DOMAIN)
        assert match.groups()[0] == 'bbb'
        assert match.groups()[1] == '27'

    def test_check_ident(self):
        ident = 'oai:%s:aaa.1' % TEST_DOMAIN
        assert check_ident(ident)
        assert check_ident(ident).groups()[0] == 'aaa'
        assert check_ident(ident).groups()[1] == '1'


class Test_Identify(TestCase):
    #This verb takes no arguments and returns information about a repository
    fixtures = ['test_core.json']

    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get('/oai/?verb=Identify')

    def test_valid_xml(self):
        minidom.parseString(self.response.content)

    def test_identify(self):
        self.assertContains(self.response, "<Identify>", 1)

    def test_identify_noargs(self):
        # Identify should also be generated if no verb is given
        self.assertContains(self.response, "<Identify>", 1)

    def test_has_repositoryName(self):
        # `repositoryName`:   a human readable name for the repository;
        assert re.search(
            r"<repositoryName>(.*)</repositoryName>",
            self.response.content.decode('utf8')
        )

    def test_has_baseURL(self):
        # `baseURL`:          the base URL of the repository;
        assert re.search(
            r"<baseURL>(.*)</baseURL>",
            self.response.content.decode('utf8')
        )

    def test_baseURL_is_complete(self):
        found = re.search(r"<baseURL>(.*)</baseURL>", self.response.content.decode('utf8'))
        assert found.groups()[0] == 'http://%s/oai/' % TEST_DOMAIN

    def test_has_protocolVersion(self):
        # `protocolVersion`:  the version of the OAI-PMH supported
        self.assertContains(self.response, '<protocolVersion>2.0</protocolVersion>', 1)

    def test_has_earliestDatestamp(self):
        # `earliestDatestamp`: a UTCdatetime that is the guaranteed lower limit
        #   of all datestamps recording changes, modifications, or deletions in
        #   the repository. A repository must not use datestamps lower than the
        #   one specified by the content of the earliestDatestamp element.
        #   earliestDatestamp must be expressed at the finest granularity
        #   supported by the repository.
        assert re.search(
            r"<earliestDatestamp>(.*)</earliestDatestamp>",
            self.response.content.decode('utf8')
        )

    def test_has_deletedRecord(self):
        # `deletedRecord`:    the manner in which the repository supports the
        # notion of deleted records. Legitimate values are no ; transient ;
        # persistent with meanings defined in the section on deletion.
        assert re.search(
            r"<deletedRecord>(.*)</deletedRecord>",
            self.response.content.decode('utf8')
        )

    def test_has_granularity(self):
        # `granularity`:      the finest harvesting granularity supported by
        # the repository. The legitimate values are YYYY-MM-DD and
        # YYYY-MM-DDThh:mm:ssZ with meanings as defined in ISO8601.
        self.assertContains(self.response, "<granularity>YYYY-MM-DD</granularity>", 1)

    def test_has_adminEmail(self):
        # The response must include one or more instances of the following
        # element: `adminEmail` : the e-mail address of an administrator of the
        # repository.
        assert re.search(
            r"<adminEmail>(.*)</adminEmail>",
            self.response.content.decode('utf8')
        )

    def test_identify_error_with_extra_args(self):
        # Identify should NOT accept any other arguments
        response = self.client.get('/oai/?verb=Identify&test=test')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)


class Test_ListIdentifiers(TestCase):
    # This verb is an abbreviated form of ListRecords, retrieving only headers
    # rather than records. Optional arguments permit selective harvesting of
    # headers based on set membership and/or datestamp. Depending on the
    # repository's support for deletions, a returned header may have a status
    # attribute of "deleted" if a record matching the arguments specified in
    # the request has been deleted.
    fixtures = ['test_core.json']

    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = '/oai/?verb=ListIdentifiers&metadataPrefix=olac'

    def test_valid_xml(self):
        minidom.parseString(self.client.get(self.url).content)

    def test_listidentifiers(self):
        # Identify should also be generated if no verb is given
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert len(response.context['object_list']) == 3
        assert response.context['object_list'][0].language == 'Language1'
        assert response.context['object_list'][1].language == 'Language2'
        assert response.context['object_list'][2].language == 'Language3'

    def test_from_nochange(self):
        # `from`:      an optional argument with a UTCdatetime value, which
        # specifies a lower bound for datestamp-based selective harvesting.
        # `until`:     an optional argument with a UTCdatetime value, which
        # specifies a upper bound for datestamp-based selective harvesting.
        #
        # Language1 added on 2010-01-15 03:10:51
        # Language2 added on 2010-02-15 03:10:51
        # use `from` parameter but no filtering
        response = self.client.get("%s&from=2010-01-01" % self.url)
        assert len(response.context['object_list']) == 3

    def test_until_nochange(self):
        # use `until` parameter, but no filtering
        response = self.client.get("%s&until=2012-12-31" % self.url)
        assert len(response.context['object_list']) == 3

    def test_from(self):
        # filter on `from`, ignoring Language 1 & 2
        response = self.client.get("%s&from=2012-01-01" % self.url)
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'

    def test_until(self):
        # filter on `until` ignoring language 2 & 3
        response = self.client.get('%s&until=2011-01-01' % self.url)
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language1'

    def test_from_until(self):
        # filter with `from` and `until`, ignoring Language 1 & 3
        response = self.client.get(
            "%s&from=2011-01-01&until=2011-12-30" % self.url
        )
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language2'

    def test_from_until_top(self):
        # filter with `from` and `until`, ignoring all languages before 2012
        # (1, 2)
        response = self.client.get(
            '%s&from=2012-01-01&until=2012-12-30' % self.url
        )
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'

    def test_from_until_bottom(self):
        # filter with `from` and `until`, ignoring all languages after 2011 (2,
        # 3)
        response = self.client.get(
            '%s&from=2011-12-30&until=2012-12-30' % self.url
        )
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'

    def test_bad_from_arg(self):
        response = self.client.get('%s&from=2009-SS-0asf' % self.url)
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_bad_until_arg(self):
        response = self.client.get('%s&until=asdasdad' % self.url)
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_error_on_no_metadataPrefix(self):
        # `metadataPrefix`:   a required argument, which specifies that headers
        # should be returned only if the metadata format matching the supplied
        # metadataPrefix is available or, depending on the repository's support
        # for deletions, has been deleted. The metadata formats supported by a
        # repository and for a particular item can be retrieved using the
        # ListMetadataFormats request.
        response = self.client.get('/oai/?verb=ListIdentifiers')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)
        
    def test_error_on_invalid_metadataPrefix(self):
        # `cannotDisseminateFormat` - The value of the metadataPrefix argument
        # is not supported by the repository.
        bad = self.url.replace('metadataPrefix=olac', 'metadataPrefix=fudge')
        response = self.client.get('%s&until=asdasdad' % bad)
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="cannotDisseminateFormat">', 1)
    
    def test_error_with_conflicting_metadataPrefix(self):
        response = self.client.get('%s&metadataPrefix=oai_dc' % self.url)
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_set_raises_error(self):
        # `set`: an optional argument with a setSpec value, which
        # specifies set criteria for selective harvesting.
        # `noSetHierarchy` - The repository does not support sets.
        # Have not implemented this as unnecessary
        response = self.client.get('%s&set=foo' % self.url)
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="noSetHierarchy">', 1)

    def test_norecordsmatch(self):
        # `noRecordsMatch` - The combination of the values of the from, until,
        # and set arguments results in an empty list.
        response = self.client.get(
            '%s&from=2010-05-01&until=2010-05-02' % self.url
        )
        self.assertContains(response, '<error code="noRecordsMatch">', 1)

    def test_error_on_resumptionToken(self):
        # `resumptionToken`:   an exclusive argument with a value that is the
        # flow control token returned by a previous ListIdentifiers request
        # that issued an incomplete list.  `badResumptionToken` - The value of
        # the resumptionToken argument is invalid or expired.
        # NOT Implemented as unnecessary
        response = self.client.get('%s&resumptionToken=foo' % self.url)
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badResumptionToken">', 1)

    def test_multiple_errors(self):
        response = self.client.get(
            '/oai/?verb=ListIdentifiers&resumptionToken=junktoken'
        )
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badResumptionToken">', 1)
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_not_return_languages_with_missing_isocodes(self):
        l = Language.objects.get(pk=2)
        l.isocode = ''
        l.save()
        response = self.client.get(
            '/oai/?verb=ListIdentifiers&metadataPrefix=olac'
        )
        assert len(response.context['object_list']) == 2
        assert response.context['object_list'][0].language == 'Language1'


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListSets(TestCase):
    # Not Implemented as no set hierarchy available.
    response = Client().get('/oai/?verb=ListSets')
    
    def test_listSets(self):
        # Identify should also be generated if no verb is given
        self.assertTemplateUsed(self.response, 'olac/Error.xml')
        self.assertContains(self.response, '<error code="noSetHierarchy">', 1)

    def test_valid_xml(self):
        minidom.parseString(self.response.content)


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_ListRecords(TestCase):
    """General tests for ListRecords"""
    fixtures = ['test_core.json']
    client = Client()

    def test_valid_xml(self):
        minidom.parseString(self.client.get('/oai/?verb=ListRecords').content)

    def test_error_on_no_metadataPrefix(self):
        response = self.client.get('/oai/?verb=ListRecords')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_error_on_bad_metadataPrefix(self):
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=fudge')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="cannotDisseminateFormat">', 1)

    def test_error_on_set(self):
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac&set=foo')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="noSetHierarchy">', 1)

    def test_error_on_resumptionToken(self):
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac&resumptionToken=foo')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badResumptionToken">', 1)

    def test_until(self):
        # filter on `until` ignoring language 2 & 3
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac&until=2011-01-30')
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language1'

    def test_from_until(self):
        # filter with `from` and `until`, ignoring Language 1 & 3
        response = self.client.get(
            "/oai/?verb=ListRecords&metadataPrefix=olac&from=2011-01-01&until=2011-12-31"
        )
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language2'

    def test_from_until_top(self):
        # filter with `from` and `until`, ignoring all languages before 2012
        # (1,2)
        response = self.client.get(
            '/oai/?verb=ListRecords&metadataPrefix=olac&from=2012-01-01&until=2012-12-30'
        )
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'

    def test_from_until_bottom(self):
        # filter with `from` and `until`, ignoring all languages after 2011
        # (2,3)
        response = self.client.get(
            '/oai/?verb=ListRecords&metadataPrefix=olac&from=2011-12-30&until=2012-12-30'
        )
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0].language == 'Language3'

    def test_multiple_errors(self):
        response = self.client.get(
            '/oai/?verb=ListRecords&resumptionToken=junktoken'
        )
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badResumptionToken">', 1)
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_not_return_languages_with_missing_isocodes(self):
        l = Language.objects.get(pk=2)
        l.isocode = ''
        l.save()
        response = self.client.get('/oai/?verb=ListRecords&metadataPrefix=olac')
        assert len(response.context['object_list']) == 2


class Test_ListRecords_metadataPrefix_oai_dc(TestCase):
    """Test the metadata for the `ListRecords` command under the oai_dc mode"""
    fixtures = ['test_core.json']
    
    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get(
            '/oai/?verb=ListRecords&metadataPrefix=oai_dc'
        )

    def test_valid_xml(self):
        minidom.parseString(self.response.content)

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
        self.assertContains(
            self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=3
        )

    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=3)

    def test_dc_identifier_is_correct_url(self):
        URI = '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>'
        self.assertContains(self.response, URI % url('language1'), count=1)
        self.assertContains(self.response, URI % url('language2'), count=1)
        self.assertContains(self.response, URI % url('language3'), count=1)

    def test_dc_type_dcterms(self):
        self.assertContains(
            self.response,
            '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>',
            count=3
        )


class Test_ListRecords_metadataPrefix_olac(TestCase):
    """Test the metadata for the `ListRecords` command under the olac mode"""
    fixtures = ['test_core.json']
    
    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        cls.response = cls.client.get(
            '/oai/?verb=ListRecords&metadataPrefix=olac'
        )

    def test_valid_xml(self):
        minidom.parseString(self.response.content)

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
        self.assertContains(
            self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=3
        )

    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=3)

    def test_dc_identifier_is_correct_url(self):
        self.assertContains(
            self.response, 'language/language1</dc:identifier>', count=1
        )
        self.assertContains(
            self.response, 'language/language2</dc:identifier>', count=1
        )
        self.assertContains(
            self.response, 'language/language3</dc:identifier>', count=1
        )

    def test_dc_type_dcterms(self):
        self.assertContains(
            self.response,
            '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>',
            count=3
        )

    def test_dc_type_lexicon(self):
        self.assertContains(
            self.response,
            '<dc:type xsi:type="olac:linguistic-type" olac:code="lexicon"/>',
            count=3
        )


@override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
class Test_GetRecord(TestCase):
    """General tests for GetRecord"""
    fixtures = ['test_core.json']
    client = Client()

    def test_valid_xml(self):
        response = self.client.get('/oai/?verb=GetRecord')
        minidom.parseString(response.content)

    def test_error_on_no_metadataPrefix(self):
        response = self.client.get('/oai/?verb=GetRecord')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', )

    def test_error_on_bad_metadataPrefix(self):
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=fudge')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="cannotDisseminateFormat">', 1)

    def test_error_on_no_identifier(self):
        response = self.client.get('/oai/?verb=GetRecord&metadataPrefix=olac')
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="badArgument">', 1)

    def test_error_on_bad_identifier(self):
        response = self.client.get(
            '/oai/?verb=GetRecord&metadataPrefix=olac&identifier=simonrocks!'
        )
        self.assertTemplateUsed(response, 'olac/Error.xml')
        self.assertContains(response, '<error code="idDoesNotExist">', 1)



class Test_GetRecord_metadataPrefix_oai_dc(TestCase):
    """Test the metadata for the `GetRecord` command under the oai_dc mode"""
    fixtures = ['test_core.json']

    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        id = 'oai:%s:aaa.1' % TEST_DOMAIN
        cls.response = cls.client.get(
            '/oai/?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s' % id
        )

    def test_valid_xml(self):
        minidom.parseString(self.response.content)

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
        self.assertContains(
            self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=1
        )

    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=1)

    def test_dc_identifier_is_correct_url(self):
        URI = '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>'
        self.assertContains(self.response, URI % url('language1'), count=1)

    def test_dc_type_dcterms(self):
        self.assertContains(
            self.response,
            '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>',
            count=1
        )

    def test_dc_description_full(self):
        self.assertContains(
            self.response, '<dc:description>Vocabulary for Language1', count=1
        )


class Test_GetRecord_metadataPrefix_olac(TestCase):
    """Test the metadata for the `GetRecord` command under the olac mode"""
    fixtures = ['test_core.json']
    
    @classmethod
    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def setUpTestData(cls):
        cls.client = Client()
        id = 'oai:%s:bbb.2' % TEST_DOMAIN
        cls.response = cls.client.get(
             '/oai/?verb=GetRecord&metadataPrefix=olac&identifier=%s' % id
        )

    def test_valid_xml(self):
        minidom.parseString(self.response.content)

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
        self.assertContains(
            self.response, '<dc:date xsi:type="dcterms:W3CDTF"', count=1
        )

    def test_dc_identifier(self):
        self.assertContains(self.response, '<dc:identifier', count=1)

    def test_dc_identifier_is_correct_url(self):
        DC = '<dc:identifier xsi:type="dcterms:URI">%s</dc:identifier>'
        self.assertContains(self.response, DC % url('language2'), count=1)

    def test_dc_type_dcterms(self):
        self.assertContains(
            self.response,
            '<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>',
            count=1
        )

    def test_dc_type_lexicon(self):
        self.assertContains(
            self.response,
            '<dc:type xsi:type="olac:linguistic-type" olac:code="lexicon"/>',
            count=1
        )

    def test_dc_description_full(self):
        self.assertContains(
            self.response,
            '<dc:description>Vocabulary for Language2',
            count=1
        )


class TestNoHTML(TestCase):
    """Test that the XML output does not contain html entities."""
    # but it *should* in URLS.

    fixtures = ['test_core.json']

    @override_settings(OLAC_SETTINGS=OLAC_SETTINGS)
    def test_nohtml(self):
        l = Language.objects.get(pk=2)
        l.language = '<language2>'
        l.save()
        
        id = 'oai:%s:aaa.%d' % (TEST_DOMAIN, l.id)
        
        response = self.client.get(
            '/oai/?verb=GetRecord&metadataPrefix=oai_dc&identifier=%s' % id
        )
        self.assertNotContains(response, '&lt;')
        self.assertNotContains(response, '&gt;')

