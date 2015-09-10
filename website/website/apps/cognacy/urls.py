from django.conf.urls import *

from website.apps.cognacy.views import CognateSourceIndex, CognateSourceDetail
from website.apps.cognacy.views import CognateSetDetail

urlpatterns = patterns('',
    # PUBLIC
    
    # index page -- two names, index/source_index to allow later respecification
    url(r'^$', CognateSourceIndex.as_view(), name="index"),
    url(r'^$', CognateSourceIndex.as_view(), name="source_index"),
    
    # detail: details of cognate sets
    url(r'^source/(?P<slug>[\w\d\-\.]+)$', 
        CognateSourceDetail.as_view(), name="cognatesource_detail"
    ),
    
    # PRIVATE
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
