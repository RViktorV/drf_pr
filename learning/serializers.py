from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'owner']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)
