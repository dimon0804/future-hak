// Настройки
const settingsBtn = document.getElementById('settingsBtn');
const settingsMenu = document.getElementById('settingsMenu');

if (settingsBtn && settingsMenu) {
    settingsBtn.addEventListener('click', () => {
        settingsMenu.classList.toggle('active');
    });
}

// Тёмная тема
const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;
const themeIcon = darkModeToggle ? darkModeToggle.querySelector('i') : null;

function updateThemeImages() {
    const isDark = document.body.classList.contains('dark-mode');
    const defaultImages = document.querySelectorAll('.default-image');
    
    defaultImages.forEach(img => {
        // Получаем оригинальные пути из data-атрибутов
        const lightSrc = img.dataset.lightSrc || "{% static 'images/def.png' %}";
        const darkSrc = img.dataset.darkSrc || "{% static 'images/def-dark.png' %}";
        
        // Принудительно обновляем src
        img.src = isDark ? darkSrc : lightSrc;
    });
}

if (darkModeToggle && themeIcon) {
    // Проверяем сохранённую тему при загрузке
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
    }
    
    // Обновляем изображения и иконку при загрузке
    updateThemeImages();
    
    darkModeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        
        // Сохраняем выбор пользователя
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
        
        // Обновляем изображения и иконку
        updateThemeImages();
    });
}

// Обновление времени и даты
function updateDateTime() {
    const now = new Date();
    
    // Время
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const timeElement = document.getElementById('currentTime');
    if (timeElement) timeElement.textContent = `${hours}:${minutes}`;
    
    // Дата
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateElement = document.getElementById('currentDate');
    if (dateElement) dateElement.textContent = now.toLocaleDateString('ru-RU', options);
}

updateDateTime();
setInterval(updateDateTime, 60000); // Обновлять каждую минуту

// Поиск
const searchInput = document.querySelector('.search-input');
const searchBtn = document.querySelector('.search-btn');
const adCards = document.querySelectorAll('.ad-card');

if (searchInput && searchBtn) {
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        
        adCards.forEach(card => {
            const title = card.querySelector('.ad-title').textContent.toLowerCase();
            const description = card.querySelector('.ad-description').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

// Фильтры
const filterOptions = document.querySelectorAll('.filter-option input');
const applyBtn = document.querySelector('.subbtn');

if (applyBtn) {
    applyBtn.addEventListener('click', () => {
        // Здесь можно добавить логику фильтрации
        console.log('Фильтры применены');
    });
}
// Функция для обновления изображений при смене темы

document.addEventListener('DOMContentLoaded', function() {
    function updateThemeImages() {
        const isDarkMode = document.body.classList.contains('dark-mode');
        const defaultImages = document.querySelectorAll('.default-image');
        
        defaultImages.forEach(img => {
            const darkSrc = img.getAttribute('data-dark-src');
            if (darkSrc) {
                img.src = isDarkMode ? darkSrc : img.getAttribute('src');
            }
        });
    }

    // Принудительное обновление после загрузки страницы
    setTimeout(updateThemeImages, 100);
});

window.addEventListener('load', function() {
    // Двойная проверка после полной загрузки
    updateThemeImages();
});