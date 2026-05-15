document.addEventListener("DOMContentLoaded", function() {
    // Sol taraftaki sidebar elementini (aside) bul
    let aside = document.querySelector('aside');
    
    if (aside) {
        // Genelde kaydırma işlemi overflow-y-auto class'ına sahip div üzerinde gerçekleşir
        let scrollArea = aside.classList.contains('overflow-y-auto') ? aside : aside.querySelector('.overflow-y-auto');
        if (!scrollArea) scrollArea = aside; // Alternatif fallback
        
        // Önceki sayfadan kalan scroll konumunu al ve uygula
        let savedScroll = sessionStorage.getItem('voll_sidebar_scroll');
        if (savedScroll) {
            scrollArea.scrollTop = parseInt(savedScroll, 10);
        }

        // Kullanıcı scroll yaptıkça konumu tarayıcı hafızasına (sessionStorage) kaydet
        scrollArea.addEventListener('scroll', function() {
            sessionStorage.setItem('voll_sidebar_scroll', scrollArea.scrollTop);
        });
    }

    // Add "Kayıt Ekle" text next to the floating add button in Unfold Admin
    function addRecordLabel() {
        // Unfold'un sağ üstteki artı butonunu hedefle
        let addBtn = document.querySelector('a[href$="/add/"]');
        if (addBtn && !document.querySelector('.custom-add-label')) {
            // Butonun yanına yazıyı ekle
            let label = document.createElement('span');
            label.className = 'custom-add-label';
            label.innerText = 'Kayıt Ekle';
            label.style.cssText = 'margin-right: 10px; font-weight: 600; color: #6b21a8; font-size: 14px; vertical-align: middle;';
            
            addBtn.parentNode.insertBefore(label, addBtn);
            
            // Butonu ve yazıyı hizalamak için kapsayıcıya stil ver
            addBtn.parentNode.style.display = 'flex';
            addBtn.parentNode.style.alignItems = 'center';
            addBtn.parentNode.style.justifyContent = 'flex-end';
        }
    }

    addRecordLabel();
    // Dinamik yüklemeler için kısa bir süre sonra tekrar dene
    setTimeout(addRecordLabel, 500);
});
