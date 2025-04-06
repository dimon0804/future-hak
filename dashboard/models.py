from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('physics', 'Физика'),
        ('biology', 'Биология'),
        ('chemistry', 'Химия'),
        ('space', 'Космос'),
        ('technology', 'Технологии'),
    ]
    
    STATUS_CHOICES = [
        ('published', 'Опубликовано'),
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('archived', 'Архив'),
        ('rejected', 'Отклонено'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение')
    tags = models.CharField(max_length=255, blank=True, verbose_name='Теги')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']



class Comment(models.Model):
    # Статусы комментариев (аналогично вашим статусам постов)
    STATUS_CHOICES = [
        ('published', 'Опубликован'),
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('archived', 'Архив'),
        ('rejected', 'Отклонено'),
    ]
    
    # Основные поля (как у Post)
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    content = models.TextField(verbose_name='Содержание комментария')
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['post']),
        ]
