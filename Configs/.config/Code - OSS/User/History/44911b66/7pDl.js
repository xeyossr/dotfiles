document.addEventListener('DOMContentLoaded', function () {
    const userInfo = document.querySelector('.user-info');
    const dropdownMenu = userInfo.querySelector('.dropdown-menu');

    userInfo.querySelector('img').addEventListener('click', function (event) {
        event.stopPropagation(); // Diğer tıklamaların dropdown'u kapatmasını engelle
        userInfo.classList.toggle('active'); // Dropdown menüyü aç/kapa
    });

    document.addEventListener('click', function () {
        userInfo.classList.remove('active'); // Sayfanın başka bir yerine tıklayınca dropdown'u kapat
    });
});