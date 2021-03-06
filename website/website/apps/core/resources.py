from website.apps.api import UTF8ModelResource
from tastypie import fields
from tastypie.cache import SimpleCache
from website.apps.core.models import Language, Source

class LanguageResource(UTF8ModelResource):
    class Meta:
        queryset = Language.objects.all()
        allowed_methods = ['get']
        excludes = ['comment', 'bibtex', ]
        cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'
        default_format = 'application/json'
        limit = 100


class SourceResource(UTF8ModelResource):
    class Meta:
        queryset = Source.objects.all()
        allowed_methods = ['get']
        excludes = ['information', ]
        cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'
        default_format = 'application/json'
        limit = 100
