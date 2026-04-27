import os
from django.core.exceptions import ValidationError

def validate_image_extension(value):
    """
    Kullanıcıların yalnızca güvenli resim dosyalarını yükleyebilmesini sağlar.
    Virüslü .exe, .php vb. dosyaların yüklenmesini engeller.
    """
    ext = os.path.splitext(value.name)[1]  # Dosya uzantısını al
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Desteklenmeyen dosya formatı. Lütfen şu formatlardan birini kullanın: {", ".join(valid_extensions)}')

def validate_file_size(value):
    """
    Sunucuya yüklenecek maksimum dosya boyutunu belirler.
    DDoS veya Storage doldurma saldırılarına karşı korur. (Örn: Max 5MB)
    """
    max_size_mb = 5
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Dosya boyutu çok büyük. Maksimum {max_size_mb} MB olmalıdır.')
