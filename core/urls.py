from django.urls import path
from django.urls import include
from .views import main
from .scheduler import start

urlpatterns = [
    path('', main, name="main"),
    path('start_scheduler/', start),
      # Добавлено для маршрутизации к профилю
    # path('auth', include('auth.urls')),
]
