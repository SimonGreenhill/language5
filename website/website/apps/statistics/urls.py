from django.urls import path

from website.apps.statistics.views import statistics

app_name = 'statistics'

urlpatterns = [
    path('', statistics, name="statistics"),
]
