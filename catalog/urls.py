from django.urls import path
from . import views  # Импортируем views из текущего приложения

urlpatterns = [
    path('', views.index, name='index'),  # Добавляем URL-паттерн для главной страницы
]