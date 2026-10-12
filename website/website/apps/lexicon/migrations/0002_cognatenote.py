# flake8: noqa

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lexicon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CognateNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(help_text='Note')),
                ('cognateset', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='lexicon.CognateSet', null=True)),
                ('editor', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='lexicon.Word', null=True)),
            ],
            options={
                'db_table': 'cognacy_notes',
            },
            bases=(models.Model,),
        ),
    ]
