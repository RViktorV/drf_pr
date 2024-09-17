from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("learning.urls", namespace="learning")),  # Подключаем отдельные маршруты для уроков
    path("users/", include("users.urls", namespace="users")),  # Подключаем отдельные маршруты для пользователей
]
