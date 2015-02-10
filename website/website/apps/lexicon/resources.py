from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from website.apps.lexicon.models import Word, Lexicon



class LexiconResource(ModelResource):
    class Meta:
        queryset = Lexicon.objects.all()
        allowed_methods = ['get']
        excludes = []
        cache = SimpleCache(timeout=10)
        authorization = DjangoAuthorization()


class WordResource(ModelResource):
    class Meta:
        queryset = Word.objects.all()
        allowed_methods = ['get']
        excludes = ['comment', 'quality', ]
        cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'
