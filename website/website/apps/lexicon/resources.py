from tastypie import fields
from website.apps.api import UT8ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from website.apps.lexicon.models import Word, Lexicon
from website.apps.core.resources import LanguageResource, SourceResource


class WordResource(UT8ModelResource):
    
    def determine_format(self, request):
        return 'application/json'
    
    class Meta:
        queryset = Word.objects.all()
        allowed_methods = ['get']
        excludes = ['comment', 'quality', ]
        cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'


class LexiconResource(UT8ModelResource):
    
    language = fields.ForeignKey(LanguageResource, 'language', full=False)
    source = fields.ForeignKey(SourceResource, 'source', full=False)
    word = fields.ForeignKey(WordResource, 'word', full=False)
    
    def determine_format(self, request):
        return 'application/json'
    
    class Meta:
        queryset = Lexicon.objects.all()
        allowed_methods = ['get']
        excludes = []
        cache = SimpleCache(timeout=10)
        authorization = DjangoAuthorization()

