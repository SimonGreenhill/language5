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
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(help_text='Name of Task', max_length=255, db_index=True)),
                ('description', models.TextField(help_text='Task Description', null=True, blank=True)),
                ('records', models.IntegerField(default=20, null=True, blank=True)),
                ('view', models.CharField(default='GenericView', help_text='Data entry view to Use', max_length=256, choices=[('GenericView', 'Generic data entry task'), ('WordlistView', 'Data entry task using a wordlist')])),
                ('image', models.ImageField(help_text='The Page Image', null=True, upload_to='data/%Y-%m/', blank=True)),
                ('file', models.FileField(help_text='The Resource File (PDF)', null=True, upload_to='data/%Y-%m/', blank=True)),
                ('completable', models.BooleanField(default=True, help_text='Is task completable or not?', db_index=True)),
                ('done', models.BooleanField(default=False, help_text='Data has been entered', db_index=True)),
                ('checkpoint', models.TextField(help_text='Saved Checkpoint Data', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(blank=True, to='core.Language', null=True)),
                ('lexicon', models.ManyToManyField(help_text='Saved Lexical Items', to='lexicon.Lexicon', null=True, blank=True)),
                ('source', models.ForeignKey(to='core.Source')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'tasks',
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page', models.CharField(max_length=64)),
                ('message', models.CharField(max_length=255)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(blank=True, to='entry.Task', null=True)),
            ],
            options={
                'ordering': ['time'],
                'db_table': 'tasklog',
                'get_latest_by': 'time',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wordlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(help_text='Name of Wordlist', unique=True, max_length=255, db_index=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'task_wordlists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordlistMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(db_index=True)),
                ('word', models.ForeignKey(to='lexicon.Word')),
                ('wordlist', models.ForeignKey(to='entry.Wordlist')),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'task_wordlists_members',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='wordlist',
            name='words',
            field=models.ManyToManyField(to='lexicon.Word', through='entry.WordlistMember'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='wordlist',
            field=models.ForeignKey(blank=True, to='entry.Wordlist', null=True),
            preserve_default=True,
        ),
    ]
