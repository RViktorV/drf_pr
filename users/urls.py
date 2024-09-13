from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet  # Импортируем ViewSet для пользователей

router = DefaultRouter()
router.register(r"users", UsersViewSet)  # Регистрируем ViewSet для пользователей

urlpatterns = [
    path("", include(router.urls)),  # Подключаем маршруты API для курсов и пользователей
]
