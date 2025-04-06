from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 1 is an example of a default user id
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.CharField(
    max_length=50,
    choices=[
        ('atom', 'Атом'),
        ('dna', 'ДНК'),
        ('rocket', 'Ракета'),
        ('flask', 'Колба'),
        ('microscope', 'Микроскоп')
    ],
    default='atom'  # Provide a default value (e.g., 'atom' or another valid cover)
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


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
