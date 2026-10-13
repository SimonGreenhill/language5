# Sync the watson search index: drop entries for deleted objects, index objects that have none.
# Replaces `manage.py buildwatson`, whose NOT IN cleanup is quadratic on PostgreSQL 14.
# Run: manage.py shell < ../deploy/watson_sync.py   (safe to re-run)
from django.contrib.contenttypes.models import ContentType
from watson import search as watson
from watson.models import SearchEntry

engine = watson.default_search_engine
for model in watson.get_registered_models():
    entries = SearchEntry.objects.filter(engine_slug='default', content_type=ContentType.objects.get_for_model(model))
    indexed = dict(entries.values_list('object_id_int', 'id'))
    existing = set(model.objects.values_list('pk', flat=True))
    stale = [indexed[pk] for pk in indexed.keys() - existing]
    missing = existing - indexed.keys()
    for i in range(0, len(stale), 1000):
        SearchEntry.objects.filter(id__in=stale[i:i + 1000]).delete()
    for obj in model.objects.filter(pk__in=missing):
        engine.update_obj_index(obj)
    print(f'{model._meta.label}: {len(stale)} stale removed, {len(missing)} missing added')
