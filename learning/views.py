from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from learning.models import Course
from learning.serializers import CourseSerializer
from rest_framework import generics
from learning.models import Lesson
from learning.serializers import LessonSerializer
from learning.permissions import IsModerator, IsOwnerOrModerator, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем курс к владельцу


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]
