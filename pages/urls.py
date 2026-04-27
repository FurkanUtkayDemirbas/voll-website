from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kurumsal/', views.about, name='about'),
    path('kurumsal/uzmanlik-alanlari/', views.uzmanlik_alanlari, name='uzmanlik_alanlari'),
    path('kurumsal/hakkimizda-ozet/', views.hakkimizda_ozet, name='hakkimizda_ozet'),
    path('hizmetler/<slug:kategori_slug>/', views.hizmetler, name='hizmetler'),
    path('referanslar/', views.references, name='references'),
    path('duyurular/', views.blog, name='blog'),
    path('duyuru/<int:id>/', views.blog_details, name='blog_details'),
    path('iletisim/', views.contact, name='contact'),
    # ── Admin Auth ──
    path('giris/', views.admin_giris, name='admin_giris'),
    path('kayit/', views.admin_kayit, name='admin_kayit'),
    path('cikis/', views.admin_cikis, name='admin_cikis'),
]