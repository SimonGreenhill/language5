from django.conf.urls import *

from views import oai

urlpatterns = patterns('',
    url(r'^$', oai, name='baseurl'),
)
