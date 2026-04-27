from .models import SiteSettings, MenuItem

def global_settings(request):
    return {
        'settings': SiteSettings.objects.first(),
        # Sadece "ana menüleri" gönderiyoruz. Alt menüleri HTML içinde çekeceğiz.
        'menu_items': MenuItem.objects.filter(parent=None).order_by('order') 
    }