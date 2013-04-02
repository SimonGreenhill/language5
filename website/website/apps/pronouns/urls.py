from django.conf.urls import *

from website.apps.pronouns.views import Index

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name="index"),
    url(r'^edit/$', 
        'website.apps.pronouns.views.add', name="add"),
    url(r'^edit/(?P<paradigm_id>\d+)$', 
        'website.apps.pronouns.views.edit', name="edit"),
    url(r'^(?P<paradigm_id>\d+)$', 
        'website.apps.pronouns.views.detail', name="detail"),
)
