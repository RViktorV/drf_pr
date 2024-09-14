from django.core.management.base import BaseCommand
from users.models import Payment
from users.models import Users
from learning.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создание тестовых данных для платежей'

    def handle(self, *args, **kwargs):
        user = Users.objects.first()  # Получаем первого пользователя
        course = Course.objects.first()  # Получаем первый курс
        lesson = Lesson.objects.first()  # Получаем первый урок

        Payment.objects.create(
            user=user, course=course, amount=1000.00, payment_method='cash'
        )
        Payment.objects.create(
            user=user, lesson=lesson, amount=500.00, payment_method='bank_transfer'
        )
        self.stdout.write(self.style.SUCCESS('Данные успешно созданы!'))
