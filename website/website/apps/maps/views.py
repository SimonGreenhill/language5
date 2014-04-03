from django.http import Http404
from django.views.generic import DetailView
from website.apps.lexicon.models import Word


class WordMap(DetailView):
    """Word Map Detail"""
    model = Word
    template_name = 'maps/word.html'
    
    def get_context_data(self, **kwargs):
        context = super(WordMap, self).get_context_data(**kwargs)
        context['records'] = []
        
        # DUMMY 
        
        from random import gauss, sample
        from string import ascii_lowercase
        
        MAX = 100
        def get_rand_loc():
            return (gauss(-5.3, 4), gauss(141.0, 4))
        
        for i in range(0, MAX):
            lat, lon = get_rand_loc()
            wrd = "".join(sample(ascii_lowercase, 5))
            context['records'].append({'latitude': lat, 'longitude': lon, 'label': wrd})
        
        return context
