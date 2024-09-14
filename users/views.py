from rest_framework import viewsets

from users.models import Users, Payment
from users.serializers import UsersSerializer, PaymentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.filters import PaymentFilter


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.

    - Осуществляет CRUD операции для модели Users.
    - Использует UsersSerializer для сериализации данных.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с платежами.

    - Осуществляет CRUD операции для модели Payment.
    - Реализует фильтрацию по курсу, уроку и способу оплаты с помощью PaymentFilter.
    - Поддерживает сортировку по дате оплаты.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter

    # Сортировка по дате оплаты
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # По умолчанию сортировка по убыванию даты
