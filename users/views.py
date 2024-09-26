from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from users.models import Users, Payment
from users.serializers import UsersSerializer, PaymentSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)  # Для разрешения доступа


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]  # Закрываем доступ авторизацией


class UsersCreateAPIView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ для регистрации без авторизации


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        pass
