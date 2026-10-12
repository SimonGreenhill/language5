import base64
import json
import pickle

from django.db import migrations
from django.http import QueryDict


def pickle_to_json(content):
    q = pickle.loads(base64.b64decode(content))
    return json.dumps(dict(q.lists()))


def json_to_pickle(content):
    q = QueryDict(mutable=True)
    for key, values in json.loads(content).items():
        q.setlist(key, values)
    return base64.b64encode(pickle.dumps(q, protocol=2)).decode('ascii')


def convert(apps, func, legacy):
    Task = apps.get_model('entry', 'Task')
    for task in Task.objects.exclude(checkpoint__isnull=True).exclude(checkpoint='').only('id', 'checkpoint'):
        if task.checkpoint.startswith('{') == legacy:  # already in the target format
            continue
        task.checkpoint = func(task.checkpoint)
        task.save(update_fields=['checkpoint'])


class Migration(migrations.Migration):
    """Checkpoints were pickled QueryDicts; store them as JSON so nothing is unpickled at runtime."""

    dependencies = [
        ('entry', '0004_image_filefield'),
    ]

    operations = [
        migrations.RunPython(
            lambda apps, schema_editor: convert(apps, pickle_to_json, legacy=True),
            lambda apps, schema_editor: convert(apps, json_to_pickle, legacy=False),
        ),
    ]
