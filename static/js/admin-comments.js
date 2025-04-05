 // Модальное окно для просмотра комментария
 const modal = document.getElementById('commentModal');
 const approveBtn = document.getElementById('approveBtn');
 const rejectBtn = document.getElementById('rejectBtn');
 
 function viewComment(commentId) {
     // Здесь должна быть логика загрузки данных комментария
     // Для примера используем статические данные
     document.getElementById('commentId').textContent = commentId;
     
     // В реальном проекте здесь бы был запрос к API для получения данных комментария
     // и заполнение полей модального окна
     
     modal.style.display = 'flex';
 }
 
 function closeModal() {
     modal.style.display = 'none';
 }
 
 // Закрытие при клике вне модального окна
 modal.addEventListener('click', (e) => {
     if (e.target === modal) {
         closeModal();
     }
 });
 
 // Обработка действий с комментарием
 approveBtn.addEventListener('click', function() {
     if (confirm('Одобрить этот комментарий?')) {
         // Логика одобрения комментария
         alert('Комментарий одобрен!');
         closeModal();
     }
 });
 
 rejectBtn.addEventListener('click', function() {
     if (confirm('Удалить этот комментарий?')) {
         // Логика удаления комментария
         alert('Комментарий удалён!');
         closeModal();
     }
 });
 
 // Пагинация
 document.querySelectorAll('.page-btn').forEach(btn => {
     btn.addEventListener('click', function() {
         document.querySelectorAll('.page-btn').forEach(b => b.classList.remove('active'));
         this.classList.add('active');
         // Здесь должна быть логика загрузки соответствующей страницы
     });
 });
 
 // Фильтрация
 document.querySelectorAll('.filter-select').forEach(select => {
     select.addEventListener('change', function() {
         // Логика применения фильтров
         console.log('Фильтр изменён:', this.value);
     });
 });
 
 // Поиск
 document.querySelector('.search-input').addEventListener('input', function(e) {
     // Логика поиска (можно добавить debounce для оптимизации)
     console.log('Поиск:', e.target.value);
 });