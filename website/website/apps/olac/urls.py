from django.conf.urls.defaults import patterns, url

from olac.views import oai

urlpatterns = patterns('',
    url(r'^$', oai),
)
