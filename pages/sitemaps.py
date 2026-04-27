from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog, ServiceCategory

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['index', 'about', 'uzmanlik_alanlari', 'hakkimizda_ozet', 'references', 'blog', 'contact']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at
        
    def location(self, obj):
        return reverse('blog_details', kwargs={'id': obj.id})

class ServiceCategorySitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return ServiceCategory.objects.all()
        
    def location(self, obj):
        return reverse('hizmetler', kwargs={'kategori_slug': obj.slug})
