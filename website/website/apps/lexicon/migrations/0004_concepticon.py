# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 13:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lexicon', '0003_auto_20160323_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concepticon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('gloss', models.CharField(db_index=True, help_text='Concepticon Gloss', max_length=64, unique=True)),
                ('semanticfield', models.CharField(db_index=True, help_text='Semantic Field', max_length=32, unique=True)),
                ('definition', models.TextField(blank=True, help_text='Definition', null=True)),
                ('ontologicalcategory', models.CharField(db_index=True, help_text='Ontological Category', max_length=32, unique=True)),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'concepticon',
            },
        ),
        migrations.AddField(
            model_name='word',
            name='concepticon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lexicon.Concepticon'),
        ),
    ]
