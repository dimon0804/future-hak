 // Здесь можно добавить логику для:
        // - Загрузки данных статистики
        // - Управления пользователями и постами
        // - Фильтрации и поиска
        
        // Пример: выделение активной страницы в пагинации
        document.querySelectorAll('.page-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.page-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            });
        });
        
        // Пример: подтверждение удаления
        document.querySelectorAll('.action-btn.delete').forEach(btn => {
            btn.addEventListener('click', function() {
                if (confirm('Вы уверены, что хотите удалить этот элемент?')) {
                    // Логика удаления
                    this.closest('tr').remove();
                }
            });
        });
        document.addEventListener('DOMContentLoaded', function() {
            const modal = document.getElementById('userModal');
            
            // Открытие модалки
            document.querySelectorAll('.edit').forEach(btn => {
                btn.addEventListener('click', function() {
                    const userData = this.dataset;
                    document.getElementById('userId').value = userData.id;
                    document.getElementById('userName').value = userData.name;
                    document.getElementById('userEmail').value = userData.email;
                    document.getElementById('userRole').value = userData.role;
                    document.getElementById('userStatus').value = userData.status;
                    modal.style.display = 'flex'; // Используем flex для центрирования
                });
            });
        
            // Закрытие модалки
            document.getElementById('modalClose').addEventListener('click', () => {
                modal.style.display = 'none';
            });
        
            // Отправка формы
            document.getElementById('userForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const data = {
                    id: document.getElementById('userId').value,
                    name: document.getElementById('userName').value,
                    email: document.getElementById('userEmail').value,
                    role: document.getElementById('userRole').value,
                    status: document.getElementById('userStatus').value,
                };
        
                try {
                    const response = await fetch("{% url 'edit_user_all' %}", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}'
                        },
                        body: JSON.stringify(data)
                    });
        
                    if (response.ok) {
                        alert('Данные сохранены!');
                        location.reload();
                    } else {
                        const errorData = await response.json();
                        alert('Ошибка: ' + (errorData.error || 'Неизвестная ошибка'));
                    }
                } catch (error) {
                    console.error('Ошибка:', error);
                    alert('Сетевая ошибка');
                }
            });
        });
        