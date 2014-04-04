from django.http import Http404
from django.views.generic import DetailView, ListView
from website.apps.core.models import Language, Location
from website.apps.lexicon.models import Word, CognateSet


def prepare_map_data(queryset):
    # this is a bit horrific but minimises database queries.
    # 1. get entries and store in `entries`
    isos = set()
    entries = []
    for e in queryset:
        if e.language.isocode and len(e.language.isocode) == 3:
            entries.append({
                'label': e.entry,
                'language': e.language,
                'isocode': e.language.isocode,
            })
            # save isocode
            isos.add(e.language.isocode)
    
    # 2. get locations for the isocodes we've seen and store in a lookup table
    locations = {}
    for loc in Location.objects.filter(isocode__in=list(isos)):
        locations[loc.isocode] = loc
    
    # 3. loop back through entries and plug in location data if we know it.
    final = []
    for e in entries:
        if e['isocode'] in locations:
            e['latitude'] = locations[e['isocode']].latitude
            e['longitude'] = locations[e['isocode']].longitude
            final.append(e)
        else:
            # ignore entries without lats/longs
            continue
    return final


class LanguageMap(ListView):
    """Word Map Detail"""
    model = Language
    template_name = 'maps/language.html'
    
    def get_context_data(self, **kwargs):
        context = super(LanguageMap, self).get_context_data(**kwargs)
        
        class dummy(object):  # quack!
            def __init__(self, lang):
                self.entry = lang
                self.language = lang
            
        context['records'] = prepare_map_data([
            dummy(_) for _ in Language.objects.all()
        ])
        return context


class WordMap(DetailView):
    """Word Map Detail"""
    model = Word
    template_name = 'maps/word.html'
    
    def get_context_data(self, **kwargs):
        context = super(WordMap, self).get_context_data(**kwargs)
        context['records'] = prepare_map_data(
            kwargs['object'].lexicon_set.select_related('language').all()
        )
        return context


class CognateSetMap(DetailView):
    """Cognate Set Detail"""
    model = CognateSet
    template_name = 'maps/cognateset.html'

    def get_context_data(self, **kwargs):
        context = super(CognateSetMap, self).get_context_data(**kwargs)
        context['records'] = prepare_map_data([
            _.lexicon for _ in 
            kwargs['object'].cognate_set.select_related('language').all()
        ])
        return context
