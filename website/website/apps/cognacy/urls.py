from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 
        'website.apps.cognacy.views.index',
        name="index"
    ),
    url(r'^(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$',
        'website.apps.cognacy.views.do',
        name="do"
    ),
)
