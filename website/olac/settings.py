import re
from django.conf import settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# OLAC Settings
OLAC_SETTINGS = {
    'oai_url': settings.DOMAIN_NAME, # Website URL
    'repositoryName': settings.PROJECT_NAME,
    'description': 'Generic OLAC repository',
    'repositoryIdentifier': settings.DOMAIN_NAME,
    'baseURL': 'http://%s/oai' % settings.DOMAIN_NAME, # URL to OAI implementation
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
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + ('olac.content_processors.',)