import re
from django.contrib.sites.models import Site
from django.conf import settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

website = Site.objects.get_current()

# OLAC Settings
OLAC_SETTINGS = {
    'oai_url': website.domain,
    'repositoryName': website.name,
    'description': website.name,
    'repositoryIdentifier': website.domain,
    'baseURL': 'http://%s/oai' % website.domain, # URL to OAI implementation
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
