from django.conf.urls import *

from views import WordMap, LanguageMap, CognateSetMap, DataMap

urlpatterns = [
    url(r'word/(?P<slug>[\w\d\-\.]+)$', WordMap.as_view(), name="word-map"),
    url(r'cognate/(?P<pk>\d+)$', CognateSetMap.as_view(), name="cognate-map"),
    url(r'language/$', LanguageMap.as_view(), name="language-map"),
    url(r'data/$', DataMap.as_view(), name="data-map"),
]