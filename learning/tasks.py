from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_course_update_email(course_title, user_email):
    print("Hello")
    #subject = f"Обновление курса: {course_title}"
    #message = f"Курс {course_title} был обновлен. Проверьте новые материалы."
    #email_from = settings.DEFAULT_FROM_EMAIL
    #send_mail(subject, message, email_from, [user_email])
