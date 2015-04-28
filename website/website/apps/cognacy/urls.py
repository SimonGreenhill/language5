from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 
        'website.apps.cognacy.views.index',
        name="index"
    ),
    url(r'^do/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$',
        'website.apps.cognacy.views.do',
        name="do"
    ),
    url(r'^save/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$',
        'website.apps.cognacy.views.save',
        name="save"
    ),
    url(r'^merge/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$',
        'website.apps.cognacy.views.merge',
        name="merge"
    ),
)
