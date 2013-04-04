from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseServerError

from django_tables2 import SingleTableView

from website.apps.entry.models import Task
from website.apps.entry.tables import TaskIndexTable

from website.apps.entry import dataentry


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
        return redirect('entry:index')
    # 3. send to correct view
    views = dict(dataentry.available_views)
    if t.view in views:
        viewfunc = getattr(dataentry, t.view)
        return viewfunc(request, t)
    else:
        # ...but if we don't know which view, then we die.
        return HttpResponseServerError("Can't find view %s" % t.view)
    
    
