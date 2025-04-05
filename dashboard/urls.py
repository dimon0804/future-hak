from django.urls import path
from django.urls import include
from dashboard.views import admin_dashboard, delete_user, edit_user, admin_users

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('admin-users', admin_users, name='admin_users'),
    path('admin-posts', admin_dashboard, name='admin_posts'),
    path('admin-comments', admin_dashboard, name='admin_comments'),
    path('admin-analytics', admin_dashboard, name='admin_analytics'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),

]
