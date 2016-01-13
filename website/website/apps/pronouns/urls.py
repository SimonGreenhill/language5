from django.conf.urls import patterns, url

from website.apps.pronouns import views as v

urlpatterns = patterns('',
    url(r'^$', v.Index.as_view(), name="index"),
    url(r'add$', v.add, name="add"),
    url(r'^(?P<paradigm_id>\d+)$', v.detail, name="detail"),
    url(r'^(?P<paradigm_id>\d+)/edit$', v.edit, name="edit"),
    url(r'^(?P<paradigm_id>\d+)/relationship$', v.edit_relationships, name="edit_relationships"),
    url(r'^(?P<paradigm_id>\d+)/copy$', v.copy, name="copy_paradigm"),
    url(r'^(?P<paradigm_id>\d+)/rule$', v.process_rule, name="process_rule"),
)
