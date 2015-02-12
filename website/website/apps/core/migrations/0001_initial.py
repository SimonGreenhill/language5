# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternateName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(help_text=b'Alternate Name for this language', unique=True, max_length=64, db_index=True)),
                ('slug', models.SlugField(help_text=b'`Slug` for language (for use in URLS)', unique=True, max_length=64)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'altnames',
                'verbose_name_plural': 'Alternate Language Names',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('details', models.CharField(help_text=b'Extra details e.g. page number', max_length=b'32', null=True, blank=True)),
                ('file', models.FileField(help_text=b'The Resource File (PDF)', null=True, upload_to=b'data/%Y-%m/', blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'attachments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('family', models.CharField(help_text=b'Language Family', unique=True, max_length=64, db_index=True)),
                ('slug', models.SlugField(help_text=b'`Slug` for language family (for use in URLS)', unique=True, max_length=64)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['family'],
                'db_table': 'families',
                'verbose_name_plural': 'families',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(help_text=b'Language Name', max_length=64, db_index=True)),
                ('dialect', models.CharField(help_text=b'Dialect', max_length=64, null=True, db_index=True, blank=True)),
                ('slug', models.SlugField(help_text=b'`Slug` for language (for use in URLS)', unique=True, max_length=64)),
                ('isocode', models.CharField(help_text=b'3 character ISO-639-3 Code.', max_length=3, null=True, db_index=True, blank=True)),
                ('classification', models.TextField(help_text=b'Classification String', null=True, blank=True)),
                ('information', models.TextField(help_text=b'Information about language', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('family', models.ManyToManyField(to='core.Family', blank=True)),
            ],
            options={
                'ordering': ['language', 'dialect'],
                'db_table': 'languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField(help_text=b'URL to link')),
                ('description', models.TextField(help_text=b'Language Description')),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='core.Language')),
            ],
            options={
                'db_table': 'links',
                'verbose_name_plural': 'Resource Links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('isocode', models.CharField(max_length=3, db_index=True)),
                ('longitude', models.FloatField(help_text=b'Longitude')),
                ('latitude', models.FloatField(help_text=b'Latitiude')),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'locations',
                'verbose_name_plural': 'Geographical Locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(help_text=b'Note')),
                ('location', models.CharField(help_text=b'Location (e.g. p12)', max_length=50, null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='core.Language')),
            ],
            options={
                'db_table': 'notes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PopulationSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('populationsize', models.IntegerField()),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='core.Language')),
            ],
            options={
                'db_table': 'popsize',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('year', models.CharField(help_text=b'Year published', max_length=12, null=True, db_index=True, blank=True)),
                ('author', models.CharField(help_text=b'Short Author list e.g. (Smith et al.)', max_length=255, db_index=True)),
                ('slug', models.SlugField(help_text=b'`Slug` for author i.e. author-year (for use in URLS)', unique=True, max_length=64)),
                ('reference', models.TextField(help_text=b'Reference for Source', null=True, blank=True)),
                ('bibtex', models.TextField(help_text=b'BibTeX entry', null=True, blank=True)),
                ('comment', models.TextField(help_text=b'Private comment on source', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['author', 'year'],
                'db_table': 'sources',
            },
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name='source',
            index_together=set([('author', 'year')]),
        ),
        migrations.AddField(
            model_name='populationsize',
            name='source',
            field=models.ForeignKey(to='core.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='source',
            field=models.ForeignKey(to='core.Source'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together=set([('language', 'link')]),
        ),
        migrations.AlterUniqueTogether(
            name='language',
            unique_together=set([('isocode', 'language', 'dialect')]),
        ),
        migrations.AlterIndexTogether(
            name='language',
            index_together=set([('language', 'dialect')]),
        ),
        migrations.AddField(
            model_name='attachment',
            name='language',
            field=models.ForeignKey(to='core.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='source',
            field=models.ForeignKey(to='core.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alternatename',
            name='language',
            field=models.ForeignKey(to='core.Language'),
            preserve_default=True,
        ),
    ]
