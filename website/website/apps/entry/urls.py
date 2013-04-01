from django.conf.urls import *

from website.apps.entry.views import TaskIndex

urlpatterns = patterns('',
    url(r'^$', TaskIndex.as_view(), name="index"),
    url(r'^(?P<task_id>\d+)$', 
        'website.apps.entry.views.task_detail', name="detail"),
)
