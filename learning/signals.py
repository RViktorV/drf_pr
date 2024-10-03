# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from datetime import timedelta
# from .models import Course, Lesson
# from .tasks import send_course_update_email
#
# @receiver(post_save, sender=Course)
# def send_course_update_email_signal(sender, instance, **kwargs):
#     """
#     Обработчик сигнала, который запускает асинхронную задачу для отправки уведомления по электронной почте.
#     когда экземпляр «Курса» обновляется и не обновлялся в течение последних 4 часов.
#
#     Аргументы:
#         отправитель: класс модели (курс), отправивший сигнал.
#         экземпляр: экземпляр модели (курса), который был сохранен.
#         **kwargs: дополнительные аргументы ключевого слова.
#     """
#     # Проверьте, не прошло ли более 4 часов с момента последнего обновления курса.
#     if timezone.now() - instance.updated_at > timedelta(seconds=2):
#         # Запланируйте асинхронную задачу для отправки электронного письма с обновлением курса.
#         send_course_update_email.delay(instance.id)
#
# @receiver(post_save, sender=Lesson)
# def send_lesson_update_email_signal(sender, instance, **kwargs):
#     """
#     Обработчик сигнала, который запускает асинхронную задачу для отправки уведомления по электронной почте.
#     когда экземпляр «Урока», связанный с «Курсом», обновляется, а сам курс
#     не обновлялось последние 4 часа.
#
#     Аргументы:
#         отправитель: класс модели (урок), отправивший сигнал.
#         экземпляр: экземпляр модели (урока), который был сохранен.
#         **kwargs: дополнительные аргументы ключевого слова.
#     """
#     # Проверьте, прошло ли более 4 часов с момента последнего обновления соответствующего курса.
#     if timezone.now() - instance.course.updated_at > timedelta(seconds=2):
#         # Запланируйте асинхронную задачу для отправки электронного письма с обновлением курса.
#         send_course_update_email.delay(instance.course.id)