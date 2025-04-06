// Обработчик для кнопки профиля
document.querySelector('.profile-btn').addEventListener('click', function() {
    alert('Открывается меню профиля');
});

document.addEventListener('DOMContentLoaded', function () {
    const readMoreLinks = document.querySelectorAll('.read-more');
    readMoreLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            alert('Читать далее: ' + this.previousElementSibling.textContent.trim());
        });
    });
});