// Обработчик для кнопки профиля
document.querySelector('.profile-btn').addEventListener('click', function() {
    alert('Открывается меню профиля');
});

// Обработчик для кнопки отправки сообщения
document.querySelector('.send-btn').addEventListener('click', function() {
    const textarea = document.querySelector('.chat-input textarea');
    if (textarea.value.trim() !== '') {
        alert('Сообщение отправлено: ' + textarea.value);
        textarea.value = '';
    }
});

// Обработчик для кнопки лайка
document.querySelector('.like-btn').addEventListener('click', function() {
    const icon = this.querySelector('i');
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        this.innerHTML = '<i class="fas fa-heart"></i> 246';
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        this.innerHTML = '<i class="far fa-heart"></i> 245';
    }
});