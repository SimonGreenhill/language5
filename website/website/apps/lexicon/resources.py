from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache
from website.apps.lexicon.models import Word


class WordResource(ModelResource):
    class Meta:
        queryset = Word.objects.all()
        allowed_methods = ['get']
        excludes = ['comment', 'quality', ]
        cache = SimpleCache(timeout=10)

