from rest_framework import serializers
from learning.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "description", "preview", "video_url"]



class CourseSerializer(serializers.ModelSerializer):
    # Поле для вывода количества уроков в курсе
    number_of_lessons = serializers.SerializerMethodField()

    # Вложенный сериализатор для уроков
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'number_of_lessons', 'lessons']  # Добавляем поле в список полей

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()  # Считаем количество связанных уроков
