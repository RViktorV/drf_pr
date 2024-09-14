from rest_framework import viewsets
from learning.models import Course
from learning.serializers import CourseSerializer
from rest_framework import generics
from learning.models import Lesson
from learning.serializers import LessonSerializer


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
