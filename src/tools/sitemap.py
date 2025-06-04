from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from .models import Tools, Category

class BaseSitemap(Sitemap):
    protocol = 'https'

class ToolsSitemap(BaseSitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Tools.objects.all().order_by('-date_added')

    def lastmod(self, obj):
        return obj.date_added

    def location(self, obj):
        return f'/tools/{obj.slug}/'

class CategorySitemap(BaseSitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all().order_by('name')

    def location(self, obj):
        return f'/tools/category/{obj.slug}/'

class StaticViewSitemap(BaseSitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return ['home', 'gallery', 'about', 'suggestion']

    def location(self, item):
        if item == 'home':
            return reverse('home')
        return reverse(item)

    def lastmod(self, item):
        # For static pages, we can return None or a fixed date
        return None 