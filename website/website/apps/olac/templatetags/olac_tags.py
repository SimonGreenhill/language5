from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='oai_id')
def oai_id(obj):
    return 'oai:%s:%s.%d' % (settings.OLAC_SETTINGS['repositoryName'], obj.isocode, obj.id)
