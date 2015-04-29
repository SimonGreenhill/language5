# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lexicon', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paradigm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(help_text=b'Comment on this paradigm', null=True, blank=True)),
                ('analect', models.CharField(blank=True, max_length=1, null=True, help_text=b'System Type', choices=[(b'F', b'Free'), (b'B', b'Bound')])),
                ('label', models.CharField(help_text=b'Short label', max_length=32, null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='core.Language')),
                ('source', models.ForeignKey(to='core.Source')),
            ],
            options={
                'db_table': 'paradigms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pronoun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(help_text=b'Comment on this paradigm', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('entries', models.ManyToManyField(to='lexicon.Lexicon', null=True, blank=True)),
                ('paradigm', models.ForeignKey(to='pronouns.Paradigm')),
            ],
            options={
                'db_table': 'pronouns',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PronounType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('alignment', models.CharField(help_text=b'Alignment', max_length=1, choices=[(b'A', b'A'), (b'S', b'S'), (b'O', b'O'), (b'P', b'Possessive')])),
                ('person', models.CharField(help_text=b'Person', max_length=2, choices=[(b'1', b'1st (excl) Person'), (b'12', b'1st (incl) Person'), (b'2', b'2nd Person'), (b'3', b'3rd Person')])),
                ('number', models.CharField(help_text=b'Number', max_length=2, choices=[(b'sg', b'Singular'), (b'du', b'Dual'), (b'pl', b'Plural')])),
                ('gender', models.CharField(blank=True, max_length=1, null=True, help_text=b'Gender', choices=[(b'M', b'Gender 1'), (b'F', b'Feminine'), (b'N', b'Gender 2')])),
                ('active', models.BooleanField(default=True, help_text=b'Show on website?', db_index=True)),
                ('sequence', models.PositiveSmallIntegerField(unique=True, db_index=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='lexicon.Word')),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'added',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('relationship', models.CharField(default=None, choices=[(b'TD', b'Totally Distinct'), (b'FO', b'Formal Overlap'), (b'FI', b'Formal Increment'), (b'TS', b'Total Syncretism')], max_length=2, blank=True, help_text=b'Relationship', null=True)),
                ('comment', models.TextField(help_text=b'Comment on this relationship', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('paradigm', models.ForeignKey(to='pronouns.Paradigm')),
                ('pronoun1', models.ForeignKey(related_name=b'pronoun1', to='pronouns.Pronoun')),
                ('pronoun2', models.ForeignKey(related_name=b'pronoun2', to='pronouns.Pronoun')),
            ],
            options={
                'db_table': 'pronoun_relationships',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('rule', models.CharField(max_length=64)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('paradigm', models.ForeignKey(to='pronouns.Paradigm')),
                ('relationships', models.ManyToManyField(to='pronouns.Relationship', null=True, blank=True)),
            ],
            options={
                'db_table': 'pronoun_rules',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pronoun',
            name='pronountype',
            field=models.ForeignKey(to='pronouns.PronounType'),
            preserve_default=True,
        ),
    ]
