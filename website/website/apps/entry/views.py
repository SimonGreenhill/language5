from django.core import serializers

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseServerError

from django_tables2 import SingleTableView

from website.apps.entry.models import Task, TaskLog
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
    
    queryset = Task.objects.all().select_related().filter(done=False)
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        TaskLog.objects.create(person=self.request.user, 
                               page="website.apps.entry.task_index", 
                               message="Viewed Task Index")
        return super(TaskIndex, self).dispatch(*args, **kwargs)


@login_required()
def task_detail(request, task_id):
    "Handles routing of tasks"
    # 1. check if task is valid
    t = get_object_or_404(Task, pk=task_id)
    # 2. check if task is complete
    if t.done:
        TaskLog.objects.create(person=request.user, 
                               page="website.apps.entry.task_detail", 
                               message="Completed Task: %s" % task_id)
        return redirect('entry:index')
    
    # # 3. save checkpoint
    # if request.POST:
    #     t.checkpoint = serializers.serialize("json", request.POST)
    #     print 'SAVING ==========================================='
    #     print request.POST
    #     print "=================================================="
    #     t.save()
    # elif t.checkpoint:
    #     # load checkpoint if needed
    #     request.POST = serializers.deserialize("json", t.checkpoint)
    #     print 'LOADING ==========================================='
    #     print request.POST
    #     print "=================================================="
    #     TaskLog.objects.create(person=request.user, 
    #                            page="website.apps.entry.task_detail", 
    #                            message="Loaded Checkpoint: %s" % task_id)
    # 
    # 4. send to correct view
    views = dict(dataentry.available_views)
    if t.view in views:
        viewfunc = getattr(dataentry, t.view)
        TaskLog.objects.create(person=request.user, 
                               page="website.apps.entry.task_detail", 
                               message="Called View Func: %s" % t.view)
        return viewfunc(request, t)
    else:
        TaskLog.objects.create(person=request.user, 
                               page="website.apps.entry.task_detail", 
                               message="Error - Can't find View Func %s for task %s" % (t.view, task_id))
        # ...but if we don't know which view, then we die.
        return HttpResponseServerError("Can't find view %s for task %s" % (t.view, task_id))
    
    
