from django.urls import path, re_path

from website.apps.maps.views import WordMap, LanguageMap, CognateSetMap, DataMap

app_name = 'maps'

urlpatterns = [
    re_path(r'word/(?P<slug>[\w\d\-\.]+)$', WordMap.as_view(), name="word-map"),
    path('cognate/<int:pk>', CognateSetMap.as_view(), name="cognate-map"),
    path('language/', LanguageMap.as_view(), name="language-map"),
    path('data/', DataMap.as_view(), name="data-map"),
]