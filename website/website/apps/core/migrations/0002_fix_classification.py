# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

from django.db import migrations


def fix_classification(apps, schema_editor):
    Language = apps.get_model("core", "Language")
    for lang in Language.objects.all():
        old = lang.classification
        lang.classification = lang.classification.replace(u"\u2019", "'")
        lang.classification = lang.classification.strip()
        if lang.classification != old:
            print('Changed Classification: %s' % lang)
            lang.save()
        

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_classification),
    ]
