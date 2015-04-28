# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='source',
            field=models.ForeignKey(blank=True, to='core.Source', null=True),
            preserve_default=True,
        ),
    ]
