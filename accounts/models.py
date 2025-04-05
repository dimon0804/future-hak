from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, role='user'):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password):
        user = self.create_user(username, email, name, password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

STATUS_CHOICES = [
    ('active', 'Активен'),
    ('banned', 'Заблокирован'),
    ('pending', 'Ожидает подтверждения'),
]
USER_ROLES = [
        ('user', 'Пользователь'),
        ('expert', 'Эксперт'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='user') 
    is_active = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Для аутентификации используется email
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email
