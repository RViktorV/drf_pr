from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import Users  # Убедитесь, что используете правильный путь к вашей модели


@shared_task
def block_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)

    # Ищем всех пользователей, которые не заходили более месяца и активны
    inactive_users = Users.objects.filter(last_login__lt=one_month_ago, is_active=True)

    # Блокируем каждого пользователя
    for user in inactive_users:
        user.is_active = False
        user.save()

    return f'Блокировано пользователей: {inactive_users.count()}'
