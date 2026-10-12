from django.urls import path

from website.apps.olac.views import oai

urlpatterns = [
    path('', oai, name='baseurl'),
]
