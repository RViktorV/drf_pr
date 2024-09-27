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

from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_checkout_session,
    retrieve_stripe_session,
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]  # Закрываем доступ авторизацией


class UsersCreateAPIView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ для регистрации без авторизации


class PaymentCreateAPIView(CreateAPIView):
    """APIView для создания платежа и Stripe сессии."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Создает запись о платеже и генерирует сессию Stripe для оплаты."""
        payment = serializer.save(user=self.request.user)

        # Создаем продукт и цену в Stripe
        product_id = create_stripe_product(
            payment.course.title if payment.course else payment.lesson.title
        )
        price_id = create_stripe_price(product_id, int(payment.amount))

        # URL успеха и отмены
        success_url = self.request.build_absolute_uri(reverse("users:payment_success"))
        cancel_url = self.request.build_absolute_uri(reverse("users:payment_cancel"))

        # Создаем сессию Stripe и получаем session_id и session_url
        session_data = create_stripe_checkout_session(price_id, success_url, cancel_url)
        session_url = session_data['url']
        session_id = session_data['id']  # Сохраняем session_id

        # Сохраняем ссылку на оплату и session_id в модели платежа
        payment.link = session_url
        payment.session_id = session_id  # Сохраняем session_id
        payment.save()

        # Возвращаем ссылку на оплату
        return Response({"payment_link": session_url})


class PaymentStatusAPIView(APIView):
    """APIView для получения статуса платежа по session_id."""
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        """Возвращает информацию о сессии Stripe по session_id."""
        session = retrieve_stripe_session(session_id)
        return Response(
            {
                "id": session.id,
                "status": session.payment_status,
                "amount_total": session.amount_total,
                "currency": session.currency,
            }
        )


class PaymentSuccessAPIView(APIView):
    """APIView для обработки успешного завершения платежа."""
    def get(self, request):
        """Обрабатывает GET запрос после успешной оплаты."""
        return Response({"message": "Оплата прошла успешно. Ваш курс теперь доступен."})


class PaymentCancelAPIView(APIView):
    """APIView для обработки отмены платежа."""
    def get(self, request):
        """Обрабатывает GET запрос после отмены платежа."""
        return Response(
            {"message": "Оплата была отменена. Вы можете попробовать еще раз."}
        )
