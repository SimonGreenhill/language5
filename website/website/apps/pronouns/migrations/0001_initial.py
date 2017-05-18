# -*- coding: utf-8 -*-
# flake8: noqa
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
                ('comment', models.TextField(help_text='Comment on this paradigm', null=True, blank=True)),
                ('analect', models.CharField(blank=True, max_length=1, null=True, help_text='System Type', choices=[('F', 'Free'), ('', 'Bound')])),
                ('label', models.CharField(help_text='Short label', max_length=32, null=True, blank=True)),
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
                ('comment', models.TextField(help_text='Comment on this paradigm', null=True, blank=True)),
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
                ('alignment', models.CharField(help_text='Alignment', max_length=1, choices=[('A', 'A'), ('S', 'S'), ('O', 'O'), ('P', 'Possessive')])),
                ('person', models.CharField(help_text='Person', max_length=2, choices=[('1', '1st (excl) Person'), ('12', '1st (incl) Person'), ('2', '2nd Person'), ('3', '3rd Person')])),
                ('number', models.CharField(help_text='Number', max_length=2, choices=[('sg', 'Singular'), ('du', 'Dual'), ('pl', 'Plural')])),
                ('gender', models.CharField(blank=True, max_length=1, null=True, help_text='Gender', choices=[('M', 'Gender 1'), ('F', 'Feminine'), ('N', 'Gender 2')])),
                ('active', models.BooleanField(default=True, help_text='Show on website?', db_index=True)),
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
                ('relationship', models.CharField(default=None, choices=[('TD', 'Totally Distinct'), ('FO', 'Formal Overlap'), ('FI', 'Formal Increment'), ('TS', 'Total Syncretism')], max_length=2, blank=True, help_text='Relationship', null=True)),
                ('comment', models.TextField(help_text='Comment on this relationship', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('paradigm', models.ForeignKey(to='pronouns.Paradigm')),
                ('pronoun1', models.ForeignKey(related_name='pronoun1', to='pronouns.Pronoun')),
                ('pronoun2', models.ForeignKey(related_name='pronoun2', to='pronouns.Pronoun')),
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
