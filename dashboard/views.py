from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

User = get_user_model()

def admin_dashboard(request):
    # Получаем 4 последних зарегистрированных пользователя
    recent_users_query = User.objects.order_by('-created_at')[:4]

    recent_users = []
    for user in recent_users_query:
        recent_users.append({
            "avatar": user.name[:1].upper() + user.username[:1].upper(),
            "name": user.name,
            "date": localtime(user.created_at).strftime("%d.%m.%Y"),
            "status": user.is_active,
            "posts": 0,
            "id": user.id,
        })

    # Примерные данные для статистики (в будущем можно автоматизировать)
    stats = {
        "total_users": User.objects.count(),
        "new_posts": 356,
        "comments": 2845,
        "activity": "78%",
    }

    # Демо-данные для постов (ты позже подключишь реальные)
    recent_posts = [
        {"title": "Новые космические технологии", "author": "Иван Иванов", "date": "14.05.2023", "comments": 24, "status": "published"},
        {"title": "Исследование Марса", "author": "Анна Петрова", "date": "12.05.2023", "comments": 18, "status": "published"},
        {"title": "Спутники нового поколения", "author": "Сергей Сидоров", "date": "10.05.2023", "comments": 5, "status": "pending"},
        {"title": "Космический туризм", "author": "Мария Морозова", "date": "08.05.2023", "comments": 32, "status": "published"},
    ]

    context = {
        "stats": stats,
        "recent_users": recent_users,
        "recent_posts": recent_posts,
    }

    return render(request, 'dashboard/admin.html', context)

def delete_user(request, user_id):
    try:
        # Получаем пользователя по ID из URL
        user = get_object_or_404(User, id=user_id)
        user.delete()  # Удаляем пользователя
        messages.success(request, f"Пользователь {user.username} удалён.")
    except Exception as e:
        messages.error(request, f"Произошла ошибка при удалении: {str(e)}")
    return redirect('dashboard')

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Тут можешь отобразить форму редактирования или сразу перенаправить
    return render(request, 'dashboard/edit_user.html', {'user': user})

def admin_users(request):
    email = request.GET.get('email', '')
    status = request.GET.get('status', '')
    role = request.GET.get('role', '')

    # Фильтруем пользователей
    users = User.objects.all()

    if email:
        users = users.filter(email__icontains=email)  # Фильтрация по email
    if status:
        users = users.filter(is_active=status)  # Фильтрация по статусу
    if role:
        users = users.filter(role=role)  # Фильтрация по роли

    # Пагинация
    paginator = Paginator(users, 10)  # Показывать по 10 пользователей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/admin-users.html', {'page_obj': page_obj})
