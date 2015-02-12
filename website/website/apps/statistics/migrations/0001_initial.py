# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticalValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('label', models.CharField(max_length=128, db_index=True)),
                ('model', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=12)),
                ('field', models.CharField(max_length=32)),
                ('value', models.FloatField()),
            ],
            options={
                'ordering': ['date'],
                'db_table': 'statistics',
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
    ]
