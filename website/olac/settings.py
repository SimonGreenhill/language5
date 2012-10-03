import re
from django.contrib.sites.models import Site
from django.conf import settings

# handle defaults gracefully.
# settings.ADMIN is always set in default settings.py
# We want to look for DOMAIN and NAME in a Site object.

try:
    website = Site.objects.get_current()
    domain = website.domain
    sitename   = website.name
except:
    domain = sitename = 'example.com'
    

# OLAC Settings
OLAC_SETTINGS = {
    'oai_url': domain,
    'repositoryName': sitename,
    'description': sitename,
    'repositoryIdentifier': domain,
    'baseURL': 'http://%s/oai' % domain, # URL to OAI implementation
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
