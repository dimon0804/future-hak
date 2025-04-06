 // Управление модальным окном
 const modal = document.getElementById('tagModal');
 const addTagBtn = document.getElementById('addTagBtn');
 const modalClose = document.getElementById('modalClose');
 const cancelBtn = document.getElementById('cancelBtn');
 const modalTitle = document.getElementById('modalTitle');
 const tagForm = document.getElementById('tagForm');
 const colorPreview = document.getElementById('colorPreview');
 const tagColorInput = document.getElementById('tagColor');
 const tagTextColorInput = document.getElementById('tagTextColor');
 
 // Открытие модального окна для добавления
 addTagBtn.addEventListener('click', () => {
     modalTitle.textContent = 'Добавить тег';
     tagForm.reset();
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
 
 // Выбор цвета
 document.querySelectorAll('.color-option').forEach(option => {
     option.addEventListener('click', function() {
         document.querySelectorAll('.color-option').forEach(opt => {
             opt.classList.remove('selected');
         });
         this.classList.add('selected');
         const bgColor = this.getAttribute('data-color');
         const textColor = this.getAttribute('data-text');
         colorPreview.style.background = bgColor;
         tagColorInput.value = bgColor;
         tagTextColorInput.value = textColor;
     });
 });
 
 // Обработка отправки формы
 tagForm.addEventListener('submit', (e) => {
     e.preventDefault();
     // Здесь должна быть логика сохранения тега
     alert('Тег сохранен!');
     closeModal();
 });
 
 // Обработка кнопок редактирования
 document.querySelectorAll('.action-btn.edit').forEach(btn => {
     btn.addEventListener('click', () => {
         modalTitle.textContent = 'Редактировать тег';
         // Здесь должна быть логика загрузки данных тега в форму
         modal.style.display = 'flex';
     });
 });
 
 // Обработка кнопок удаления
 document.querySelectorAll('.action-btn.delete').forEach(btn => {
     btn.addEventListener('click', () => {
         if (confirm('Вы уверены, что хотите удалить этот тег?')) {
             // Логика удаления тега
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