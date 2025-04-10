# Generated by Django 5.2 on 2025-04-06 10:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('category', models.CharField(choices=[('physics', 'Физика'), ('biology', 'Биология'), ('chemistry', 'Химия'), ('space', 'Космос'), ('technology', 'Технологии')], max_length=50, verbose_name='Категория')),
                ('status', models.CharField(choices=[('published', 'Опубликовано'), ('draft', 'Черновик'), ('moderation', 'На модерации'), ('archived', 'Архив'), ('rejected', 'Отклонено')], default='draft', max_length=50, verbose_name='Статус')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Изображение')),
                ('tags', models.CharField(blank=True, max_length=255, verbose_name='Теги')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержание комментария')),
                ('status', models.CharField(choices=[('published', 'Опубликован'), ('draft', 'Черновик'), ('moderation', 'На модерации'), ('archived', 'Архив'), ('rejected', 'Отклонено')], default='draft', max_length=50, verbose_name='Статус')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dashboard.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['status'], name='dashboard_c_status_d0e143_idx'), models.Index(fields=['created_at'], name='dashboard_c_created_582d0f_idx'), models.Index(fields=['post'], name='dashboard_c_post_id_2e229f_idx')],
            },
        ),
    ]
