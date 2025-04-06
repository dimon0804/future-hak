from django.urls import path
from django.urls import include
from dashboard.views import admin_dashboard, delete_user, admin_users, export_users_excel, create_user, edit_user, edit_user_all,comment_list, admin_analytics, post_list
from . import views

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('admin-users', admin_users, name='admin_users'),
    path('admin-posts', post_list, name='admin-posts'),
    path('admin-comments', comment_list, name='admin-comments'),
    path('admin-analytics', admin_analytics, name='admin-analytics'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('admin-users/export/', export_users_excel, name='export_users'),
    path("create-user/", create_user, name="create_user"),
    path('edit-user/', edit_user, name='edit_user'),
    path('admin-users/edit/<int:user_id>/', views.update_user, name='admin_edit_user'),
    # path('admin-users/delete/<int:user_id>/', views.admin_delete_users, name='admin_delete_user'),
    path('admin-posts/', views.post_list, name='admin_posts'),  # Исправлено
    path('create-post/', views.post_create, name='create-post'),
    path('edit-user-all/', edit_user_all, name='edit_user_all'),
    # path('admin/posts/', views.admin_posts, name='admin_posts'),
    # path('admin/posts/add/', views.add_post, name='add_post'),
    # path('edit/<int:post_id>/', views.edit_posts, name='edit_posts'),
    # path('admin/posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('admin/posts/export/', views.export_posts, name='export_posts'),
    path('comments/', views.comment_list, name='comment_list'), 
    path('edit_post/', views.post_edit, name='edit-post'),
    path('posts/', views.filter_posts, name='filter_posts'),
]
