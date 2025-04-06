from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from accounts.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model 
import time

def login_view(request):
    if request.user.is_authenticated:
        # return render(request, 'auth/login.html', {'show_success': True})
        return redirect('main')  # Перенаправление, если пользователь уже авторизован

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Используем email для аутентификации
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'auth/login.html', {'show_success': True})
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')  # Перенаправление на домашнюю страницу
        else:
            messages.error(request, 'Неверный email или пароль')

    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


User = get_user_model()

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('home')  # Перенаправление, если пользователь уже авторизован

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Используем email для аутентификации
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Перенаправление на домашнюю страницу
#         else:
#             messages.error(request, 'Неверный email или пароль')

#     return render(request, 'auth/login.html')

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])  # Хешируем пароль
#             user.save()
#             messages.success(request, 'Вы успешно зарегистрированы!')
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'auth/register.html', {'form': form})

def generate_random_password(length=8):
    """Генерация случайного пароля."""
    characters = string.ascii_letters + string.digits + '!@#$%^&*()-=_+[]{}|;:,.<>?'
    return ''.join(random.choice(characters) for i in range(length))

def forgot_password(request):
    """Представление для восстановления пароля."""
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")
            return render(request, 'auth/forgot-password.html')

        # Генерация нового пароля
        new_password = generate_random_password()

        # Сохранение нового пароля в базе данных
        user.set_password(new_password)
        user.save()

        try:
            subject = 'Восстановление пароля'
            message = f'Ваш новый пароль: {new_password}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        except Exception as e:
            messages.error(request, "Ошибка при отправке письма. Попробуйте позже.")
            return render(request, 'auth/forgot-password.html')

        messages.success(request, "Письмо с новым паролем отправлено на вашу почту.")
        return redirect('login')

    return render(request, 'auth/forgot-password.html')
