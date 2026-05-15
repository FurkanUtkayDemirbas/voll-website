from django.db import models
from .validators import validate_image_extension, validate_file_size


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    image = models.ImageField(upload_to='slider_images/', validators=[validate_image_extension, validate_file_size], verbose_name="Arka Plan Resmi")
    
    btn1_text = models.CharField(max_length=50, default="Hizmetlerimiz", verbose_name="1. Buton Yazısı")
    btn1_link = models.CharField(max_length=200, default="services-sap.html", verbose_name="1. Buton Linki")
    
    btn2_text = models.CharField(max_length=50, default="İletişime Geç", verbose_name="2. Buton Yazısı")
    btn2_link = models.CharField(max_length=200, default="contact.html", verbose_name="2. Buton Linki")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ana Ekran (Slider)"
        verbose_name_plural = "Ana Ekran (Slider)"


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Marka Adı")
    image = models.ImageField(upload_to='brand_images/', validators=[validate_image_extension, validate_file_size], verbose_name="Marka Logosu")

    class Meta:
        verbose_name = "Referans Marka"
        verbose_name_plural = "Referans Markalar"

    def __str__(self):
        return self.name


class About(models.Model):
    experience_years = models.IntegerField(default=4, verbose_name="Deneyim Yılı")
    image = models.ImageField(upload_to='about_images/', validators=[validate_image_extension, validate_file_size], verbose_name="Hakkımızda Resmi (Büyük)")
    title = models.CharField(max_length=200, verbose_name="Ana Başlık")
    description = models.TextField(verbose_name="Açıklama Yazısı")

    class Meta:
        verbose_name = "Hakkımızda Alanı"
        verbose_name_plural = "Hakkımızda Alanı"

    def __str__(self):
        return "Hakkımızda Ayarları"

class AboutFeature(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='features', null=True, blank=True, verbose_name="Bağlı Olduğu Hakkımızda Modülü")
    title = models.CharField(max_length=100, verbose_name="Özellik Başlığı")
    description = models.TextField(verbose_name="Özellik Açıklaması")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="İkon Sınıfı")

    class Meta:
        verbose_name = "Hakkımızda Özelliği"
        verbose_name_plural = "Hakkımızda Özellikleri"

    def __str__(self):
        return self.title


class Counter(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlık (Örn: Başarı Oranı)")
    number = models.IntegerField(verbose_name="Sayı")
    symbol = models.CharField(max_length=10, verbose_name="Sembol (%, + vb.)", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "İstatistik"
        verbose_name_plural = "İstatistikler"

class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    role = models.CharField(max_length=100, verbose_name="Pozisyon")
    description = models.TextField(verbose_name="Açıklama")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ekip Üyesi"
        verbose_name_plural = "Ekip Üyeleri"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı (Örn: SAP Hizmetleri)")
    slug = models.SlugField(verbose_name="Kısa İsim (Örn: sap-solutions)", help_text="HTML'deki ID ile aynı olmalı")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hizmet Kategorisi"
        verbose_name_plural = "Hizmet Kategorileri"

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    author = models.CharField(max_length=100, default="admin", verbose_name="Yazar")
    seo_title = models.CharField(max_length=150, blank=True, null=True, verbose_name="SEO Başlığı")
    seo_description = models.TextField(blank=True, null=True, verbose_name="SEO Açıklaması")
    image = models.ImageField(upload_to='blog_images/', verbose_name="Blog Resmi")
    
    # İŞTE EKSİK OLAN O İKİ ALAN BURADA:
    short_description = models.TextField(verbose_name="Kısa Açıklama (Özet)", blank=True, null=True)
    content = models.TextField(verbose_name="Ana Metin (İçerik)", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        verbose_name = "Duyuru / Blog"
        verbose_name_plural = "Duyurular / Bloglar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    
    email = models.EmailField(default="info@volltr.com", verbose_name="E-posta Adresi")
    phone = models.CharField(max_length=20, default="+90 505 864 95 13", verbose_name="Telefon Numarası")
    address = models.CharField(max_length=255, default="Ankara, Türkiye", verbose_name="Adres")
    footer_text = models.TextField(default="Kurumsal çözümlerimiz ve dijital dönüşüm hizmetlerimizle işletmenize değer katıyoruz.", verbose_name="Footer Kısa Açıklama")
    
    logo_dark = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Koyu Logo (Normal)")
    logo_white = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Beyaz Logo (Şeffaf Menü İçin)")
    
    copyright_text = models.CharField(max_length=150, default="Tüm Hakları Saklıdır © 2025 VOLL", verbose_name="Telif Hakkı Yazısı")
    developer_text = models.CharField(max_length=150, default="Powered by Design furkandemirbas", verbose_name="Geliştirici Yazısı")
    # Sosyal Medya Linkleri
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook Linki")
    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter (X) Linki")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram Linki")
    pinterest = models.URLField(blank=True, null=True, verbose_name="Pinterest Linki")

    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Genel Site Ayarları"

    def __str__(self):
        return "İletişim ve Sosyal Medya Ayarları"


class MenuItem(models.Model):
    title = models.CharField(max_length=50, verbose_name="Menü Başlığı")
    link = models.CharField(max_length=200, default="#", verbose_name="Sayfa Linki (Örn: about.html)")
    order = models.IntegerField(default=0, verbose_name="Sıralama (Örn: 1, 2, 3)")
    
    # Kendi kendine bağlanan bu yapı sayesinde "Hizmetler" menüsünün altına "SAP", "Web" gibi alt menüler ekleyebileceğiz
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE, verbose_name="Üst Menü (Eğer alt menüyse seçin)")

    class Meta:
        verbose_name = "Menü Elemanı"
        verbose_name_plural = "Menü Elemanları"
        ordering = ['order'] # Admin panelinde sıraya göre dizer

    def __str__(self):
        return self.title


class ChooseUs(models.Model):
    subtitle = models.CharField(max_length=100, default="Neden Biz?", verbose_name="Alt Başlık")
    title = models.CharField(max_length=200, default="Özel BT Çözümleri ve Hizmetleri", verbose_name="Ana Başlık")
    description = models.TextField(verbose_name="Açıklama")

    class Meta:
        verbose_name = "Neden Biz (Ana Bilgi)"
        verbose_name_plural = "Neden Biz (Ana Bilgi)"

    def __str__(self):
        return self.title

class ChooseUsFeature(models.Model):
    choose_us = models.ForeignKey(ChooseUs, on_delete=models.CASCADE, related_name='features', null=True, blank=True, verbose_name="Bağlı Olduğu Neden Biz")
    title = models.CharField(max_length=150, verbose_name="Özellik Metni")

    class Meta:
        verbose_name = "Neden Biz Özelliği"
        verbose_name_plural = "Neden Biz Özellikleri"

    def __str__(self):
        return self.title

class CounterTwo(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlık (Örn: Tamamlanan Proje)")
    number = models.IntegerField(verbose_name="Sayı")
    symbol = models.CharField(max_length=10, blank=True, null=True, verbose_name="Sembol (+ vb.)")

    class Meta:
        verbose_name = "İkinci Sayaç"
        verbose_name_plural = "İkinci Sayaçlar"

    def __str__(self):
        return self.title

class MarqueeItem(models.Model):
    text = models.CharField(max_length=200, verbose_name="Kayan Yazı Metni")

    class Meta:
        verbose_name = "Kayan Yazı"
        verbose_name_plural = "Kayan Yazılar"

    def __str__(self):
        return self.text

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad")
    surname = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    website = models.URLField(blank=True, null=True, verbose_name="Web Sitesi")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")

    class Meta:
        verbose_name = "Gelen Mesaj"
        verbose_name_plural = "Gelen Mesajlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.surname} - {self.email}"



# About kısmı için model 


class AboutPage(models.Model):
    header_bg = models.ImageField(upload_to='about_images/', verbose_name="Üst Arka Plan Resmi")
    image_1 = models.ImageField(upload_to='about_images/', verbose_name="Sol Büyük Resim")
    image_2 = models.ImageField(upload_to='about_images/', verbose_name="Sağ Küçük Resim")
    satisfaction_text = models.CharField(max_length=100, default="100% Müşteri Memnuniyeti", verbose_name="Memnuniyet Yazısı")
    
    subtitle = models.CharField(max_length=100, default="Hakkımızda", verbose_name="Alt Başlık")
    title = models.CharField(max_length=200, default="Dijital Dönüşüm Yolculuğunuzda Güvenilir İş Ortağınız", verbose_name="Ana Başlık")
    description = models.TextField(verbose_name="Açıklama Yazısı")

    class Meta:
        verbose_name = "Kurumsal (Ana Bilgiler)"
        verbose_name_plural = "Kurumsal (Ana Bilgiler)"

    def __str__(self):
        return "Kurumsal Sayfası Ayarları"

class AboutPageFeature(models.Model):
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='features', null=True, blank=True, verbose_name="Bağlı Olduğu Sayfa")
    title = models.CharField(max_length=200, verbose_name="Özellik Maddesi")

    class Meta:
        verbose_name = "Kurumsal Özellik Maddesi"
        verbose_name_plural = "Kurumsal Özellik Maddeleri"

    def __str__(self):
        return self.title

class AboutCounter(models.Model):
    about_page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='counters', null=True, blank=True, verbose_name="Bağlı Olduğu Sayfa")
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.CharField(max_length=255, verbose_name="Kısa Açıklama")
    number = models.IntegerField(verbose_name="Sayı")
    symbol = models.CharField(max_length=10, default="+", verbose_name="Sembol")

    class Meta:
        verbose_name = "Kurumsal Sayaç"
        verbose_name_plural = "Kurumsal Sayaçlar"

    def __str__(self):
        return self.title

class ExpertiseArea(models.Model):
    image = models.ImageField(upload_to='about_images/', verbose_name="Uzmanlık Resmi")
    subtitle = models.CharField(max_length=100, default="Uzmanlıklarımız", verbose_name="Alt Başlık")
    title = models.CharField(max_length=200, default="İşletmenizi Dijital Güçle Geleceğe Taşıyoruz", verbose_name="Ana Başlık")
    description = models.TextField(verbose_name="Açıklama Yazısı")

    class Meta:
        verbose_name = "Uzmanlık Alanı (Ana Bilgiler)"
        verbose_name_plural = "Uzmanlık Alanı (Ana Bilgiler)"

    def __str__(self):
        return "Uzmanlık Alanı Ayarları"

class ExpertiseSkill(models.Model):
    expertise = models.ForeignKey(ExpertiseArea, on_delete=models.CASCADE, related_name='skills', null=True, blank=True, verbose_name="Bağlı Olduğu Uzmanlık")
    title = models.CharField(max_length=100, verbose_name="Yetenek Adı (Örn: SAP Danışmanlığı)")
    percentage = models.IntegerField(default=90, verbose_name="Yüzdelik Değer (Örn: 95)")

    class Meta:
        verbose_name = "Uzmanlık Yüzdesi"
        verbose_name_plural = "Uzmanlık Yüzdeleri"

    def __str__(self):
        return f"{self.title} - %{self.percentage}"




# Service kısmı için model 


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', verbose_name="Kategori")
    title = models.CharField(max_length=150, verbose_name="Hizmet Adı")
    seo_title = models.CharField(max_length=150, blank=True, null=True, verbose_name="SEO Başlığı")
    seo_description = models.TextField(blank=True, null=True, verbose_name="SEO Açıklaması")
    description = models.TextField(verbose_name="Kısa Açıklama")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="İkon Sınıfı (Ana sayfa için)")
    
    # YENİ EKLENEN SATIR (Detay sayfası resimleri için):
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Hizmet Resmi (Detay sayfası için)")
    
    link = models.CharField(max_length=200, default="#", verbose_name="Yönlendirme Linki")

    class Meta:
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"

    def __str__(self):
        return self.title

class ServicePageSetting(models.Model):
    header_bg = models.ImageField(upload_to='service_bg/', verbose_name="Sayfa Üst Arka Plan Resmi")

    class Meta:
        verbose_name = "Hizmetler Sayfası Ayarı"
        verbose_name_plural = "Hizmetler Sayfası Ayarları"

    def __str__(self):
        return "Hizmetler Sayfası Genel Ayarları"




# Reference kısmı için model 

class ReferencePageSetting(models.Model):
    header_bg = models.ImageField(upload_to='reference_bg/', verbose_name="Sayfa Üst Arka Plan Resmi")

    class Meta:
        verbose_name = "Referanslar Sayfası Ayarı"
        verbose_name_plural = "Referanslar Sayfası Ayarları"

    def __str__(self):
        return "Referanslar Sayfası Genel Ayarları"

class ReferenceCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Kategori Başlığı (Örn: SAP Hizmetleri Referansları)")
    subtitle = models.CharField(max_length=100, default="Güçlü İş Ortaklıkları", verbose_name="Alt Başlık")
    description = models.TextField(verbose_name="Açıklama")
    order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        verbose_name = "Referans Kategorisi"
        verbose_name_plural = "Referans Kategorileri"
        ordering = ['order']

    def __str__(self):
        return self.title

class ReferenceItem(models.Model):
    category = models.ForeignKey(ReferenceCategory, on_delete=models.CASCADE, related_name='references', verbose_name="Kategori")
    name = models.CharField(max_length=100, verbose_name="Firma Adı")
    image = models.ImageField(upload_to='references/', verbose_name="Firma Logosu")

    class Meta:
        verbose_name = "Referans Firma"
        verbose_name_plural = "Referans Firmalar"

    def __str__(self):
        return f"{self.name} ({self.category.title})"



# Blog kısmı için model 
class BlogPageSetting(models.Model):
    header_bg = models.ImageField(upload_to='blog_bg/', verbose_name="Sayfa Üst Arka Plan Resmi")

    class Meta:
        verbose_name = "Blog Sayfası Ayarı"
        verbose_name_plural = "Blog Sayfası Ayarları"

    def __str__(self):
        return "Blog Sayfası Genel Ayarları"


# İletişim kısmı için model 
class ContactPageSetting(models.Model):
    header_bg = models.ImageField(upload_to='contact_bg/', verbose_name="Sayfa Üst Arka Plan Resmi")
    address = models.CharField(max_length=255, default="INNOPARK Teknoloji Geliştirme Bölgesi SELÇUKLU / KONYA", verbose_name="Açık Adres")
    map_iframe = models.TextField(verbose_name="Harita Iframe Linki (Sadece src içindeki linki girin)", default="https://maps.google.com/maps?q=INNOPARK+Teknoloji+Geliştirme+Bölgesi&t=&z=15&ie=UTF8&iwloc=&output=embed")

    class Meta:
        verbose_name = "İletişim Sayfası Ayarı"
        verbose_name_plural = "İletişim Sayfası Ayarları"

    def __str__(self):
        return "İletişim Sayfası Genel Ayarları"