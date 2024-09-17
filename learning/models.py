from django.db import models
from django.conf import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Название курса", help_text="Название курса"
    )
    preview = models.ImageField(upload_to="course_previews/")
    description = models.TextField(
        **NULLABLE, verbose_name="Описание курса", help_text="Описание курса"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(
        **NULLABLE, verbose_name="Описание урока", help_text=" Укажите описание урока"
    )
    preview = models.ImageField(upload_to="lesson_previews/")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    video_url = models.URLField()

    def __str__(self):
        return self.title
