 // Обработка загрузки изображения
 const postImage = document.getElementById('postImage');
 const previewContainer = document.getElementById('previewContainer');
 const previewImage = document.getElementById('previewImage');
 const removeImage = document.getElementById('removeImage');
 
 postImage.addEventListener('change', function(e) {
     const file = e.target.files[0];
     if (file) {
         const reader = new FileReader();
         reader.onload = function(event) {
             previewImage.src = event.target.result;
             previewContainer.style.display = 'block';
         }
         reader.readAsDataURL(file);
     }
 });
 
 removeImage.addEventListener('click', function() {
     postImage.value = '';
     previewContainer.style.display = 'none';
 });
 
 // Обработка тегов
 const postTags = document.getElementById('postTags');
 const tagsContainer = document.getElementById('tagsContainer');
 
 postTags.addEventListener('keydown', function(e) {
     if (e.key === 'Enter' || e.key === ',') {
         e.preventDefault();
         addTag(this.value.trim());
         this.value = '';
     }
 });
 
 function addTag(tagText) {
     if (tagText && !tagsContainer.querySelector(`[data-tag="${tagText}"]`)) {
         const tag = document.createElement('div');
         tag.className = 'tag';
         tag.dataset.tag = tagText;
         tag.innerHTML = `
             ${tagText}
             <span class="tag-remove" onclick="removeTag('${tagText}')">&times;</span>
         `;
         tagsContainer.appendChild(tag);
     }
 }
 
 window.removeTag = function(tagText) {
     const tag = tagsContainer.querySelector(`[data-tag="${tagText}"]`);
     if (tag) {
         tag.remove();
     }
 };
 
 // Обработка отправки формы
 const postForm = document.getElementById('postForm');
const successMessage = document.getElementById('successMessage');

postForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(postForm);

    fetch(postForm.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (response.ok) {
            postForm.style.display = 'none';
            successMessage.style.display = 'block';
            setTimeout(() => {
                window.location.href = "/"; // или {% url 'main' %}, если рендерить прямо в шаблоне
            }, 3000);
        } else {
            return response.text().then(text => {
                console.error("Ошибка сервера:", text);
                alert("Ошибка при отправке поста.");
            });
        }
    })
    .catch(error => {
        console.error("Ошибка запроса:", error);
        alert("Произошла ошибка. Попробуйте позже.");
    });

     
     // Здесь должна быть логика отправки данных на сервер
     
     // Анимация успешной отправки
     postForm.style.display = 'none';
     successMessage.style.display = 'block';
     
     // Перенаправление через 3 секунды
     setTimeout(() => {
         window.location.href = "{% url 'main' %}"; // Замените на нужный URL
     }, 3000);
 });