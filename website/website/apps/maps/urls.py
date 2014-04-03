from django.conf.urls import *

from views import WordMap

urlpatterns = patterns('',
    url(r'word/(?P<slug>[\w\d\-\.]+)$', 
        WordMap.as_view(),
        name="word-map"
    ),
)
