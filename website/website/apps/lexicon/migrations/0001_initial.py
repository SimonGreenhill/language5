# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cognate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(help_text=b'Comment about this Cognate set', null=True, blank=True)),
                ('flag', models.CharField(default=0, help_text=b'The quality of this cognate.', max_length=1, choices=[(b'0', b'Unassessed'), (b'1', b'Published'), (b'2', b'Accepted'), (b'9', b'Problematic')])),
            ],
            options={
                'db_table': 'cognates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CognateSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('protoform', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('gloss', models.CharField(max_length=128, null=True, blank=True)),
                ('comment', models.TextField(help_text=b'Comment about this cognate set', null=True, blank=True)),
                ('quality', models.CharField(default='0', help_text=b'The quality of this cognate set.', max_length=1, choices=[(b'0', b'Unassessed'), (b'1', b'Published'), (b'2', b'Accepted'), (b'9', b'Problematic')])),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cognatesets',
                'verbose_name_plural': 'Cognate Sets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Correspondence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('rule', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'correspondences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CorrespondenceSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(help_text=b'Notes', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ManyToManyField(to='core.Language', through='lexicon.Correspondence')),
                ('source', models.ForeignKey(blank=True, to='core.Source', null=True)),
            ],
            options={
                'db_table': 'corrsets',
                'verbose_name_plural': 'Correspondence Sets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lexicon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('entry', models.CharField(help_text=b'Entry from source', max_length=128, db_index=True)),
                ('phon_entry', models.CharField(help_text=b'Entry in Phonological format (in known)', max_length=128, null=True, blank=True)),
                ('source_gloss', models.CharField(help_text=b'Gloss in original source if it is semantically different', max_length=128, null=True, blank=True)),
                ('annotation', models.TextField(help_text=b'Annotation for this item', null=True, blank=True)),
                ('loan', models.BooleanField(default=False, help_text=b'Is a loan word?', db_index=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='core.Language')),
                ('loan_source', models.ForeignKey(related_name=b'loan_source_set', blank=True, to='core.Language', help_text=b'Loanword Source (if known)', null=True)),
                ('source', models.ForeignKey(to='core.Source')),
            ],
            options={
                'ordering': ['entry'],
                'db_table': 'lexicon',
                'verbose_name_plural': 'Lexical Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('word', models.CharField(help_text=b'Word in English', unique=True, max_length=64, db_index=True)),
                ('slug', models.SlugField(help_text=b'`Slug` for word (for use in URLS)', unique=True, max_length=64)),
                ('full', models.TextField(help_text=b'Full word details/gloss.', null=True, blank=True)),
                ('comment', models.TextField(help_text=b'PUBLIC comment on this word', null=True, blank=True)),
                ('quality', models.CharField(default='0', help_text=b'The quality of this word.', max_length=1, choices=[(b'0', b'Unassessed'), (b'1', b'Extremely stable or reliable'), (b'8', b'Open to serious objections as a test item'), (b'9', b'Highly unsuitable')])),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['word'],
                'db_table': 'words',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordSubset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('subset', models.CharField(help_text=b'Subset Label', unique=True, max_length=64, db_index=True)),
                ('slug', models.SlugField(help_text=b'`Slug` for subset (for use in URLS)', unique=True, max_length=64)),
                ('description', models.TextField(help_text=b'Details of subset.', null=True, blank=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('words', models.ManyToManyField(to='lexicon.Word', null=True, blank=True)),
            ],
            options={
                'ordering': ['slug'],
                'db_table': 'wordsubsets',
                'verbose_name_plural': 'Word Subsets',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lexicon',
            name='word',
            field=models.ForeignKey(to='lexicon.Word'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='correspondence',
            name='corrset',
            field=models.ForeignKey(to='lexicon.CorrespondenceSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='correspondence',
            name='editor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='correspondence',
            name='language',
            field=models.ForeignKey(to='core.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cognateset',
            name='lexicon',
            field=models.ManyToManyField(to='lexicon.Lexicon', through='lexicon.Cognate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cognateset',
            name='source',
            field=models.ForeignKey(blank=True, to='core.Source', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cognate',
            name='cognateset',
            field=models.ForeignKey(to='lexicon.CognateSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cognate',
            name='editor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cognate',
            name='lexicon',
            field=models.ForeignKey(to='lexicon.Lexicon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cognate',
            name='source',
            field=models.ForeignKey(blank=True, to='core.Source', null=True),
            preserve_default=True,
        ),
    ]
