from django.conf.urls import url

from website.apps.statistics.views import statistics

app_name = 'statistics'

urlpatterns = [
    url(r'^$', statistics, name="statistics"),
]
