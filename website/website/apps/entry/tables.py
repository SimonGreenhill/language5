import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from website.apps.core.tables import DataTable

from website.apps.entry.models import Task

class TaskIndexTable(DataTable):
    """Task Listing"""
    id = tables.LinkColumn('content-list', args=[A('id')])
    name = tables.LinkColumn('content-list', args=[A('id')])
    task_count = tables.LinkColumn('content-list', args=[A('id')])
    
    class Meta(DataTable.Meta):
        model = Task
        order_by_field = 'name' # default sorting
        sequence = ('id', 'name', 'description', 'added', 'source')
        exclude = ('editor', 'form')
    Meta.attrs['summary'] = 'Table of Tasks'
    

