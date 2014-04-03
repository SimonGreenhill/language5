from django.http import Http404
from django.views.generic import DetailView
from website.apps.core.models import Location
from website.apps.lexicon.models import Word


class WordMap(DetailView):
    """Word Map Detail"""
    model = Word
    template_name = 'maps/word.html'
    
    def get_context_data(self, **kwargs):
        context = super(WordMap, self).get_context_data(**kwargs)
        context['records'] = []
        
        isos = set()
        entries = []
        # this is a bit horrific but minimises database queries.
        # 1. get entries and store in `entries`
        for e in kwargs['object'].lexicon_set.select_related('language').all():
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
        for e in entries:
            if e['isocode'] in locations:
                e['latitude'] = locations[e['isocode']].latitude
                e['longitude'] = locations[e['isocode']].longitude
                context['records'].append(e)
            else:
                # ignore entries without lats/longs
                continue
        
        return context
