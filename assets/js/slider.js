// HTML'den kategorileri otomatik al
const categoryContainers = document.querySelectorAll('.services-container');
let categories = [];
let currentIndex = 0;

// Kategorileri ve başlıklarını HTML'den oluştur
categoryContainers.forEach(container => {
    if (container.id) {
        // data-title varsa onu kullan, yoksa id'yi kullan (fallback)
        const title = container.getAttribute('data-title') || container.id;
        categories.push({
            id: container.id,
            title: title
        });
    }
});

function changeCategory(direction) {
    // Eğer hiç kategori yoksa işlem yapma
    if (categories.length === 0) return;

    // Mevcut olanı gizle
    const currentCategory = categories[currentIndex];
    const currentContainer = document.getElementById(currentCategory.id);
    if (currentContainer) {
        currentContainer.style.display = 'none';
        currentContainer.classList.remove('fade-in'); // Animasyon sınıfını kaldır
    }

    // Yeni indexi hesapla
    currentIndex += direction;
    if (currentIndex < 0) {
        currentIndex = categories.length - 1;
    } else if (currentIndex >= categories.length) {
        currentIndex = 0;
    }

    // Yeni olanı göster
    const newCategory = categories[currentIndex];
    const newContainer = document.getElementById(newCategory.id);

    // Başlığı Güncelle
    const titleEl = document.getElementById('categoryTitle');
    if (titleEl) titleEl.innerText = newCategory.title; // textContent yerine innerText kullanarak HTML entity sorunlarını önleyebiliriz

    // Yeni container'ı animasyonla göster
    if (newContainer) {
        newContainer.style.display = 'flex';

        // Reflow tetikleyerek animasyonu yeniden başlat
        void newContainer.offsetWidth;

        newContainer.classList.add('fade-in');
    }
}

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    const titleEl = document.getElementById('categoryTitle');

    // İlk kategori var mı kontrol et
    if (categories.length > 0) {
        // Başlangıç başlığını ayarla (HTML'de statik olsa bile JS ile senkronize ediyoruz)
        if (titleEl) titleEl.innerText = categories[0].title;

        // Sadece ilk kategoriyi göster, diğerlerini gizle
        categories.forEach((cat, index) => {
            const el = document.getElementById(cat.id);
            if (el) {
                if (index === 0) {
                    el.style.display = 'flex';
                    el.classList.add('fade-in');
                } else {
                    el.style.display = 'none';
                    el.classList.remove('fade-in');
                }
            }
        });
    }
});
