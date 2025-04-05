 // Управление модальным окном
 const modal = document.getElementById('postModal');
 const addPostBtn = document.getElementById('addPostBtn');
 const modalClose = document.getElementById('modalClose');
 const cancelBtn = document.getElementById('cancelBtn');
 const modalTitle = document.getElementById('modalTitle');
 const postForm = document.getElementById('postForm');
 
 // Открытие модального окна для добавления
 addPostBtn.addEventListener('click', () => {
     modalTitle.textContent = 'Добавить пост';
     postForm.reset();
     modal.style.display = 'flex';
     document.body.style.overflow = 'hidden';
 });
 
 // Закрытие модального окна
 const closeModal = () => {
     modal.style.display = 'none';
     document.body.style.overflow = 'auto';
 };
 
 modalClose.addEventListener('click', closeModal);
 cancelBtn.addEventListener('click', closeModal);
 
 // Закрытие при клике вне модального окна
 modal.addEventListener('click', (e) => {
     if (e.target === modal) {
         closeModal();
     }
 });
 
 // Обработка отправки формы
 postForm.addEventListener('submit', (e) => {
     e.preventDefault();
     // Здесь должна быть логика сохранения поста
     alert('Пост сохранен!');
     closeModal();
 });
 
 // Обработка кнопок редактирования
 document.querySelectorAll('.action-btn.edit').forEach(btn => {
     btn.addEventListener('click', () => {
         modalTitle.textContent = 'Редактировать пост';
         // Здесь должна быть логика загрузки данных поста в форму
         modal.style.display = 'flex';
         document.body.style.overflow = 'hidden';
     });
 });
 
 // Обработка кнопок удаления
 document.querySelectorAll('.action-btn.delete').forEach(btn => {
     btn.addEventListener('click', () => {
         if (confirm('Вы уверены, что хотите удалить этот пост?')) {
             // Логика удаления поста
             btn.closest('tr').style.animation = 'fadeIn 0.3s reverse';
             setTimeout(() => {
                 btn.closest('tr').remove();
             }, 300);
         }
     });
 });

 // Обработка кнопок просмотра
 document.querySelectorAll('.action-btn.view').forEach(btn => {
     btn.addEventListener('click', () => {
         // Логика просмотра поста
         alert('Просмотр поста (откроется в новой вкладке)');
     });
 });
 
 // Пагинация
 document.querySelectorAll('.page-btn').forEach(btn => {
     btn.addEventListener('click', function() {
         document.querySelectorAll('.page-btn').forEach(b => b.classList.remove('active'));
         this.classList.add('active');
         // Здесь должна быть логика загрузки соответствующей страницы
         
         // Анимация загрузки новых данных
         const tableBody = document.querySelector('tbody');
         tableBody.style.opacity = '0.5';
         tableBody.style.transition = 'opacity 0.3s';
         
         setTimeout(() => {
             // Здесь должна быть загрузка новых данных
             tableBody.style.opacity = '1';
         }, 300);
     });
 });

 // Поиск по таблице
 const searchInput = document.querySelector('.search-input');
 searchInput.addEventListener('input', function() {
     const searchTerm = this.value.toLowerCase();
     const rows = document.querySelectorAll('tbody tr');
     
     rows.forEach(row => {
         const text = row.textContent.toLowerCase();
         if (text.includes(searchTerm)) {
             row.style.display = '';
             row.style.animation = 'fadeIn 0.3s';
         } else {
             row.style.display = 'none';
         }
     });
 });

 // Фильтрация по статусу и категории
 const filterSelects = document.querySelectorAll('.filter-select');
 filterSelects.forEach(select => {
     select.addEventListener('change', function() {
         const statusFilter = document.querySelectorAll('.filter-select')[0].value;
         const categoryFilter = document.querySelectorAll('.filter-select')[1].value;
         const rows = document.querySelectorAll('tbody tr');
         
         rows.forEach(row => {
             const status = row.querySelector('.status-badge').textContent.toLowerCase();
             const category = row.querySelector('.category-badge').textContent.toLowerCase();
             
             const statusMatch = !statusFilter || status.includes(statusFilter);
             const categoryMatch = !categoryFilter || category.includes(categoryFilter);
             
             if (statusMatch && categoryMatch) {
                 row.style.display = '';
                 row.style.animation = 'fadeIn 0.3s';
             } else {
                 row.style.display = 'none';
             }
         });
     });
 });