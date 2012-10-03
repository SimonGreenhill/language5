from django.contrib.sitemaps import Sitemap
from website.apps.core.models import Language, Family

class LanguageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Language.objects.filter()

    def lastmod(self, obj):
        return obj.added


class FamilySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Family.objects.filter()

    def lastmod(self, obj):
        return obj.added
