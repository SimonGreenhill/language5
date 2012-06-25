from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'index.html'},
        name="index"
    ),
    
    #    (r'^/news/', ) # project news
    #    (r'^publications/', ''), # publications
    #    (r'^doc/', ''), # documentation/faq/ etc
            # -> about
            # -> links
            
    #    (r'^add/', ''), # 
    
    url(r'^about',
        'django.views.generic.simple.direct_to_template',
        {'template': 'about.html'},
        name="about"
    ),
    
    # Show all languages
    url(r'^language/$', 
        'core.views.language_index', 
        name="language-index"
    ),
    # Show the given language
    url(r'^language/(?P<language>.+)$', 
        'core.views.language_detail', 
        name="language-detail"
    ),
    # redirects to the language page ^
    url(r'^iso/(?P<iso>\w{3})$', 
        'core.views.iso_lookup', 
        name="iso-lookup"
    ),
    
    # Show all families
    url(r'^family/$', 
        'core.views.family_index', 
        name="family-index"
    ),
    # Show the given language
    url(r'^family/(?P<family>.+)$', 
        'core.views.family_detail', 
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
    ## (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
    (r'^robots\.txt$', include('robots.urls')),
    
    # ADMIN
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
