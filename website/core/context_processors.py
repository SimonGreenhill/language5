from django.conf import settings
from django.contrib.sites.models import Site

def InjectSettings(context):
    """Injects various settings into the context"""
    return {
        'site': Site.objects.get_current()
    }
