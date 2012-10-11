import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.models import Source, Language, Family

class DataTable(tables.Table):
    """Parent class for Datatables"""
    class Meta:
        sortable = True
        attrs = {
            'class': "table table-striped table-bordered table-condensed"
        }
    

class SourceIndexTable(DataTable):
    """Source Listing"""
    id = tables.LinkColumn('source-detail', args=[A('slug')])
    author = tables.LinkColumn('source-detail', args=[A('slug')])
    year = tables.LinkColumn('source-detail', args=[A('slug')])
    reference = tables.LinkColumn('source-detail', args=[A('slug')])
    
    class Meta(DataTable.Meta):
        model = Source
        order_by_field = 'author' # default sorting
        sequence = ('id', 'author', 'year', 'reference')
        exclude = ('editor', 'added', 'slug', 'comment')
        

class LanguageIndexTable(DataTable):
    """Language Listing"""
    id = tables.LinkColumn('language-detail', args=[A('slug')])
    language = tables.LinkColumn('language-detail', args=[A('slug')])
    isocode = tables.LinkColumn('language-detail', args=[A('slug')])
    
    class Meta(DataTable.Meta):
        model = Language
        order_by_field = 'language' # default sorting
        sequence = ('id', 'isocode', 'language')
        exclude = ('editor', 'added', 'slug', 'classification', 'information')


class FamilyIndexTable(DataTable):
    """Family Listing"""
    id = tables.LinkColumn('family-detail', args=[A('slug')])
    family = tables.LinkColumn('family-detail', args=[A('slug')])
    count = tables.LinkColumn('family-detail', args=[A('slug')])

    class Meta(DataTable.Meta):
        model = Family
        order_by_field = 'family' # default sorting
        sequence = ('id', 'family', 'count')
        exclude = ('editor', 'added', 'slug')

