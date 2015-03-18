# -*- coding: utf-8 -*-
import reversion
from django.db.models import Count
from optparse import make_option
from django.core.management.base import BaseCommand

from website.apps.core.models import Language, Source
from website.apps.lexicon.models import Word, Lexicon, Cognate, CognateSet


def repr_cog(cog_id, source_id=None):
    if source_id:
        return "%03d.%05d" % (source_id, cog_id)
    else:
        return "{0:x}".format(cog_id)


class Command(BaseCommand):
    args = 'write_table'
    help = 'writes a table of data'
    output_transaction = True
    option_list = BaseCommand.option_list + (
        make_option('--language',
            action='store',
            dest='language',
            default=False,
            help='Filter by language slug'),
        make_option('--word',
            action='store',
            dest='word',
            default=False,
            help='Filter by word slug'),
        make_option('--source',
            action='store',
            dest='source',
            default=False,
            help='Filter by source slug'),
        make_option('--clade',
            action='store',
            dest='clade',
            default=False,
            help='Filter by clade'),
    )
    
    def get_entries(self, language=None, word=None, source=None, clade=None):
        lexica = Lexicon.objects.all().select_related()
        lexica = lexica.order_by('word').order_by('language')
    
        # filters
        if language:
            lexica = lexica.filter(language=Language.objects.get(slug=language))
        if word:
            lexica = lexica.filter(word=Word.objects.get(slug=word))
        if source:
            lexica = lexica.filter(source=Source.objects.get(slug=source))
        if clade:
            lexica = lexica.filter(language__in=
                Language.objects.filter(classification__startswith=clade)
            )
        return lexica
    
    def handle(self, *args, **options):
        lexica = self.get_entries(
            language=options.get('language', None),
            word = options.get('word', None),
            source = options.get('source', None),
            clade = options.get('clade', None)
        )
        
        for lex in lexica:
            cogs = ",".join([repr_cog(_.id) for _ in lex.cognateset_set.all()])
            print(u"\t".join([
                "%s" % lex.id,
                lex.language.slug,
                lex.word.slug,
                lex.source.slug,
                lex.entry.replace('\t', ''),
                cogs
            ]))
