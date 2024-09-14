from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import (
    UsersViewSet,
    PaymentViewSet,
)  # Импортируем ViewSet для пользователей и платежей

# Создаем роутер для автоматической генерации маршрутов для ViewSet'ов
router = DefaultRouter()

# Регистрируем ViewSet для пользователей
router.register(r"users", UsersViewSet)

# Регистрируем ViewSet для платежей
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # Подключаем маршруты, сгенерированные роутером, для API
]
