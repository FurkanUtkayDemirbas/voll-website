from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

from core.settings import env

# .env dosyasındaki ADMIN_URL değişkeninden asıl adresi okuyoruz. 
# Eğer tanımlı değilse güvenlik için farklı bir adrestir.
admin_url = env('ADMIN_URL', default='voll-gizli-yonetim/')

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from pages.sitemaps import StaticViewSitemap, BlogSitemap, ServiceCategorySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'services': ServiceCategorySitemap,
}

urlpatterns = [
    path(admin_url, admin.site.urls),
    path('', include('pages.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

# Resimlerin tarayıcıda görünebilmesi için gerekli ayar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)