from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import (
    UsersViewSet,
    UsersCreateAPIView,
    PaymentCreateAPIView,
    PaymentStatusAPIView,
    PaymentSuccessAPIView,
    PaymentCancelAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UsersViewSet)  # CRUD для пользователей

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),  # JWT авторизация
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Обновление токена
    path("register/", UsersCreateAPIView.as_view(), name="register"),  # Регистрация
    path("payments/", PaymentCreateAPIView.as_view(), name="payment_create"), # Оплата
    path('payment-success/', PaymentSuccessAPIView.as_view(), name='payment_success'), # Ссылка на оплату
    path('payment-cancel/', PaymentCancelAPIView.as_view(), name='payment_cancel'), # Отмена платежа
    path(
        "payment-status/<str:session_id>/",
        PaymentStatusAPIView.as_view(),
        name="payment_status",
    ),
]
