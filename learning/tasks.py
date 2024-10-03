from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription


@shared_task
def send_course_update_email_async(course_id):
    """
    Асинхронная задача для отправки уведомлений о обновлении курса подписчикам.

    Args:
        course_id (int): ID курса, который был обновлен.
    """
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for subscriber in subscribers:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Курс "{course.title}" был обновлен.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.user.email],
        )
