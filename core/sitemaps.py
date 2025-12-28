from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            'core:home', 
            'products:shop', 
            'pages:about', 
            'pages:contact', 
            'pages:privacy', 
            'pages:returns'
        ]

    def location(self, item):
        return reverse(item)
