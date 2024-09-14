from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import (
    UsersViewSet,
    PaymentViewSet,
)  # Импортируем ViewSet для пользователей и платежей


router = DefaultRouter()
router.register(r"users", UsersViewSet)  # Регистрируем ViewSet для пользователей
router.register(r"payments", PaymentViewSet)  # Регистрируем ViewSet для платежей

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # Подключаем маршруты API для курсов и пользователей
]
