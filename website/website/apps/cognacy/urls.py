from django.urls import path, re_path

from website.apps.cognacy import views as v

app_name = 'cognacy'

urlpatterns = [
    # PUBLIC
    
    # index page -- two names, index/source_index to allow later respecification
    path('', v.CognateSourceIndex.as_view(), name="index"),
    path('', v.CognateSourceIndex.as_view(), name="source_index"),
    
    # detail: details of cognate sets
    re_path(r'^source/(?P<slug>[\w\d\-\.]+)$', 
        v.CognateSourceDetail.as_view(), name="cognatesource_detail"
    ),
    
    # PRIVATE
    path('view/<int:pk>', v.CognateSetDetail.as_view(), name="detail"),
    
    path('do/', v.do_index, name="do_index"),
    re_path(r'^do/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$', v.do, name="do"),
    re_path(r'^save/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$', v.save, name="save"),
    re_path(r'^merge/(?P<word>[\w\d\-\.]+)/(?P<clade>.*)$', v.merge, name="merge"),
]
