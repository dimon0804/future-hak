from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.timezone import now, timedelta
from accounts.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.http import HttpResponse
from accounts.models import CustomUser
from .models import Comment

from .forms import PostForm

User = get_user_model()

def admin_dashboard(request):
    # Последние 4 пользователя
    recent_users_query = User.objects.order_by('-created_at')[:4]

    recent_users = []
    for user in recent_users_query:
        user_post_count = Post.objects.filter(author=user).count()
        recent_users.append({
            "avatar": user.name[:1].upper() + user.username[:1].upper(),
            "name": user.name,
            "email": user.email,
            "date": localtime(user.created_at).strftime("%d.%m.%Y"),
            "status": user.is_active,
            "posts": user_post_count,
            "id": user.id,
        })

    # Временной диапазон для анализа за неделю
    week_ago = now() - timedelta(days=7)

    # Подсчёты
    new_users_this_week = User.objects.filter(created_at__gte=week_ago).count()
    new_posts_this_week = Post.objects.filter(created_at__gte=week_ago).count()
    new_comments_this_week = Comment.objects.filter(created_at__gte=week_ago).count()
    total_comments = Comment.objects.count()

    # Сводная статистика
    stats = {
        "total_users": User.objects.count(),
        "new_users_week": new_users_this_week,
        "new_posts": new_posts_this_week,
        "comments": total_comments,
        "new_comments": new_comments_this_week,
        "activity": "78%",  # Пока демо
    }

    # Последние посты с количеством опубликованных комментариев
    recent_posts_query = Post.objects.select_related('author').order_by('-created_at')[:4]
    recent_posts = []
    for post in recent_posts_query:
        comments_count = Comment.objects.filter(post=post, status='published').count()
        recent_posts.append({
            "title": post.title,
            "author": post.author.name,
            "date": localtime(post.created_at).strftime("%d.%m.%Y"),
            "comments": comments_count,
            "status": post.status,
        })

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


from openpyxl import Workbook

def export_users_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'

    # Создаем книгу Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Пользователи"

    # Заголовки
    ws.append(['ID', 'Имя', 'Email', 'Роль', 'Статус', 'Дата регистрации'])

    # Данные
    users = CustomUser.objects.all()
    for user in users:
        ws.append([
            user.id,
            user.name,
            user.email,
            user.role,
            'Активен' if user.is_active else 'Неактивен',
            user.created_at.strftime('%d.%m.%Y')
        ])

    # Сохраняем книгу в HTTP-ответ
    wb.save(response)
    return response


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:
            # Получаем данные из запроса
            data = json.loads(request.body)
            name = data.get("name")
            username = data.get("username")
            email = data.get("email")
            role = data.get("role")
            status = data.get("status")
            password = data.get("password")

            # Создаём пользователя в базе данных
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                name=name,
                password=password,
                role=role,
            )

            # Устанавливаем статус и сохраняем
            user.is_active = status
            user.save()

            return JsonResponse({"message": "Пользователь успешно создан!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Неверный запрос"}, status=400)

@csrf_exempt  # Для обработки POST-запроса
def edit_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        role = data.get('role')
        status = data.get('status')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(id=user_id)
            user.name = name
            user.email = email
            user.role = role
            user.is_active = status
            if password:  # Если пароль указан, обновляем его
                user.set_password(password)
            user.save()

            return JsonResponse({'message': 'Пользователь успешно обновлен'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)



def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # Обработка отправленных данных
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.is_active = request.POST.get('status') == 'active'
        user.save()
        messages.success(request, 'Пользователь успешно обновлен!')
        return redirect('admin_users')  # Перенаправление на страницу пользователей

    context = {
        'user': user,
    }
    return render(request, 'admin/admin_edit_user.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Post
import csv
from django.shortcuts import render
from .models import Post
from accounts.models import CustomUser
from django.core.paginator import Paginator

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Фильтрация
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    if status_filter:
        posts = posts.filter(status=status_filter)
    if category_filter:
        posts = posts.filter(category=category_filter)
    
    # Пагинация
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем всех пользователей для подстановки в форму
    users = CustomUser.objects.all()

    return render(request, 'dashboard/admin-posts.html', {'posts': page_obj, 'users': users})

from django.core.files.storage import FileSystemStorage

def post_create(request):
    if request.method == 'POST':
        print("ghb")
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        category = request.POST.get('category')
        status = request.POST.get('status')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        
        # Обработка файла изображения
        image = request.FILES.get('image')
        if image:
            # Генерируем уникальное имя файла с сохранением расширения
            ext = os.path.splitext(image.name)[1]  # получаем расширение (например, .jpg)
            filename = f"{uuid.uuid4().hex}{ext}"  # создаем уникальное имя

            # Путь внутри static
            upload_path = f"static/images/{filename}"

            # Сохраняем файл
            fs = FileSystemStorage()
            fs.save(upload_path, image)

            image_url = upload_path
        else:
            image_url = ""
        
        # Получаем автора по ID
        author = CustomUser.objects.get(id=author_id)
        
        # Создаем новый пост
        new_post = Post.objects.create(
            title=title,
            author=author,
            category=category,
            status=status,
            content=content,
            tags=tags,
            image=image_url
        )
        
        return redirect('admin-posts')  # Перенаправляем на страницу списка постов (или куда тебе нужно)

    # В случае, если это GET-запрос (например, чтобы показать форму), возвращаем страницу с формой
    users = CustomUser.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/admin-posts.html', {'posts': page_obj, 'users': users})

def export_posts(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Author', 'Category', 'Status', 'Date', 'Views'])
    
    for post in Post.objects.all():
        writer.writerow([
            post.id,
            post.title,
            post.author.name,
            post.get_category_display(),
            post.get_status_display(),
            post.created_at.strftime("%d.%m.%Y"),
            post.views
        ])
    
    response['Content-Disposition'] = 'attachment; filename="posts_export.csv"'
    return response

@csrf_exempt
def edit_user_all(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = CustomUser.objects.get(id=data['id'])
            
            # Обновляем ВСЕ поля явно
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)  # Добавлено
            user.role = data.get('role', user.role)     # Добавлено
            user.is_active = (data.get('status', 'active') == 'active')  # Исправлено
            
            user.save()  # Важно: сохраняем изменения
            
            return JsonResponse({'message': 'Данные обновлены!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
    # return JsonResponse({'error': 'Метод не разрешен'}, status=405)

def admin_analytics(request):
    # Здесь будет логика для отображения аналитики
    return render(request, 'dashboard/admin-analytics.html')

#обработчик для постов 

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Post
from .forms import PostForm
import csv
import os
import uuid
from django.core.files.storage import FileSystemStorage

def post_edit(request, post_id):
    # Получаем пост для редактирования
    post = get_object_or_404(Post, id=post_id)
    users = CustomUser.objects.all()  # Получаем всех пользователей для выпадающего списка авторов
    
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        category = request.POST.get('category')
        status = request.POST.get('status')
        content = request.POST.get('content')
        tags = request.POST.get('tags')

        # Обработка файла изображения (если есть)
        image = request.FILES.get('image')
        if image:
            # Генерируем уникальное имя файла с сохранением расширения
            ext = os.path.splitext(image.name)[1]  # получаем расширение (например, .jpg)
            filename = f"{uuid.uuid4().hex}{ext}"  # создаем уникальное имя

            # Путь внутри static
            upload_path = f"static/images/{filename}"

            # Сохраняем файл
            fs = FileSystemStorage()
            fs.save(upload_path, image)

            image_url = upload_path
        else:
            image_url = post.image # Если изображения нет, оставляем старое

        # Получаем пользователя-автора
        try:
            author = CustomUser.objects.get(id=author_id)
        except CustomUser.DoesNotExist:
            return HttpResponse("Автор не найден", status=400)

        # Обновляем данные поста
        post.title = title
        post.author = author
        post.category = category
        post.status = status
        post.content = content
        post.tags = tags
        post.image = image_url
        post.save()

        return redirect('admin-posts')  # После сохранения перенаправляем на список постов
    
    return render(request, 'dashboard/edit_post.html', {'post': post, 'users': users})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return JsonResponse({'success': True})


def export_posts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=posts.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Название', 'Автор', 'Категория', 'Статус', 'Дата', 'Просмотры'])

    for post in Post.objects.all():
        writer.writerow([post.id, post.title, post.author.name, post.get_category_display(),
                         post.get_status_display(), post.created_at.strftime('%d.%m.%Y'), post.views])

    return response

def comment_list(request):
    comments = Comment.objects.all()

    # Фильтрация по статусу
    status = request.GET.get('status', '')
    if status:
        comments = comments.filter(status=status)

    # Фильтрация по посту
    post_id = request.GET.get('post', '')
    if post_id:
        comments = comments.filter(post__id=post_id)

    # Поиск только по содержанию
    search_query = request.GET.get('search', '')
    if search_query:
        comments = comments.filter(content__icontains=search_query)

    posts = Post.objects.all()  # Для фильтра по постам в шаблоне
    context = {
        'comments': comments,
        'posts': posts,
        'status': status,
        'post_id': post_id,
        'search_query': search_query,
    }
    return render(request, 'dashboard/admin-comments.html', context)



def comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = 'published'
    comment.save()
    return redirect('comment_list')

def comment_reject(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = 'deleted'
    comment.save()
    return redirect('comment_list')

def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, 'dashboard/comment_detail.html', {'comment': comment})

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Post  # Убедитесь, что импортировали Category

def filter_posts(request):
    posts = Post.objects.all()
    date_filter = request.GET.get('date', '')
    categories = request.GET.getlist('category')
    sites = request.GET.getlist('site')
    
    # Фильтрация по дате
    if date_filter:
        today = timezone.now().date()
        if date_filter == 'today':
            posts = posts.filter(created_at__date=today)
        elif date_filter == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            posts = posts.filter(created_at__date__gte=start_of_week)
        elif date_filter == 'month':
            start_of_month = today.replace(day=1)
            posts = posts.filter(created_at__date__gte=start_of_month)
    
    # Фильтрация по категориям
    if categories:
        posts = posts.filter(category=categories)
    
    # Фильтрация по сайтам
    if sites:
        posts = posts.filter(site=sites)  # Предполагаем поле site в модели Post
    
    context = {
        'posts': posts,
        'selected_date': date_filter,
        'selected_categories': categories,
        'selected_sites': sites,
        'categories': Category.objects.all(),  # Раскомментируйте, если используете
    }
    return render(request, 'your_template.html', context)