from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.entry.models import Task

from django_tables2 import SingleTableView

from website.apps.entry.tables import TaskIndexTable

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
    """
    Show Task Detail
    """
    # 1. check if task is valid
    t = get_object_or_404(Task, pk=task_id)
        
    # 2. check if task is complete
    if t.done:
        return redirect('task-index')
    
    form = None
    # # get form...
    # _temp = __import__("website.apps.entry.forms", globals(), locals(), [str(t.form)])
    # #context['form'] = getattr(_temp, context['task'].form)(initial={'editor': self.request.user})
    # form = getattr(_temp, t.form)()
    
    return render_to_response('entry/detail.html', {
        'task': t,
        'form': form,
    })
    
