from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from sitemap import FamilySitemap, LanguageSitemap

urlpatterns = patterns('',
    
    # Main Index
    url(r'^$',
        TemplateView.as_view(template_name="index.html"),
        name="index"
    ),
    
    # about
    url(r'^about',
        TemplateView.as_view(template_name="about.html"),
        name="about"
    ),
    
    # Show all languages
    url(r'^language/$', 
        'website.apps.core.views.language_index', 
        name="language-index"
    ),
    # Show the given language
    url(r'^language/(?P<language>.+)$', 
        'website.apps.core.views.language_detail', 
        name="language-detail"
    ),
    # ISO Lookup: redirects to the language page ^
    url(r'^iso/(?P<iso>\w{3})$', 
        'website.apps.core.views.iso_lookup', 
        name="iso-lookup"
    ),
    
    # Show all families
    url(r'^family/$', 
        'website.apps.core.views.family_index', 
        name="family-index"
    ),
    # Show the given language
    url(r'^family/(?P<family>.+)$', 
        'website.apps.core.views.family_detail', 
        name="family-detail"
    ),
    
    

    
    #   (r'^family/(?P<family>\w+)/word/(?P<word>\w+)', ''), # 
    
    # words
    #    (r'^word/(?P<word>\w+)', ''), # 
    #    (r'^word/(?P<word>\w+)/(?P<cognate\w+)', '')
    
    # search page
    #    (r'^search/', ''), #
    
    # classification pages
    #    (r'^classification/', ''), # 
    #    (r'^classification/(?P<node>.*)', ''), # 
    
    # files
    #    (r'^files/(?P<filename>.*)', ''), # download file.
    
    # feeds
    #    (r'^feeds/', ''), 
    #    (r'^feeds/wordaday', ''),
    #    (r'^feeds/changes', ''),
    #    (r'^feeds/changes/(?P<language>\w+)', ''),
    
    # plumbing (sitemap, robots.txt)
    (r'^sitemap\.xml$', 
           'django.contrib.sitemaps.views.sitemap', 
           {'sitemaps': {'families': FamilySitemap, 'languages': LanguageSitemap}}
       ),
    (r'^robots\.txt$', include('robots.urls')),
    
    # OAI:
    (r'^oai/', include('website.apps.olac.urls')),
    
    # ADMIN
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
