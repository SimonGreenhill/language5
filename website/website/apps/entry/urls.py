from django.conf.urls import *

from website.apps.entry import views as v

urlpatterns = patterns('',
    url(r'^$', v.TaskIndex.as_view(), name="index"),
    url(r'^task/quick$', v.quick_entry, name="quick"),
    url(r'^task/(?P<task_id>\d+)$', v.task_detail, name="detail"),
    url(r'^task/(?P<pk>\d+)/done$', v.TaskComplete.as_view(), name="complete"),
)
