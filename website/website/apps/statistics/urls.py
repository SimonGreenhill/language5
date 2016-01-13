from django.conf.urls import patterns, url

from website.apps.statistics.views import statistics

urlpatterns = patterns('',
    url(r'^$', statistics, name="statistics"),
)
