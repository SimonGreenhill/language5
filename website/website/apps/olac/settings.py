import re
from django.contrib.sites.models import Site
from django.conf import settings

# handle defaults gracefully.
# settings.ADMIN is always set in default settings.py
# We want to look for DOMAIN and NAME in a Site object.

site = Site.objects.get_current()

# DEFAULT OLAC Settings
OLAC_SETTINGS = {
    'oai_url': site.domain,
    'repositoryName': site.name,
    'description': site.name,
    'repositoryIdentifier': site.domain,
    'baseURL': 'http://%s/oai' % site.domain, # URL to OAI implementation
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
