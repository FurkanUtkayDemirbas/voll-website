from django.core.cache import cache
from django.http import HttpResponseForbidden
from functools import wraps

def rate_limit(requests=5, window=60):
    """
    Belirli bir IP adresinden gelen istekleri sınırlandıran güvenlik dekoratörü.
    Brute-force (kaba kuvvet) şifre denemelerini ve iletişim formu spamlarını engeller.
    
    Kullanım:
    @rate_limit(requests=5, window=60)
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Form postlanıyorsa IP adresini kontrol et
            if request.method == 'POST':
                # Kullanıcının IP adresini al (Proxy vs destekli)
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                # Cache anahtarını view adı ve IP ile oluştur
                cache_key = f"rate_limit_{view_func.__name__}_{ip}"
                
                # Mevcut istek sayısını al
                request_count = cache.get(cache_key, 0)
                
                if request_count >= requests:
                    # Limiti aştıysa 403 Forbidden dön
                    return HttpResponseForbidden(
                        f"Çok fazla istek gönderdiniz. Güvenlik sebebiyle {window} saniye geçici olarak engellendiniz. Lütfen daha sonra tekrar deneyin."
                    )
                
                # İstek sayısını artır ve süresini ayarla
                cache.set(cache_key, request_count + 1, window)
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
