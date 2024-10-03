from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from learning.models import Course, Lesson, Subscription
from learning.serializers import CourseSerializer, LessonSerializer
from rest_framework import generics
from learning.permissions import IsModerator, IsOwnerOrModerator, IsOwnerOrReadOnly

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .paginators import CustomPagination

from .tasks import send_course_update_email_async


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами (Course).

    Предоставляет стандартные действия CRUD:
    - Получение списка курсов.
    - Создание нового курса.
    - Получение деталей курса по идентификатору.
    - Обновление существующего курса.
    - Удаление курса.

    Использует сериализатор `CourseSerializer`.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем курс к владельцу

    def perform_update(self, serializer):
        """
        Переопределяет стандартное обновление курса с асинхронной отправкой уведомлений подписчикам.
        """
        course = self.get_object()

        # Сохраняем изменения
        serializer.save()

        # Запускаем асинхронную задачу для отправки писем подписчикам
        send_course_update_email_async.delay(course.id)

class LessonListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка уроков (Lesson) и создания новых уроков.

    Доступные действия:
    - Получение списка всех уроков.
    - Создание нового урока.

    Использует сериализатор `LessonSerializer`.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления урока (Lesson).

    Доступные действия:
    - Получение деталей урока по идентификатору.
    - Обновление существующего урока.
    - Удаление урока.

    Использует сериализатор `LessonSerializer`.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]


class CourseSubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # Ищем существующую подписку
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
