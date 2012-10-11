from django.contrib.sites.models import Site
from django.conf import settings

def InjectOLACSettings(context):
    """Injects various settings into the context"""
    
    # if we have a non-empty sitename and domain in OLAC_SETTINGS
    # ... then try and load from site.
    if not settings.OLAC_SETTINGS['sitename'] and not settings.OLAC_SETTINGS['sitedomain']:
        site = Site.objects.get_current()
        settings.OLAC_SETTINGS['sitename'] = site.name
        settings.OLAC_SETTINGS['sitedomain'] = site.domain
    return {'OLAC': settings.OLAC_SETTINGS}
