# backends.py

from django.contrib.auth.backends import ModelBackend
from accounts.models import CustomUser  # Импортируем кастомную модель

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)  # Поиск пользователя по email
            if user.check_password(password):  # Проверка пароля
                return user
        except CustomUser.DoesNotExist:
            return None
