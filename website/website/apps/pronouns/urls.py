from django.conf.urls import *

from website.apps.pronouns.views import Index

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name="index"),
    url(r'^edit/(?P<paradigm_id>\d+)$', 
        'website.apps.entry.views.edit', name="edit"),
)
