from django.conf.urls import *

from website.apps.cognacy.views import CognateSetIndex, CognateSetDetail

urlpatterns = patterns('',
    # index: List cognate Sets
    url(r'^$', CognateSetIndex.as_view(), name="index"),
    
    # detail: details of cognate sets
    url(r'^view/(?P<pk>\d+)$', CognateSetDetail.as_view(), name="detail"),
    
    url(r'^do/$', 
        'website.apps.cognacy.views.do_index',
        name="do_index"
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
