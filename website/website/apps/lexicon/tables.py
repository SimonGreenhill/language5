import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.lexicon.models import Word, WordSubset, Lexicon


class WordIndexTable(DataTable):
    """Word Listing"""
    id = tables.LinkColumn('word-detail', args=[A('slug')])
    word = tables.LinkColumn('word-detail', args=[A('slug')])
    count = tables.Column()
    
    class Meta(DataTable.Meta):
        model = Word
        order_by_field = 'word' # default sorting
        sequence = ('id', 'word', 'count')
        exclude = ('editor', 'added', 'slug', 'full')
    Meta.attrs['summary'] = 'Table of Words'


class WordLexiconTable(DataTable):
    """Lexicon table for Word pages"""
    #id = tables.Column()
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('', 'x'))
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by_field = 'language' # default sorting
        sequence = ('id', 'language', 'entry', 'annotation', 'loan',  'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'word')
    Meta.attrs['summary'] = 'Table of Lexicon'


class LanguageLexiconTable(DataTable):
    """Lexicon table for Language pages"""
    id = tables.Column()
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('', 'x'))

    class Meta(DataTable.Meta):
        model = Lexicon
        order_by_field = 'word' # default sorting
        sequence = ('id', 'word', 'entry', 'annotation', 'loan', 'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'language')
    Meta.attrs['summary'] = 'Table of Lexicon'


class SourceLexiconTable(DataTable):
    """Lexicon table for Source pages"""
    id = tables.Column()
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('', 'x'))

    class Meta(DataTable.Meta):
        model = Lexicon
        order_by_field = 'language' # default sorting
        sequence = ('id', 'language', 'word', 'entry', 'annotation', 'loan')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'source')
    Meta.attrs['summary'] = 'Table of Lexicon'

        