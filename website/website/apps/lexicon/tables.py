import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from website.apps.core.tables import DataTable

from website.apps.lexicon.models import Word, WordSubset, Lexicon
from website.apps.lexicon.models import CognateSet, Cognate


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
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'word' # default sorting
        sequence = ('id', 'language', 'entry', 'annotation', 'loan',  'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'word',)
    Meta.attrs['summary'] = 'Table of Lexicon'


class LanguageLexiconTable(DataTable):
    """Lexicon table for Language pages"""
    id = tables.Column()
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))

    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'word' # default sorting
        sequence = ('id', 'word', 'entry', 'annotation', 'loan', 'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'language',)
    Meta.attrs['summary'] = 'Table of Lexicon'


class SourceLexiconTable(DataTable):
    """Lexicon table for Source pages"""
    id = tables.Column()
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'language' # default sorting
        sequence = ('id', 'language', 'word', 'entry', 'annotation', 'loan')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'source',)
    Meta.attrs['summary'] = 'Table of Lexicon'


class CognateSetDetailTable(DataTable):
    """Cognate set detail table"""
    id = tables.Column()
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'language' # default sorting
        sequence = ('id', 'language', 'word', 'entry', 'annotation', 'loan')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'source',)
    Meta.attrs['summary'] = 'Table of Lexicon'


class CognateSetIndexTable(DataTable):
    """Table of cognate sets"""
    id = tables.LinkColumn('cognateset-detail', args=[A('id')])
    protoform = tables.LinkColumn('cognateset-detail', args=[A('id')])
    gloss = tables.LinkColumn('cognateset-detail', args=[A('id')])
    count = tables.Column()
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    
    class Meta(DataTable.Meta):
        model = CognateSet
        order_by = 'id' # default sorting
        sequence = ('id', 'protoform', 'gloss', 'count', 'source', )
        exclude = ('editor', 'added', 'comment', 'lexicon', 'quality')
    Meta.attrs['summary'] = 'Table of Cognate Sets'



# Tables with Edit links
# it would be nice if these could just inherit from their parents (e.g. WordLexiconEditTable 
# is subclass of WordLexiconTable) but then django-tables has problems - i.e. column types
# aren't inherited (esp. LinkColumn's get converted to Column's etc)
class WordLexiconEditTable(WordLexiconTable):
    id = tables.LinkColumn('lexicon-edit', args=[A('id')])
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    def render_language(self, record):
        col = tables.LinkColumn('language-detail', args=[record.language.slug])
        return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(WordLexiconTable.Meta):
        model = Lexicon
        order_by = 'word' # default sorting
        sequence = ('id', 'language', 'entry', 'annotation', 'loan',  'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'word',)
    Meta.attrs['summary'] = 'Table of Lexicon'


class LanguageLexiconEditTable(LanguageLexiconTable):
    id = tables.LinkColumn('lexicon-edit', args=[A('id')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    class Meta(LanguageLexiconTable.Meta):
        model = Lexicon
        order_by = 'word' # default sorting
        sequence = ('id', 'word', 'entry', 'annotation', 'loan', 'source')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'language',)
    Meta.attrs['summary'] = 'Table of Lexicon'


class SourceLexiconEditTable(SourceLexiconTable):
    id = tables.LinkColumn('lexicon-edit', args=[A('id')])
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    source_gloss = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    class Meta(SourceLexiconTable.Meta):
        model = Lexicon
        order_by = 'language' # default sorting
        sequence = ('id', 'language', 'word', 'entry', 'annotation', 'loan')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source', 'source',)
    Meta.attrs['summary'] = 'Table of Lexicon'
        
