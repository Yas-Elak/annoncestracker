from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'monthly'
    i18n = True

    def items(self):
        return ['faq', 'login', 'contact', 'upgrade', 'homepage', 'register']

    def location(self, item):
        return reverse(item)

