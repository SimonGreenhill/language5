from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'website.apps.statistics.views.statistics', name="statistics"),
)
