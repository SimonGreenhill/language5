from django.conf.urls import patterns, url

from website.apps.statistics.views import statistics

urlpatterns = [
    url(r'^$', statistics, name="statistics"),
]
