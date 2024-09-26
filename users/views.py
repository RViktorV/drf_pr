from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from users.models import Users, Payment
from users.serializers import UsersSerializer, PaymentSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)  # Для разрешения доступа

from users.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session, \
    retrieve_stripe_session


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
        payment = serializer.save(users=self.request.user)

        # Создаем продукт и цену в Stripe
        product_id = create_stripe_product(payment.course.title if payment.course else payment.lesson.title)
        price_id = create_stripe_price(product_id, int(payment.amount * 100))

        # URL успеха и отмены
        success_url = self.request.build_absolute_uri(reverse('payment_success'))
        cancel_url = self.request.build_absolute_uri(reverse('payment_cancel'))

        # Создаем сессию Stripe
        session_url = create_stripe_checkout_session(price_id, success_url, cancel_url)

        # Сохраняем ссылку на оплату в модели платежа
        payment.link = session_url
        payment.save()

        # Возвращаем ссылку на оплату
        return Response({"payment_link": session_url})

class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        """Получает информацию о сессии Stripe по session_id."""
        session = retrieve_stripe_session(session_id)
        return Response({
            "id": session.id,
            "status": session.payment_status,
            "amount_total": session.amount_total,
            "currency": session.currency,
        })

class PaymentSuccessAPIView(APIView):
    def get(self, request):
        return Response({
            "message": "Оплата прошла успешно. Ваш курс теперь доступен."
        })

class PaymentCancelAPIView(APIView):
    def get(self, request):
        return Response({
            "message": "Оплата была отменена. Вы можете попробовать еще раз."
        })

