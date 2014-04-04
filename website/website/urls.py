from django.conf import settings
from django.conf.urls import *
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from website.apps.core.resources import LanguageResource, SourceResource
from website.apps.lexicon.resources import WordResource


v1_api = Api(api_name='v1')
v1_api.register(LanguageResource())
v1_api.register(SourceResource())
v1_api.register(WordResource())

from website.apps.maps.resources import LanguageMapResource
v1_api.register(LanguageMapResource())



from website.apps.core.views import LanguageIndex, RobotsTxt
from website.apps.core.views import SourceIndex, SourceDetail
from website.apps.core.views import FamilyIndex, FamilyDetail

from website.apps.lexicon.views import WordIndex, WordDetail
from website.apps.lexicon.views import CognateSetIndex, CognateSetDetail
from website.apps.lexicon.views import LexiconDetail, LexiconEdit

from sitemap import sitemaps

urlpatterns = patterns('',
    # Main Page / Home
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    
    # About
    url(r'^about', TemplateView.as_view(template_name="about.html"), name="about"),
    
    # ------------------------------------------------------------------------ #
    # Core
    # ------------------------------------------------------------------------ #
    
    # Language-Index: Show all languages
    url(r'^language/$', LanguageIndex.as_view(), name="language-index"),
    
    # Source-Index: Show all sources
    url(r'^source/$', SourceIndex.as_view(), name="source-index"),
    
    # Family-Index: Show all families
    url(r'^family/$', FamilyIndex.as_view(), name="family-index"),
    
    # Language-Detail: Show the given language
    url(r'^language/(?P<language>[\w\d\-\.]+)$', 
        'website.apps.core.views.language_detail', 
        name="language-detail"
    ),
    
    # Source-Detail: Show the given source
    url(r'^source/(?P<slug>[\w\d\-\.]+)$', SourceDetail.as_view(), name="source-detail"),

    # Family-Detail: Show the given family
    url(r'^family/(?P<slug>[\w\d\-\.]+)$', FamilyDetail.as_view(), name="family-detail"),

    # ISO Lookup: redirects to the language page
    url(r'^iso/(?P<iso>\w{3})$', 
        'website.apps.core.views.iso_lookup', 
        name="iso-lookup"
    ),

    # search page
    url(r"^search/", include('watson.urls', namespace='watson')),
    
    # Sitemap
    url(r'^sitemap.xml', include('static_sitemaps.urls')),
       
    # Robots.txt
    url(r'^robots\.txt$', RobotsTxt.as_view(),  name='robots_txt'),
    
    # OAI:
    url(r'^oai/', include('website.apps.olac.urls')),
    
    # ADMIN
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, 
        name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),
    
    url(r'^favicon\.ico$', RedirectView.as_view(url='%s/favicon.ico' % settings.STATIC_URL)),
    
    (r'^api/', include(v1_api.urls)),
)



# ------------------------------------------------------------------------ #
# Lexicon
# ------------------------------------------------------------------------ #
if 'website.apps.lexicon' in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        # Word-Index: Show all words
        url(r'^word/$', WordIndex.as_view(), name="word-index"),
        
        # Word-Detail: Show the given word
        url(r'^word/(?P<slug>[\w\d\-\.]+)$', WordDetail.as_view(), name="word-detail"),
        
        # Subset-Detail: Show the given word subset
        url(r'^word/\?subset=(?P<slug>[\w\d\-\.]+)$', WordDetail.as_view(), name="subset-detail"),
        
        # lexicon-detail: detail of lexical item.
        url(r'^lexicon/(?P<pk>\d+)$', LexiconDetail.as_view(), name="lexicon-detail"),
        
        # cognateset-index: List cognate Sets
        url(r'^cognate/$', CognateSetIndex.as_view(), name="cognateset-index"),
        
        # cognateset-detail: details of cognate sets
        url(r'^cognate/(?P<pk>\d+)$', CognateSetDetail.as_view(), name="cognateset-detail"),
        
        # Admin/Editor pages
        # lexicon-edit: edit lexical item.
        url(r'^lexicon/(?P<pk>\d+)/edit$', LexiconEdit.as_view(), name="lexicon-edit"),
        url(r'^word/(?P<slug>[\w\d\-\.]+)/edit$', 'website.apps.lexicon.views.word_edit', name="word-edit"),
    )

# ------------------------------------------------------------------------ #
# Pronouns
# ------------------------------------------------------------------------ #
if 'website.apps.pronouns' in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        url(r"^pronouns/", include('website.apps.pronouns.urls', namespace='pronouns')),
    )

# ------------------------------------------------------------------------ #
# Data Entry
# ------------------------------------------------------------------------ #
if 'website.apps.entry' in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        url(r"^entry/", include('website.apps.entry.urls', namespace='entry')),
    )

# ------------------------------------------------------------------------ #
# Statistics                                                               #
# ------------------------------------------------------------------------ #
if 'website.apps.statistics' in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        url(r"^statistics/", include('website.apps.statistics.urls', namespace='statistics')),
    )


# ------------------------------------------------------------------------ #
# Maps                                                                     #
# ------------------------------------------------------------------------ #
if 'website.apps.maps' in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        url(r"^maps/", include('website.apps.maps.urls', namespace='maps')),
    )



# ------------------------------------------------------------------------ #
# Debug Media...
# ------------------------------------------------------------------------ #
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    
