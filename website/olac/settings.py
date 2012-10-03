import re
from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# OLAC Settings
OLAC_SETTINGS = {
    'oai_url': settings.WEBSITE_DOMAIN,
    'repositoryName': settings.WEBSITE_NAME,
    'description': settings.WEBSITE_NAME,
    'repositoryIdentifier': settings.WEBSITE_DOMAIN,
    'baseURL': 'http://%s/oai' % settings.WEBSITE_DOMAIN, # URL to OAI implementation
    'adminEmail': settings.ADMINS, 
    'admins': settings.ADMINS,
    'deletedRecord': 'no', # deletedRecord policy
    'protocolVersion': '2.0', # the version of the OAI-PMH supported by the repository;
    '_identifier': re.compile(r"""oai:.*?:(\w{3})\.(\d+)"""),
    'depositor': settings.ADMINS,
    'institution': 'NA',
    'institutionURL': 'http://example.com',
    'shortLocation': 'Auckland, New Zealand',
}
