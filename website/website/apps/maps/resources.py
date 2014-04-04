from django.core.urlresolvers import reverse

from tastypie import fields
from tastypie.resources import Resource
from tastypie.cache import SimpleCache

from website.apps.core.models import Language, Location


class MapObj(object):
    def __init__(self, adict):
        self.isocode = None
        self.language = None
        self.label = None
        self.longitude = None
        self.latitude = None
        self.url = None
        
        for k, v in adict.items():
            setattr(self, k, v)
        
        

def prepare_map_data(records):
    # this is a bit horrific but minimises database queries.
    # 1. get entries and store in `entries`
    isos = set()
    entries = []
    for r in records:
        if r.get('isocode', None) and len(r.get('isocode', "")) == 3:
            obj = MapObj(r)
            entries.append(obj)
            isos.add(obj.isocode) # save isocode
    
    # 2. get locations for the isocodes we've seen and store in a lookup table
    locations = {}
    for loc in Location.objects.filter(isocode__in=list(isos)):
        locations[loc.isocode] = loc
    
    # 3. loop back through entries and plug in location data if we know it.
    records = []
    for e in entries:
        # ignore entries without lats/longs
        if e.isocode in locations:
            e.latitude = locations[e.isocode].latitude
            e.longitude = locations[e.isocode].longitude
            records.append(e)
    return records
    


class LanguageMapResource(Resource):
    label = fields.CharField(attribute='label')
    language = fields.CharField(attribute='language')
    isocode = fields.CharField(attribute='isocode')
    latitude = fields.FloatField(attribute='latitude')
    longitude = fields.FloatField(attribute='longitude')
    url = fields.CharField(attribute='url')
    
    class Meta:
        limit = 0 # show all
        include_resource_uri = False
        allowed_methods = ['get']
        cache = SimpleCache(timeout=10)
    
    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)
        
    def get_object_list(self, request):
        results = []
        for L in Language.objects.all():
            results.append({
                'isocode': L.isocode,
                'language': L.language,
                'label': L.language,
                'url': reverse('language-detail', kwargs={'language': L.slug}),
            })
        return prepare_map_data(results)

