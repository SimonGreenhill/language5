from django.conf.urls.defaults import *

from olac.views import oai

urlpatterns = patterns('',
    url(r'^$', oai),
)
