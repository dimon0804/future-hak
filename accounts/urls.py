from django.urls import path
from django.urls import include
from accounts.views import login_view, register_view, forgot_password 

urlpatterns = [
    path('login', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('forgot-password/', forgot_password, name='forgot_password'),
]
