import base64
import pickle
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseServerError, QueryDict
from django.views.generic import DetailView

from django_tables2 import SingleTableView, RequestConfig

from website.apps.entry.models import Task
from website.apps.entry.tables import TaskIndexTable, TaskLexiconTable
from website.apps.entry.forms import QuickEntryViewForm
from website.apps.entry import dataentry
from website.apps.entry.utils import task_log

import reversion

def encode_checkpoint(content):
    """Encodes a checkpoint (request.POST QueryDict) as database storable"""
    # make sure we're using protocol 2: http://bugs.python.org/issue2980
    # pickle it, then base64 it.
    return base64.b64encode(pickle.dumps(content, protocol=2))
    
def decode_checkpoint(content):
    """Restores the encoded checkpoint (request.POST QueryDict)"""
    try:
        return pickle.loads(base64.b64decode(content))
    except TypeError:
        return None
        
def make_querydict(content):
    qdict = QueryDict('checkpoint=1')
    q = qdict.copy() # have to do this to avoid "QueryDict instance is immutable"
    q.update(content)
    return q


# task index
class TaskIndex(SingleTableView):
    """Task Index"""
    model = Task
    template_name = 'entry/index.html'
    table_class = TaskIndexTable
    table_pagination = {"per_page": 50}
    order_by = 'added'
    
    queryset = Task.objects.filter(done=False).select_related('source', 'wordlist', 'language')    
    
    def get_context_data(self, **kwargs):
        context = super(TaskIndex, self).get_context_data(**kwargs)
        context['quickform'] = QuickEntryViewForm()
        return context
        
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        task_log(self.request, task=None, message="Viewed Task Index")
        return super(TaskIndex, self).dispatch(*args, **kwargs)




@login_required()
@reversion.create_revision()
def task_detail(request, task_id):
    "Handles routing of tasks"
    # check if task is valid
    t = get_object_or_404(Task, pk=task_id)
    # redirect away if task is complete
    if t.done:
        return redirect('entry:complete', pk=t.id)
    
    # If we've got POST data, then save checkpoint otherwise load the checkpoint
    # if it exists.
    if request.POST:
        task_log(request, task=t, message="Saved Checkpoint")
        t.checkpoint = encode_checkpoint(request.POST)
        t.save()
    elif t.checkpoint not in (None, u""):
        task_log(request, task=t, message="Loaded Checkpoint")
        request.POST = make_querydict(decode_checkpoint(t.checkpoint))
    
    # Finally send to correct view
    views = dict(dataentry.available_views)
    if t.view in views:
        viewfunc = getattr(dataentry, t.view)
        task_log(request, task=t, message="Called View Func: %s" % t.view)
        return viewfunc(request, t)
    else:
        task_log(request, task=t, message="Error - Can't find View Func %s" % t.view)
        # ...but if we don't know which view, then we die.
        return HttpResponseServerError("Can't find view %s for task %s" % (t.view, task_id))
    
    

@login_required()
@reversion.create_revision()
def quick_entry(request):
    """Quick data entry"""
    form = QuickEntryViewForm(request.POST)
    
    if not form.is_valid():
        return redirect('entry:index')
    
    # fake a task.
    descr = u"Source: %s\nLanguage: %s\nWordlist: %s" % (
           form.cleaned_data['source'], 
           form.cleaned_data['language'],
           form.cleaned_data['wordlist']
    )
    
    t = Task.objects.create(
        name=u"Quick", 
        description=descr,
        editor=request.user,
        source=form.cleaned_data['source'],
        wordlist=form.cleaned_data['wordlist'],
        language=form.cleaned_data['language'],
        records=form.cleaned_data['records'],
        view='WordlistView' if form.cleaned_data.get('wordlist', False) else 'GenericView',
        completable=True
    )
    t.save()
    task_log(request, task=t, message="Created Quick Entry Task")
    return redirect('entry:detail', task_id=t.id)


class TaskComplete(DetailView):
    """Task Index"""
    model = Task
    template_name = 'entry/complete.html'
    
    def get_context_data(self, **kwargs):
        context = super(TaskComplete, self).get_context_data(**kwargs)
        context['lexicon'] = TaskLexiconTable(kwargs['object'].lexicon.select_related().all())
        RequestConfig(self.request).configure(context['lexicon'])
        return context
        
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskComplete, self).dispatch(*args, **kwargs)
