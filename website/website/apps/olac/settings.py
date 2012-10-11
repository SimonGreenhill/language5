import re
from django.conf import settings
# DEFAULT OLAC Settings
OLAC_SETTINGS = {
    'sitename': '',
    'sitedomain': '',
    'description': '',
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
