from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from dashboard.models import Post, Comment
from django.contrib.auth.models import User
from accounts.models import CustomUser
from .models import Playlist, PlaylistArticle
from django.http import JsonResponse
from .forms import PlaylistForm

# Create your views here.
def my_profile(request):
    user = request.user  # Получаем текущего авторизованного пользователя
    posts = Post.objects.filter(author=user)  # Все посты пользователя
    comments = Comment.objects.filter(author=user)  # Все комментарии пользователя
    # Передаем данные в контекст шаблона
    context = {
        'user': user,
        'posts': posts,
        'comments': comments,
    }
    
    return render(request, 'user/profile.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'auth/login.html')

def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        # status = request.POST.get('status')
        image = request.FILES.get('image')
        author = request.user
    
        new_post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            tags=tags,
            status="moderation",
            image=image,
            author=author
        )
        return redirect('main')
    context = {
        'user': request.user,
    }
    return render(request, 'user/redact.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        print(request.POST)
        content = request.POST.get('content')
        author = request.user
        new_comment = Comment.objects.create(
            content=content,
            author=author,
            post=post
        )
        return redirect('post_detail', post_id=post.id)
    
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'user/comment.html', context)

def author_profile(request, author_id):
    # Получаем пользователя по его ID или возвращаем 404 ошибку
    author = get_object_or_404(CustomUser, id=author_id)

    # Получаем все посты автора
    posts = Post.objects.filter(author=author).order_by('-created_at')

    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'user/post.html', context)

def list_place(request):
    # Получаем все плейлисты текущего пользователя, используя правильное имя поля
    playlists = Playlist.objects.filter(user_id=request.user.id)

    playlist_data = []
    
    # Для каждого плейлиста, получаем статьи, привязанные к нему
    for playlist in playlists:
        articles = PlaylistArticle.objects.filter(playlist_id=playlist.id)
        article_list = []
        
        for playlist_article in articles:
            try:
                article = Post.objects.get(id=playlist_article.article_id)
                article_list.append(article)
            except Post.DoesNotExist:
                continue
        
        playlist_data.append({
            'playlist': playlist,
            'articles': article_list
        })
    
    # Передаем плейлисты и статьи в контекст
    return render(request, 'user/place.html', {'playlist_data': playlist_data})


def create_playlist(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            # Устанавливаем пользователя
            playlist = form.save(commit=False)
            playlist.user = request.user  # Устанавливаем пользователя как текущего
            playlist.save()

            # Проверка на AJAX-запрос
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Плейлист успешно создан',
                    'playlist_id': playlist.id,
                    'playlist_title': playlist.title,
                })

            # Перенаправляем на страницу с плейлистами
            return redirect('main')

    return JsonResponse({'status': 'error', 'message': 'Ошибка при создании плейлиста'}, status=400)

def post_list(request, place_id):
    return render(request, 'user/list-place.html')
