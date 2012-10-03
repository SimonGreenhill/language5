from django.conf.urls.defaults import patterns, url

from views import oai

urlpatterns = patterns('',
    url(r'^$', oai),
)
