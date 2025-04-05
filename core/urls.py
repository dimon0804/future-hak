from django.urls import path
from django.urls import include
from .views import home

urlpatterns = [
    path('', home, name="home"),
    # path('auth', include('auth.urls')),
]
