document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Анимация отправки формы
    const formContainer = document.querySelector('.form-container');
    const successMessage = document.querySelector('.success-message');
    
    formContainer.style.animation = 'fadeOut 0.5s ease forwards';
    setTimeout(() => {
        formContainer.style.display = 'none';
        successMessage.style.display = 'block';
        successMessage.style.animation = 'fadeIn 0.6s ease forwards';
        
        // Здесь можно добавить редирект после успешного входа
        setTimeout(() => {
            window.location.href = "{% url 'main' %}"; // Замените на нужный URL
        }, 2000);
    }, 500);
});

// Добавляем ключевые кадры для анимации fadeOut
const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: translateY(-20px) scale(0.95);
        }
    }
`;
document.head.appendChild(style);

// Обработчик для кнопки Telegram
document.querySelector('.telegram-btn').addEventListener('click', function(e) {
    e.preventDefault();
    // Здесь можно добавить логику входа через Telegram
    alert('Функция входа через Telegram будет реализована здесь');
});
setTimeout(() => {
    window.location.href = "{% url 'main' %}";
}, 2000);