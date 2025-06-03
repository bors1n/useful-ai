from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Tools, Category

class ToolsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Tools.objects.all()

    def lastmod(self, obj):
        return obj.date_added

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return ['home', 'gallery', 'about', 'suggestion']

    def location(self, item):
        if item == 'home':
            return '/'
        return f'/{item}/' 