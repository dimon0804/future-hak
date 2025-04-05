// Фильтры по дате
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // Здесь должна быть логика обновления данных по выбранному периоду
        console.log('Выбран период:', this.textContent);
    });
});

// Применение кастомного диапазона дат
document.querySelector('.apply-btn').addEventListener('click', function() {
    const startDate = document.querySelectorAll('.date-input')[0].value;
    const endDate = document.querySelectorAll('.date-input')[1].value;
    
    if (startDate && endDate) {
        // Здесь должна быть логика загрузки данных за выбранный период
        console.log('Загрузка данных с', startDate, 'по', endDate);
        
        // Деактивируем другие кнопки фильтров
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    } else {
        alert('Пожалуйста, выберите обе даты');
    }
});

// В реальном проекте здесь бы подключались библиотеки для графиков, например Chart.js
// и загружались данные с сервера через API