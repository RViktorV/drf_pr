from rest_framework import viewsets

from users.models import Users, Payment
from users.serializers import UsersSerializer, PaymentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.filters import PaymentFilter

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter

    # Сортировка по дате оплаты
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию сортировка по убыванию даты
