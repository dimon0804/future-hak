from django.shortcuts import render
from dashboard.models import Post

def main(request):
    # Получаем выбранные сайты из GET-параметров
    selected_sites = request.GET.getlist('site')
    
    # Получаем все посты
    posts = Post.objects.filter(status='published')
    
    # Фильтруем по выбранным сайтам
    if selected_sites:
        posts = posts.filter(source_site__in=selected_sites)
    
    # Проверяем роль пользователя
    is_admin = hasattr(request.user, 'role') and request.user.role == 'admin'
    
    # Формируем контекст для шаблона
    context = {
        'posts': posts,
        'user': request.user,
        'is_admin': is_admin,
    }
    return render(request, 'core/main.html', context)
