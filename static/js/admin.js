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