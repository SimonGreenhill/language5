import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from website.apps.core.tables import DataTable
from website.apps.lexicon.models import Lexicon
from website.apps.entry.models import Task

class TaskIndexTable(DataTable):
    """Task Listing"""
    id = tables.LinkColumn('entry:detail', args=[A('id')])
    name = tables.LinkColumn('entry:detail', args=[A('id')])
    description = tables.LinkColumn('entry:detail', args=[A('id')])
    
    class Meta(DataTable.Meta):
        model = Task
        order_by = 'id' # default sorting
        sequence = ('id', 'name', 'source', 'language', 'description', 'records')
        exclude = ('editor', 'view', 'image', 'done', 'checkpoint', 'added', 'file', 'completable')
    Meta.attrs['summary'] = 'Table of Tasks'
    

class TaskLexiconTable(DataTable):
    id = tables.LinkColumn('lexicon-edit', args=[A('id')])
    language = tables.LinkColumn('language-detail', args=[A('language.slug')])
    source = tables.LinkColumn('source-detail', args=[A('source.slug')])
    word = tables.LinkColumn('word-detail', args=[A('word.slug')])
    entry = tables.Column()
    annotation = tables.Column()
    loan = tables.BooleanColumn(null=False, yesno=('x', ''))
    
    # def render_language(self, record):
    #     col = tables.LinkColumn('language-detail', args=[record.language.slug])
    #     return col.render(value=unicode(record.language), record=unicode(record.language), bound_column=None)
    
    class Meta(DataTable.Meta):
        model = Lexicon
        order_by = 'word' # default sorting
        sequence = ('id', 'language', 'word', 'source', 'entry', 'annotation', 'loan')
        exclude = ('editor', 'added', 'slug', 'phon_entry', 'loan_source',)
    Meta.attrs['summary'] = 'Table of Lexicon'
