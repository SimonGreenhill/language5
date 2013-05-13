from django.conf.urls import *

from website.apps.pronouns.views import Index

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name="index"),
    url(r'add$', 'website.apps.pronouns.views.add', name="add"),
    url(r'^(?P<paradigm_id>\d+)$', 
        'website.apps.pronouns.views.detail', name="detail"),
    url(r'^(?P<paradigm_id>\d+)/edit$', 
        'website.apps.pronouns.views.edit', name="edit"),
    url(r'^(?P<paradigm_id>\d+)/relations$', 
        'website.apps.pronouns.views.edit_relationships', name="edit_relationships"),
    url(r'^(?P<paradigm_id>\d+)/rule$', 
        'website.apps.pronouns.views.process_rule', name="process_rule"),
)
