from django.conf.urls import *

from website.apps.olac.views import oai

urlpatterns = [
    url(r'^$', oai, name='baseurl'),
]
