// Управление модальным окном
const modal = document.getElementById('playlistModal');
const createBtn = document.getElementById('createPlaylistBtn');
const closeBtn = document.getElementById('modalClose');
const cancelBtn = document.getElementById('cancelBtn');

// Открытие модального окна
createBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
});

// Закрытие модального окна
const closeModal = () => {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
};

closeBtn.addEventListener('click', closeModal);
cancelBtn.addEventListener('click', closeModal);

// Закрытие при клике вне модального окна
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Обработка отправки формы
document.getElementById('playlistForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Плейлист успешно создан!');
    closeModal();
    // Здесь будет логика создания плейлиста
});

// Обработка кнопок "Поделиться"
document.querySelectorAll('.action-btn.share').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        alert('Функция "Поделиться" будет реализована позже');
        // Здесь будет логика для кнопки "Поделиться"
    });
});