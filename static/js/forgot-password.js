document.getElementById('forgotPasswordForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Анимация отправки формы
    const formContainer = document.querySelector('.form-container');
    const successMessage = document.querySelector('.success-message');
    
    formContainer.style.animation = 'fadeOut 0.5s ease forwards';
    setTimeout(() => {
        formContainer.style.display = 'none';
        successMessage.style.display = 'block';
        successMessage.style.animation = 'fadeIn 0.6s ease forwards';
        
        // Перенаправление на страницу входа через 5 секунд
        setTimeout(() => {
            window.location.href = "login.html";
        }, 5000);
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