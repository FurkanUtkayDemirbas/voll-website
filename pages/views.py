from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import rate_limit
from .models import Counter, TeamMember, ServiceCategory, Service, Blog, Slider, About, AboutFeature, Brand, SiteSettings, ChooseUs, ChooseUsFeature, CounterTwo, MarqueeItem, ContactMessage, AboutPage, AboutPageFeature, AboutCounter, ExpertiseArea, ExpertiseSkill, ServicePageSetting, ReferencePageSetting, ReferenceCategory, ReferenceItem, BlogPageSetting, ContactPageSetting

def index(request):
    # EĞER FORM GÖNDERİLDİYSE (POST İŞLEMİ)
    if request.method == "POST":
        # Formdaki name etiketlerine göre verileri alıyoruz
        name = request.POST.get('name')
        surname = request.POST.get('surname') # Tasarımında ikinci bir 'name' var, onu 'surname' yapacağız HTML'de
        email = request.POST.get('email')
        phone = request.POST.get('number')
        website = request.POST.get('website')
        message = request.POST.get('messages')

        # Veritabanına kaydediyoruz
        ContactMessage.objects.create(
            name=name,
            surname=surname,
            email=email,
            phone=phone,
            website=website,
            message=message
        )
        
        # Başarılı mesajı oluşturup aynı sayfaya geri yönlendiriyoruz
        messages.success(request, "Mesajınız başarıyla gönderildi. En kısa sürede dönüş yapacağız.")
        return redirect('index') # 'index' ismini urls.py dosyanızdaki name="index" kısmından alır

    # EĞER SAYFA NORMAL AÇILDIYSA (GET İŞLEMİ)
    latest_blogs = Blog.objects.all().order_by('-created_at')[:4]

    context = {

        'team_members': TeamMember.objects.all(),
        'sap_services': Service.objects.filter(category__slug='sap-solutions'),
        'dia_services': Service.objects.filter(category__slug='dia-solutions'),
        'web_services': Service.objects.filter(category__slug='web-solutions'),
        'main_blog': latest_blogs.first() if latest_blogs else None,
        'other_blogs': latest_blogs[1:] if latest_blogs.count() > 1 else [],
        'slider': Slider.objects.first(),
        'about': About.objects.first(),
        'about_features': AboutFeature.objects.all(),
        'brands': ReferenceItem.objects.filter(show_on_homepage=True).order_by('order'),
        'choose_us': ChooseUs.objects.first(),
        'choose_features': ChooseUsFeature.objects.all(),
        'counter_twos': CounterTwo.objects.all(),
        'marquees': MarqueeItem.objects.all(),
    }
    return render(request, 'index.html', context)


def about(request):
    expertise = ExpertiseArea.objects.first()
    context = {
        'about_page': AboutPage.objects.first(),
        'about_features': AboutPageFeature.objects.filter(about_page=AboutPage.objects.first()),
        'about_counters': AboutCounter.objects.filter(about_page=AboutPage.objects.first()),
        'expertise': expertise,
        'expertise_skills': ExpertiseSkill.objects.filter(expertise=expertise) if expertise else [],
    }
    return render(request, 'about.html', context)


def uzmanlik_alanlari(request):
    expertise = ExpertiseArea.objects.first()
    context = {
        'expertise': expertise,
        'expertise_skills': ExpertiseSkill.objects.filter(expertise=expertise) if expertise else [],
    }
    return render(request, 'uzmanlik_alanlari.html', context)


def hakkimizda_ozet(request):
    context = {
        'about_page': AboutPage.objects.first(),
        'about_features': AboutPageFeature.objects.filter(about_page=AboutPage.objects.first()),
        'about_counters': AboutCounter.objects.filter(about_page=AboutPage.objects.first()),
    }
    return render(request, 'hakkimizda_ozet.html', context)


def hizmetler(request, kategori_slug):
    kategori = get_object_or_404(ServiceCategory, slug=kategori_slug)
    context = {
        'page_settings': ServicePageSetting.objects.first(),
        'kategori': kategori,
        'services': Service.objects.filter(category=kategori),
    }
    return render(request, 'services.html', context)


def references(request):
    context = {
        'page_settings': ReferencePageSetting.objects.first(),
        # Tüm kategorileri (ve içindeki referansları) çekiyoruz
        'categories': ReferenceCategory.objects.all(),
    }
    return render(request, 'references.html', context)


def blog(request):
    # Tüm blogları tarihe göre yeniden eskiye sıralayarak çekiyoruz
    blog_list = Blog.objects.all().order_by('-created_at')
    
    # Sayfada kaç blog görünsün istiyorsak buraya yazıyoruz (Örn: 4)
    paginator = Paginator(blog_list, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_settings': BlogPageSetting.objects.first(),
        'page_obj': page_obj, # Ekrana basacağımız bloglar artık bu değişkenin içinde
        'recent_blogs': blog_list[:3], # Sağ taraftaki "Son Yazılar" kısmı için son 3 blog
    }
    return render(request, 'blog.html', context)

def blog_details(request, id):
    blog = get_object_or_404(Blog, id=id)
    recent_blogs = Blog.objects.exclude(id=id).order_by('-created_at')[:3]
    page_settings = BlogPageSetting.objects.first()
    
    context = {
        'blog': blog,
        'recent_blogs': recent_blogs,
        'page_settings': page_settings,
    }
    return render(request, 'blog-details.html', context)



@rate_limit(requests=3, window=60) # Dakikada en fazla 3 iletişim mesajı
def contact(request):
    # EĞER FORMDAN MESAJ GÖNDERİLDİYSE:
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname') 
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        message = request.POST.get('message')

        # Mesajı veritabanına kaydediyoruz
        ContactMessage.objects.create(
            name=name, surname=surname, email=email, 
            phone=phone, website=website, message=message
        )
        
        messages.success(request, "Mesajınız başarıyla gönderildi. En kısa sürede dönüş yapacağız.")
        return redirect('contact') 

    # EĞER SAYFA NORMAL AÇILDIYSA:
    context = {
        'page_settings': ContactPageSetting.objects.first(),
    }
    return render(request, 'contact.html', context)


# ─────────────────────────────────────────
#  ADMIN GİRİŞ / KAYIT / ÇIKIŞ
# ─────────────────────────────────────────

@rate_limit(requests=5, window=300) # 5 dakikada en çok 5 hatalı giriş (Brute Force koruması)
def admin_giris(request):
    """Admin paneli giriş sayfası."""
    # Zaten giriş yapmışsa admin paneline yönlendir
    if request.user.is_authenticated:
        return redirect('admin:index')

    hata = None
    kullanici_adi = ''

    if request.method == 'POST':
        kullanici_adi = request.POST.get('username', '').strip()
        sifre = request.POST.get('password', '')
        remember = request.POST.get('remember')

        kullanici = authenticate(request, username=kullanici_adi, password=sifre)

        if kullanici is not None:
            # Kullanıcı geçerli — giriş yap
            login(request, kullanici)

            # "Beni hatırla" seçilmemişse oturum tarayıcı kapanınca biter
            if not remember:
                request.session.set_expiry(0)

            # Güvenli yönlendirme: next parametresi varsa oraya, yoksa admin paneline git
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('admin:index')
        else:
            hata = 'Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.'

    context = {
        'hata': hata,
        'kullanici_adi': kullanici_adi,
    }
    return render(request, 'giris.html', context)


@login_required(login_url='/giris/')
@rate_limit(requests=3, window=60)
def admin_kayit(request):
    """Yeni admin kullanıcısı oluşturma sayfası — yalnızca superuser erişebilir."""
    if not request.user.is_superuser:
        messages.error(request, 'Bu sayfaya erişim yetkiniz bulunmamaktadır.')
        return redirect('admin:index')

    if request.method == 'POST':
        kullanici_adi = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        sifre1 = request.POST.get('password1', '')
        sifre2 = request.POST.get('password2', '')

        # Doğrulama
        if not kullanici_adi:
            messages.error(request, 'Kullanıcı adı boş bırakılamaz.')
        elif User.objects.filter(username=kullanici_adi).exists():
            messages.error(request, f'"{kullanici_adi}" kullanıcı adı zaten kullanılıyor.')
        elif len(sifre1) < 8:
            messages.error(request, 'Şifre en az 8 karakter olmalıdır.')
        elif sifre1 != sifre2:
            messages.error(request, 'Girilen şifreler birbirinden farklı.')
        else:
            # Kullanıcıyı oluştur
            yeni_kullanici = User.objects.create_user(
                username=kullanici_adi,
                email=email,
                password=sifre1,
                first_name=first_name,
                last_name=last_name,
            )
            # Staff yetkisi ver (admin paneline girebilsin)
            yeni_kullanici.is_staff = True
            yeni_kullanici.save()

            messages.success(request, f'"{kullanici_adi}" kullanıcısı başarıyla oluşturuldu.')
            return redirect('admin:index')

    return render(request, 'kayit.html')


def admin_cikis(request):
    """Oturumu kapat ve giriş sayfasına yönlendir."""
    logout(request)
    messages.success(request, 'Oturumunuz başarıyla kapatıldı.')
    return redirect('admin_giris')