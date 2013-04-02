import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from website.apps.core.tables import DataTable

from website.apps.pronouns.models import Paradigm


class ParadigmIndexTable(DataTable):
    """Paradigm Listing"""
    language = tables.LinkColumn('detail', args=[A('id')])
    source = tables.LinkColumn('core:source', args=[A('source__slug')])
    
    class Meta(DataTable.Meta):
        model = Paradigm
        order_by = 'language' # default sorting
        sequence = ('id', 'language', 'source')
        exclude = ('editor', 'added', 'comment')
    Meta.attrs['summary'] = 'Table of Paradigms'
