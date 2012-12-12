from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.entry.models import Task, Content, Result

from django_tables2 import SingleTableView

from website.apps.entry.tables import TaskIndexTable

class TaskIndex(SingleTableView):
    """Task Index"""
    model = Task
    template_name = 'entry/index.html'
    table_class = TaskIndexTable
    table_pagination = {"per_page": 50}
    order_by_field = 'name'
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskIndex, self).dispatch(*args, **kwargs)
    

class TaskDetail(DetailView):
    """Task Detail"""
    model = Task
    template_name = 'entry/detail.html'
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskDetail, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context['contents'] = ContentIndexTable(kwargs['object'].content_set.all())
        return context
    
    
class TaskEntry(DetailView):
    """Task Detail"""
    model = Task
    template_name = 'entry/detail.html'
    
    # ensure logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskEntry, self).dispatch(*args, **kwargs)
    
    