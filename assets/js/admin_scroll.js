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
});
