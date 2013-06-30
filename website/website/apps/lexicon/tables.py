import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.lexicon.models import Word, WordSubset, Lexicon


class WordIndexTable(DataTable):
    """Word Listing"""
    id = tables.LinkColumn('word-detail', args=[A('slug')], order_by=("id",))
    fullword = tables.LinkColumn('word-detail', args=[A('slug')], order_by=("word", "full"))
    count = tables.Column()
    
    class Meta(DataTable.Meta):
        model = Word
        order_by = 'fullword' # default sorting
        sequence = ('id', 'fullword', 'count')
        exclude = ('editor', 'word', 'full', 'added', 'slug', 'quality', 'comment')
    Meta.attrs['summary'] = 'Table of Words'


class WordLexiconTable(DataTable):
    """Lexicon table for Word pages"""
    id = tables.Column()
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    classification = tables.Column()
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by_field = 'word' # default sorting
        sequence = ('id', 'language', 'entry', 'annotation', 'loan',  'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'word')
    Meta.attrs['summary'] = 'Table of Lexicon'


class LanguageLexiconTable(DataTable):
    """Lexicon table for Language pages"""
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))

    class Meta(DataTable.Meta):
        model = Lexicon
        order_by_field = 'word' # default sorting
        sequence = ('word', 'entry', 'annotation', 'loan', 'source')
        exclude = ('id', 'editor', 'added', 'slug', 'phon_entry', 'loan_source', 'language')
    Meta.attrs['summary'] = 'Table of Lexicon'


class SourceLexiconTable(DataTable):
    """Lexicon table for Source pages"""
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by_field = 'language' # default sorting
        sequence = ('language', 'word', 'entry', 'annotation', 'loan')
        exclude = ('id', 'editor', 'added', 'slug', 'phon_entry', 'loan_source', 'source')
    Meta.attrs['summary'] = 'Table of Lexicon'

        