from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Playlist(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID плейлиста')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Краткое описание')
    cover_image = models.ImageField(upload_to='playlists/covers/', blank=True, null=True, verbose_name='Обложка')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'
        ordering = ['-created_at']


class PlaylistArticle(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID записи')
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='articles', verbose_name='Плейлист')
    article_id = models.PositiveIntegerField(verbose_name='ID статьи')  # Assuming you want to store the ID of the article
    user_id = models.PositiveIntegerField(verbose_name='ID пользователя')  # Assuming you want to store the ID of the user who added the article

    def __str__(self):
        return f"{self.playlist_id.title} - {self.article_id}"

    class Meta:
        verbose_name = 'Статья в плейлисте'
        verbose_name_plural = 'Статьи в плейлистах'
        ordering = ['playlist_id', 'article_id']
