from django.conf.urls import *

from website.apps.cognacy import views as v

urlpatterns = patterns('',
    # PUBLIC
    
    # index page -- two names, index/source_index to allow later respecification
    url(r'^$', v.CognateSourceIndex.as_view(), name="index"),
    url(r'^$', v.CognateSourceIndex.as_view(), name="source_index"),
    
    # detail: details of cognate sets
    url(r'^source/(?P<slug>[\w\d\-\.]+)$', 
        v.CognateSourceDetail.as_view(), name="cognatesource_detail"
    ),
    
    # PRIVATE
    url(r'^view/(?P<pk>\d+)$', v.CognateSetDetail.as_view(), name="detail"),
    
    url(r'^do/$', v.do_index, name="do_index"),
    url(r'^do/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$', v.do, name="do"),
    url(r'^save/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$', v.save, name="save"),
    url(r'^merge/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$', v.merge, name="merge"),
)
