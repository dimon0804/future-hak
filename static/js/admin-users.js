 // Управление модальным окном
 const modal = document.getElementById('userModal');
 const addUserBtn = document.getElementById('addUserBtn');
 const modalClose = document.getElementById('modalClose');
 const cancelBtn = document.getElementById('cancelBtn');
 const modalTitle = document.getElementById('modalTitle');
 const userForm = document.getElementById('userForm');
 
 // Открытие модального окна для добавления
 addUserBtn.addEventListener('click', () => {
     modalTitle.textContent = 'Добавить пользователя';
     userForm.reset();
     modal.style.display = 'flex';
 });
 
 // Закрытие модального окна
 const closeModal = () => {
     modal.style.display = 'none';
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
 userForm.addEventListener('submit', (e) => {
     e.preventDefault();
     // Здесь должна быть логика сохранения пользователя
     alert('Пользователь сохранен!');
     closeModal();
 });
 
 // Обработка кнопок редактирования
 document.querySelectorAll('.action-btn.edit').forEach(btn => {
     btn.addEventListener('click', () => {
         modalTitle.textContent = 'Редактировать пользователя';
         // Здесь должна быть логика загрузки данных пользователя в форму
         modal.style.display = 'flex';
     });
 });
 
 // Обработка кнопок удаления
 document.querySelectorAll('.action-btn.delete').forEach(btn => {
     btn.addEventListener('click', () => {
         if (confirm('Вы уверены, что хотите удалить этого пользователя?')) {
             // Логика удаления пользователя
             btn.closest('tr').remove();
         }
     });
 });
 
 // Пагинация
 document.querySelectorAll('.page-btn').forEach(btn => {
     btn.addEventListener('click', function() {
         document.querySelectorAll('.page-btn').forEach(b => b.classList.remove('active'));
         this.classList.add('active');
         // Здесь должна быть логика загрузки соответствующей страницы
     });
 });