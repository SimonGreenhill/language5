import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from website.apps.core.tables import DataTable

from website.apps.entry.models import Task, Content

class TaskIndexTable(DataTable):
    """Task Listing"""
    id = tables.LinkColumn('content-list', args=[A('id')])
    name = tables.LinkColumn('content-list', args=[A('id')])
    task_count = tables.LinkColumn('content-list', args=[A('id')])
    
    class Meta(DataTable.Meta):
        model = Task
        order_by_field = 'name' # default sorting
        sequence = ('id', 'name', 'task_count', 'added', 'comment', 'source')
        exclude = ('editor', 'form')
    Meta.attrs['summary'] = 'Table of Tasks'
    

class ContentIndexTable(DataTable):
    """Content items Listing for a given task"""
    id = tables.LinkColumn('data-entry', args=[A('id')])
    description = tables.LinkColumn('data-entry', args=[A('id')])
    
    class Meta(DataTable.Meta):
        model = Content
        order_by_field = 'description' # default sorting
        sequence = ('id', 'description', 'comment', 'done')
        exclude = ('editor', 'added', 'image')
    Meta.attrs['summary'] = 'Table of Pages for this Task'

