from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_link


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description"]


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_link])  # Добавляем валидатор для video_url
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'owner','video_url']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)
