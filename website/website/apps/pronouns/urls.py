from django.conf.urls import *

from website.apps.pronouns.views import Index

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name="index"),
    url(r'^(?P<paradigm_id>\d+)$', 
        'website.apps.pronouns.views.detail', name="detail"),
    url(r'^(?P<paradigm_id>\d+)/edit$', 
        'website.apps.pronouns.views.edit', name="edit"),
    url(r'^(?P<paradigm_id>\d+)/edit2$', 
        'website.apps.pronouns.views.edit_advanced', name="edit2"),
)
