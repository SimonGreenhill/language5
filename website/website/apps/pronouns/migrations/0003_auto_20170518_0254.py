# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-18 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronouns', '0002_auto_20160323_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paradigm',
            name='analect',
            field=models.CharField(blank=True, choices=[('F', 'Free'), ('B', 'Bound')], help_text='System Type', max_length=1, null=True),
        ),
    ]
