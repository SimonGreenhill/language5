from tastypie import fields
from website.apps.api import UTF8ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from website.apps.lexicon.models import Word, Lexicon
from website.apps.core.resources import LanguageResource, SourceResource


class WordResource(UTF8ModelResource):
    
    concepticon_id = fields.CharField(attribute='concepticon_id', null=True, blank=True)
    
    class Meta:
        queryset = Word.objects.all().select_related('concepticon')
        allowed_methods = ['get']
        excludes = ['comment', 'quality', 'added', 'full']
        cache = SimpleCache(timeout=10)
        detail_uri_name = 'slug'
        default_format = 'application/json'
        limit = 100


class LexiconResource(UTF8ModelResource):
    language = fields.CharField(attribute='language')
    #language_uri = fields.ForeignKey(LanguageResource, 'language', full=False)
    source = fields.CharField(attribute='source__slug')
    #source_uri = fields.ForeignKey(SourceResource, 'source', full=False)
    word = fields.CharField(attribute='word__slug')
    #word_uri = fields.ForeignKey(WordResource, 'word', full=False)
    
    class Meta:
        queryset = Lexicon.objects.all()
        allowed_methods = ['get']
        excludes = ['phon_entry', ]
        cache = SimpleCache(timeout=10)
        default_format = 'application/json'
        limit = 100
        filtering = {
            "language": ('exact', ),
            "source": ('exact', ),
            "word": ('exact', ),
        }
        