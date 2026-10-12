from django.conf import settings
from django.urls import include, path, re_path
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

from tastypie.api import Api
from website.apps.core.resources import LanguageResource, SourceResource
from website.apps.lexicon.resources import WordResource, LexiconResource

v1_api = Api(api_name='v1')
v1_api.register(LanguageResource())
v1_api.register(SourceResource())
v1_api.register(WordResource())
v1_api.register(LexiconResource())

from website.apps.maps.resources import LanguageMapResource
v1_api.register(LanguageMapResource())

from website.apps.core.views import LanguageIndex, RobotsTxt
from website.apps.core.views import SourceIndex, SourceDetail
from website.apps.core.views import FamilyIndex, FamilyDetail
from website.apps.core.views import language_detail, iso_lookup, glotto_lookup

from website.apps.lexicon.views import WordIndex, WordDetail
from website.apps.lexicon.views import LexiconDetail, LexiconEdit
from website.apps.lexicon.views import word_edit

from website.sitemap import sitemaps

urlpatterns = [
    # Main Page / Home
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    
    # About
    re_path(r'^about', TemplateView.as_view(template_name="about.html"), name="about"),
    
    # ------------------------------------------------------------------------ #
    # Core
    # ------------------------------------------------------------------------ #
    
    # Language-Index: Show all languages
    path('language/', LanguageIndex.as_view(), name="language-index"),
    
    # Source-Index: Show all sources
    path('source/', SourceIndex.as_view(), name="source-index"),
    
    # Family-Index: Show all families
    path('family/', FamilyIndex.as_view(), name="family-index"),
    
    # Language-Detail: Show the given language
    re_path(r'^language/(?P<language>[\w\d\-\.]+)$', language_detail, name="language-detail"),
    
    # Source-Detail: Show the given source
    re_path(r'^source/(?P<slug>[\w\d\-\.]+)$', SourceDetail.as_view(), name="source-detail"),

    # Family-Detail: Show the given family
    re_path(r'^family/(?P<slug>[\w\d\-\.]+)$', FamilyDetail.as_view(), name="family-detail"),

    # ISO/Glottocode Lookup: redirects to the language page
    re_path(r'^iso/(?P<iso>\w{3})$', iso_lookup, name="iso-lookup"),
    re_path(r'^glotto/(?P<glotto>\w{8})$', glotto_lookup, name="glotto-lookup"),

    # search page
    path("search/", include('watson.urls', namespace='watson'), {'paginate_by': 50, }),
    
    # Sitemap
    path('sitemap.xml', cache_page(86400)(sitemap_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemap-section'}, name='sitemap'),
    re_path(r'^sitemap-(?P<section>\w+)\.xml$', cache_page(86400)(sitemap_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemap-section'),
       
    # Robots.txt
    path('robots.txt', RobotsTxt.as_view(),  name='robots_txt'),
    
    # OAI:
    path('oai/', include('website.apps.olac.urls')),
    
    # ADMIN
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),
    
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    
    path('favicon.ico', RedirectView.as_view(url='%s/favicon.ico' % settings.STATIC_URL, permanent=True)),
    
    path('api/', include(v1_api.urls)),
    path('api', RedirectView.as_view(url='api/v1/')),
]



# ------------------------------------------------------------------------ #
# Lexicon
# ------------------------------------------------------------------------ #
if 'website.apps.lexicon' in settings.INSTALLED_APPS:
    urlpatterns.extend([
        # Word-Index: Show all words
        path('word/', WordIndex.as_view(), name="word-index"),
        
        # Word-Detail: Show the given word
        re_path(r'^word/(?P<slug>[\w\d\-\.]+)$', WordDetail.as_view(), name="word-detail"),
        
        # lexicon-detail: detail of lexical item.
        path('lexicon/<int:pk>', LexiconDetail.as_view(), name="lexicon-detail"),
        
        # Admin/Editor pages
        # lexicon-edit: edit lexical item.
        path('lexicon/<int:pk>/edit', LexiconEdit.as_view(), name="lexicon-edit"),
        re_path(r'^word/(?P<slug>[\w\d\-\.]+)/edit$', word_edit, name="word-edit"),
    ])
    urlpatterns.extend([
        path("cognacy/", include('website.apps.cognacy.urls', namespace='cognacy')),
    ])

# ------------------------------------------------------------------------ #
# Data Entry
# ------------------------------------------------------------------------ #
if 'website.apps.entry' in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("entry/", include('website.apps.entry.urls', namespace='entry'))
    )

# ------------------------------------------------------------------------ #
# Statistics                                                               #
# ------------------------------------------------------------------------ #
if 'website.apps.statistics' in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("statistics/", include('website.apps.statistics.urls', namespace='statistics'))
    )


# ------------------------------------------------------------------------ #
# Maps                                                                     #
# ------------------------------------------------------------------------ #
if 'website.apps.maps' in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("maps/", include('website.apps.maps.urls', namespace='maps'))
    )



# ------------------------------------------------------------------------ #
# Debug Media...
# ------------------------------------------------------------------------ #
if settings.DEBUG:
    from django.views.static import serve
    urlpatterns.append(
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    )
    
