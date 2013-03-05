from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2 import SingleTableView

from website.apps.entry.models import Task
from website.apps.entry.tables import TaskIndexTable

from website.apps.entry.dataentry import available_views



# task index
class TaskIndex(SingleTableView):
    """Task Index"""
    model = Task
    template_name = 'entry/index.html'
    table_class = TaskIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'added'
    
    queryset = Task.objects.all().filter(done=False)
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskIndex, self).dispatch(*args, **kwargs)


@login_required()
def task_detail(request, task_id):
    "Handles routing of tasks"
    # 1. check if task is valid
    t = get_object_or_404(Task, pk=task_id)

    # 2. check if task is complete
    if t.done:
        return redirect('task-index')

    # get t.task
    for viewname, viewdesc in available_views:
        print viewname, viewdesc
        #return viewname(request, task)
    # else fail.
