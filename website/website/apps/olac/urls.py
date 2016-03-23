from django.conf.urls import *

from views import oai

urlpatterns = [
    url(r'^$', oai, name='baseurl'),
]
