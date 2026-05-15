from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from adminsortable2.admin import SortableAdminMixin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Slider, TeamMember, ServiceCategory, Service, Blog, About,
    AboutFeature, Brand, SiteSettings, ChooseUs, ChooseUsFeature, CounterTwo,
    MarqueeItem, ContactMessage, MenuItem, AboutPage, AboutPageFeature,
    AboutCounter, ExpertiseArea, ExpertiseSkill, ServicePageSetting,
    ReferencePageSetting, ReferenceCategory, ReferenceItem, BlogPageSetting,
    ContactPageSetting
)


# ==========================================
# TEMEL ADMIN SINIFI
# ==========================================
class BaseUnfoldAdmin(ModelAdmin):
    """
    Tüm admin sınıflarının miras aldığı temel sınıf.
    - Liste görünümüne resim önizlemesi, Düzenle ve Sil butonları ekler
    """

    def get_list_display(self, request):
        base = list(super().get_list_display(request))

        # Resim önizleme alanı ekle (model image field varsa)
        field_names = [f.name for f in self.model._meta.get_fields()
                       if hasattr(f, 'name')]
        image_field = next(
            (f for f in ['image', 'logo_dark', 'header_bg'] if f in field_names),
            None
        )
        if image_field and 'image_tag' not in base:
            base.insert(0, 'image_tag')

        # Düzenle ve Sil butonları her zaman en sona ekle
        if 'edit_icon' not in base:
            base.append('edit_icon')
        if 'delete_icon' not in base:
            base.append('delete_icon')

        return tuple(base)

    def image_tag(self, obj):
        img_field = next(
            (attr for attr in ['image', 'logo_dark', 'header_bg'] if hasattr(obj, attr)),
            None
        )
        if img_field:
            img = getattr(obj, img_field)
            if img:
                return format_html(
                    '<img src="{}" style="width:45px;height:45px;'
                    'object-fit:cover;border-radius:6px;" />',
                    img.url
                )
        return "—"
    image_tag.short_description = "Görsel"

    def edit_icon(self, obj):
        meta = self.model._meta
        url = reverse(
            f"admin:{meta.app_label}_{meta.model_name}_change",
            args=[obj.pk]
        )
        return format_html(
            '<a href="{}" style="color:#3b82f6;display:inline-flex;'
            'align-items:center;gap:4px;" title="Düzenle">'
            '<span class="material-symbols-outlined" style="font-size:20px;">edit</span>'
            '</a>',
            url
        )
    edit_icon.short_description = "Düzenle"

    def delete_icon(self, obj):
        meta = self.model._meta
        url = reverse(
            f"admin:{meta.app_label}_{meta.model_name}_delete",
            args=[obj.pk]
        )
        return format_html(
            '<a href="{}" style="color:#ef4444;display:inline-flex;'
            'align-items:center;gap:4px;" title="Sil">'
            '<span class="material-symbols-outlined" style="font-size:20px;">delete</span>'
            '</a>',
            url
        )
    delete_icon.short_description = "Sil"


# ==========================================
# INLINE SINIFLAR
# ==========================================
class AboutFeatureInline(TabularInline):
    model = AboutFeature
    extra = 1
    verbose_name = "Özellik"
    verbose_name_plural = "Özellikler"

class ChooseUsFeatureInline(TabularInline):
    model = ChooseUsFeature
    extra = 1
    verbose_name = "Özellik Maddesi"
    verbose_name_plural = "Özellik Maddeleri"

class AboutPageFeatureInline(TabularInline):
    model = AboutPageFeature
    extra = 1
    verbose_name = "Özellik Maddesi"
    verbose_name_plural = "Özellik Maddeleri"

class AboutCounterInline(TabularInline):
    model = AboutCounter
    extra = 1
    verbose_name = "Sayaç"
    verbose_name_plural = "Sayaçlar"

class ExpertiseSkillInline(TabularInline):
    model = ExpertiseSkill
    extra = 1
    verbose_name = "Yetenek"
    verbose_name_plural = "Yetenekler"

class ServiceInline(TabularInline):
    model = Service
    extra = 1
    verbose_name = "Hizmet"
    verbose_name_plural = "Hizmetler"

class ReferenceItemInline(TabularInline):
    model = ReferenceItem
    extra = 1
    verbose_name = "Referans Firma"
    verbose_name_plural = "Referans Firmalar"

class MenuItemInline(TabularInline):
    model = MenuItem
    fk_name = 'parent'
    extra = 1
    verbose_name = "Alt Menü Elemanı"
    verbose_name_plural = "Alt Menü Elemanları"


# ==========================================
# ANA ADMIN SINIFLARI
# ==========================================

@admin.register(Slider)
class SliderAdmin(BaseUnfoldAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')
    search_help_text = "Başlık veya açıklama içinde arayın"


@admin.register(Brand)
class BrandAdmin(BaseUnfoldAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    search_help_text = "Marka adına göre arayın"


@admin.register(About)
class AboutAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)
    inlines = [AboutFeatureInline]


@admin.register(AboutFeature)
class AboutFeatureAdmin(BaseUnfoldAdmin):
    list_display = ('title',)
    search_fields = ('title',)





@admin.register(TeamMember)
class TeamMemberAdmin(BaseUnfoldAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')
    search_help_text = "Ad veya pozisyona göre arayın"


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(BaseUnfoldAdmin):
    list_display = ('name', 'slug')
    inlines = [ServiceInline]
    search_fields = ('name',)
    search_help_text = "Kategori adına göre arayın"


@admin.register(Service)
class ServiceAdmin(BaseUnfoldAdmin):
    list_display = ('title', 'category')
    search_fields = ('title', 'description')
    list_filter = ('category',)
    search_help_text = "Hizmet adı veya açıklamasına göre arayın"


@admin.register(Blog)
class BlogAdmin(BaseUnfoldAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author', 'content')
    list_filter = ('created_at', 'author')
    search_help_text = "Başlık, yazar veya içeriğe göre arayın"


@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)


@admin.register(ChooseUs)
class ChooseUsAdmin(BaseUnfoldAdmin):
    list_display = ('title',)
    inlines = [ChooseUsFeatureInline]


@admin.register(ChooseUsFeature)
class ChooseUsFeatureAdmin(BaseUnfoldAdmin):
    list_display = ('title',)


@admin.register(CounterTwo)
class CounterTwoAdmin(BaseUnfoldAdmin):
    list_display = ('title', 'number', 'symbol')
    search_fields = ('title',)


@admin.register(MarqueeItem)
class MarqueeItemAdmin(BaseUnfoldAdmin):
    list_display = ('text',)


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseUnfoldAdmin):
    list_display = ('name', 'surname', 'email', 'phone', 'is_read', 'created_at')
    search_fields = ('name', 'surname', 'email', 'message')
    list_filter = ('is_read', 'created_at')
    search_help_text = "Ad, soyad, e-posta veya mesaj içeriğine göre arayın"
    readonly_fields = ('name', 'surname', 'email', 'phone', 'website', 'message', 'created_at')

    def get_list_display(self, request):
        # ContactMessage için sadece Düzenle butonunu kaldır, Sil kalsın
        base = ['name', 'surname', 'email', 'phone', 'is_read', 'created_at']
        base.append('delete_icon')
        return tuple(base)


@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, BaseUnfoldAdmin):
    list_display = ('title', 'link', 'order')
    inlines = [MenuItemInline]
    search_fields = ('title', 'link')
    search_help_text = "Menü başlığı veya linke göre arayın"


@admin.register(AboutPage)
class AboutPageAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)
    inlines = [AboutPageFeatureInline, AboutCounterInline]


@admin.register(AboutPageFeature)
class AboutPageFeatureAdmin(BaseUnfoldAdmin):
    list_display = ('title',)


@admin.register(AboutCounter)
class AboutCounterAdmin(BaseUnfoldAdmin):
    list_display = ('title', 'number', 'symbol', 'about_page')
    list_filter = ('about_page',)
    search_fields = ('title', 'description')
    search_help_text = "Sayaç başlığına göre arayın"


@admin.register(ExpertiseArea)
class ExpertiseAreaAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)
    inlines = [ExpertiseSkillInline]


@admin.register(ExpertiseSkill)
class ExpertiseSkillAdmin(BaseUnfoldAdmin):
    list_display = ('title', 'percentage', 'expertise')
    list_filter = ('expertise',)
    search_fields = ('title',)
    search_help_text = "Yetenek adına göre arayın"
    ordering = ('expertise', 'title')


@admin.register(ServicePageSetting)
class ServicePageSettingAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)


@admin.register(ReferencePageSetting)
class ReferencePageSettingAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)


@admin.register(ReferenceCategory)
class ReferenceCategoryAdmin(SortableAdminMixin, BaseUnfoldAdmin):
    list_display = ('title', 'order')
    inlines = [ReferenceItemInline]
    search_fields = ('title',)
    search_help_text = "Kategori başlığına göre arayın"


@admin.register(ReferenceItem)
class ReferenceItemAdmin(BaseUnfoldAdmin):
    list_display = ('name', 'category', 'show_on_homepage', 'order')
    list_editable = ('show_on_homepage', 'order')
    search_fields = ('name',)
    list_filter = ('category', 'show_on_homepage')
    search_help_text = "Firma adına göre arayın"


@admin.register(BlogPageSetting)
class BlogPageSettingAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)


@admin.register(ContactPageSetting)
class ContactPageSettingAdmin(BaseUnfoldAdmin):
    list_display = ('__str__',)