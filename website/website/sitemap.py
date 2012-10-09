from django.contrib.sitemaps import Sitemap
from website.apps.core.models import Language, Family, Source
from website.apps.lexicon.models import Word

class LanguageSitemap(Sitemap):
    changefreq = "website"
    priority = 0.5

    def items(self):
        return Language.objects.filter()

    def lastmod(self, obj):
        return obj.added


class FamilySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Family.objects.filter()

    def lastmod(self, obj):
        return obj.added

class SourceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Source.objects.filter()

    def lastmod(self, obj):
        return obj.added


class WordSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Word.objects.filter()

    def lastmod(self, obj):
        return obj.added