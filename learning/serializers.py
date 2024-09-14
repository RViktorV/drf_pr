from rest_framework import serializers
from learning.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели урока (Lesson).

    Поля:
    - `id`: Идентификатор урока.
    - `course`: Связанный курс, к которому относится урок.
    - `title`: Название урока.
    - `description`: Описание урока.
    - `preview`: Изображение предварительного просмотра урока.
    - `video_url`: URL видео урока.
    """
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "description", "preview", "video_url"]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса (Course).

    Поля:
    - `id`: Идентификатор курса.
    - `title`: Название курса.
    - `description`: Описание курса.
    - `preview`: Изображение предварительного просмотра курса.
    - `number_of_lessons`: Количество уроков, связанных с курсом.
    - `lessons`: Список уроков, связанных с курсом.
    """

    # Поле для вывода количества уроков в курсе
    number_of_lessons = serializers.SerializerMethodField()

    # Вложенный сериализатор для уроков
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "number_of_lessons",
            "lessons",
        ]  # Добавляем поле в список полей

    def get_number_of_lessons(self, obj):
        """
        Получить количество уроков, связанных с курсом.

        :param obj: Экземпляр модели Course.
        :return: Количество связанных уроков.
        """
        return obj.lessons.count()  # Считаем количество связанных уроков
