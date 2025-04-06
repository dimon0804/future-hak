from django.shortcuts import render
from dashboard.models import Post
from django.db.models import Q


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



# # Получаем параметры из GET-запроса
# date_filter = request.GET.get('date', '')
# categories = request.GET.getlist('category')  # Список выбранных категорий
# sites = request.GET.getlist('site')  # Список выбранных сайтов

# Начинаем с полного QuerySet (например, все посты)
posts = Post.objects.all()

# # Фильтрация по дате
# if date_filter == 'today':
#     posts = posts.filter(created_at__date=timezone.now().date())
# elif date_filter == 'week':
#     week_ago = timezone.now() - timedelta(days=7)
#     posts = posts.filter(created_at__gte=week_ago)
# elif date_filter == 'month':
#     month_ago = timezone.now() - timedelta(days=30)
#     posts = posts.filter(created_at__gte=month_ago)

# # Фильтрация по категориям
# if categories:
#     # Если выбраны категории, фильтруем по ним
#     posts = posts.filter(category__in=categories)

# # Фильтрация по сайтам (если нужно)
# if sites:
#     # Если выбраны сайты, фильтруем по ним
#     posts = posts.filter(site__in=sites)

# # Результат: отфильтрованный QuerySet
# context = {
#     'posts': posts,
#     'selected_categories': categories,  # Для отображения выбранных категорий в шаблоне
#     'selected_date': date_filter,      # Для отображения выбранной даты в шаблоне
#     'selected_sites': sites,           # Для отображения выбранных сайтов в шаблоне
# }

# # return render(request, 'your_template.html', context)


