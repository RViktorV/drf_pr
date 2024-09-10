from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learning.views import CourseViewSet  # Импортируем ViewSet из приложения learning
from users.views import UserViewSet  # Импортируем ViewSet для пользователей

router = DefaultRouter()
router.register(r"courses", CourseViewSet)  # Регистрируем ViewSet для курсов
router.register(r'users', UserViewSet)  # Регистрируем ViewSet для пользователей

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # Подключаем маршруты API для курсов и пользователей
    path("api/", include("learning.urls")),  # Подключаем отдельные маршруты для уроков
]
