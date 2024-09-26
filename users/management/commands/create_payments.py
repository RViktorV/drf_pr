from django.core.management.base import BaseCommand
from users.models import Payment, Users
from learning.models import Course, Lesson


class Command(BaseCommand):
    """
    Команда для создания тестовых данных для платежей.

    Создает два платежа:
    1. Платеж за курс на сумму 1000.00 с методом оплаты "cash".
    2. Платеж за урок на сумму 500.00 с методом оплаты "bank_transfer".

    В случае успеха выводит сообщение "Данные успешно созданы!".
    """

    help = "Создание тестовых данных для платежей"

    def handle(self, *args, **kwargs):
        """
        Основной метод для выполнения команды.

        - Получает первого пользователя из базы данных.
        - Получает первый курс и первый урок.
        - Создает два платежа: один за курс и один за урок.
        - Выводит сообщение о создании данных в случае успешного выполнения.
        """
        # Получаем первого пользователя
        user = Users.objects.first()

        # Получаем первый курс
        course = Course.objects.first()

        # Получаем первый урок
        lesson = Lesson.objects.first()

        # Создаем платеж за курс
        Payment.objects.create(
            user=user, course=course, amount=1000.00, payment_method="cash"
        )

        # Создаем платеж за урок
        Payment.objects.create(
            user=user, lesson=lesson, amount=500.00, payment_method="bank_transfer"
        )

        # Выводим сообщение о успешном создании данных
        self.stdout.write(self.style.SUCCESS("Данные успешно созданы!"))
