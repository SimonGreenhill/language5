from django.conf.urls import *

from website.apps.entry.views import TaskIndex, TaskComplete

urlpatterns = patterns('',
    url(r'^$', TaskIndex.as_view(), name="index"),
    url(r'^task/quick$', 
        'website.apps.entry.views.quick_entry', name="quick"),
    url(r'^task/(?P<task_id>\d+)$', 
        'website.apps.entry.views.task_detail', name="detail"),
    url(r'^task/(?P<pk>\d+)/done$', TaskComplete.as_view(), name="complete"),
)
