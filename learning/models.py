from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """
    Модель курса.

    Поле `title` содержит название курса.
    Поле `preview` содержит изображение предварительного просмотра курса.
    Поле `description` содержит описание курса.
    """
    title = models.CharField(
        max_length=255, verbose_name="Название курса", help_text="Название курса"
    )
    preview = models.ImageField(upload_to="course_previews/", **NULLABLE)
    description = models.TextField(
        **NULLABLE, verbose_name="Описание курса", help_text="Описание курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока.

    Поле `course` связывает урок с конкретным курсом.
    Поле `title` содержит название урока.
    Поле `description` содержит описание урока.
    Поле `preview` содержит изображение предварительного просмотра урока.
    Поле `video_url` содержит URL ссылки на видео урока.
    """
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(
        **NULLABLE, verbose_name="Описание урока", help_text="Укажите описание урока"
    )
    preview = models.ImageField(upload_to="lesson_previews/", **NULLABLE)
    video_url = models.URLField(**NULLABLE)  # Сделать поле необязательным

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
