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
 // Ожидаем отправку формы
 document.getElementById("userForm").addEventListener("submit", async function(e) {
    e.preventDefault(); // Предотвращаем стандартную отправку формы

    // Данные из формы
    const data = {
        name: document.getElementById("userName").value,
        username: document.getElementById("userUsername").value,
        email: document.getElementById("userEmail").value,
        role: document.getElementById("userRole").value,
        status: document.getElementById("userStatus").value,
        password: document.getElementById("passwordInput").value,
    };

    try {
        // Отправляем данные на сервер
        const response = await fetch("/dashboard/create-user/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")  // CSRF токен для безопасности
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Пользователь успешно добавлен!");
            document.getElementById("userForm").reset();  // Сбрасываем форму
            document.getElementById("userModal").style.display = "none";  // Закрываем модальное окно
        } else {
            alert("Ошибка: " + result.error);
        }
    } catch (error) {
        alert("Ошибка при отправке запроса");
    }
});

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.querySelectorAll('.action-btn.edit').forEach(button => {
button.addEventListener('click', function() {
    const userId = this.getAttribute('data-id');
    const userName = this.getAttribute('data-name');
    const userEmail = this.getAttribute('data-email');
    const userRole = this.getAttribute('data-role');
    const userStatus = this.getAttribute('data-status');
    
    // Заполняем форму данными
    document.getElementById('userId').value = userId;
    document.getElementById('userName').value = userName;
    document.getElementById('userEmail').value = userEmail;
    document.getElementById('userRole').value = userRole;
    document.getElementById('userStatus').value = userStatus;

    // Открываем модальное окно
    document.getElementById('userModal').style.display = 'block';
});
});
document.getElementById('userForm').addEventListener('submit', async function(event) {
event.preventDefault();  // Отменяем стандартное поведение формы

const userId = document.getElementById('userId').value;
const userName = document.getElementById('userName').value;
const userEmail = document.getElementById('userEmail').value;
const userRole = document.getElementById('userRole').value;
const userStatus = document.getElementById('userStatus').value;
const password = document.getElementById('passwordInput').value;  // Новый пароль (если его изменять)

const data = {
    id: userId,
    name: userName,
    email: userEmail,
    role: userRole,
    status: userStatus,
    password: password
};

// Отправляем запрос на сервер
const response = await fetch(`/dashboard/edit-user/`, {  // Здесь указываем путь для обновления данных
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),  // Для защиты от CSRF
    },
    body: JSON.stringify(data)
});

if (response.ok) {
    alert('Пользователь обновлен успешно');
    // Закрываем модальное окно
    document.getElementById('userModal').style.display = 'none';
    location.reload();  // Перезагружаем страницу, чтобы увидеть обновленные данные
} else {
    alert('Ошибка при обновлении пользователя');
}
});