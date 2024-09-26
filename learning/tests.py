from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
import pytest
from rest_framework.test import APIClient
from learning.models import Lesson, Course, Subscription
from users.models import Users
from learning.validators import validate_youtube_link


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create(
            email="testuser@example.com", password="password"
        )
        self.user.set_password("password")  # Убедитесь, что пароль хеширован
        self.user.save()

        # Создать курс с назначенным владельцем
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course  # Assign the test user as the owner
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("learning:lesson-list-create")
        data = {"title": "New Lesson", "course": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        url = reverse("learning:lesson-detail", args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    def test_update_lesson(self):
        url = reverse("learning:lesson-detail", args=[self.lesson.pk])
        data = {"title": "Updated Lesson", "course": self.course.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        url = reverse("learning:lesson-detail", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create(
            email="testusers@example.com", password="password"
        )
        self.user.set_password("password")  # Убедитесь, что пароль хеширован
        self.user.save()

        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_add_subscription(self):
        url = reverse("learning:course-subscription")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse(
            "learning:course-subscription"
        )  # Adjust according to your URL naming
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )


def test_validate_youtube_link():
    # Корректные ссылки
    valid_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
    ]
    for link in valid_links:
        try:
            validate_youtube_link(link)
        except ValidationError:
            pytest.fail(f"Validation failed for valid link: {link}")

    # Некорректные ссылки
    invalid_links = ["https://vimeo.com/123456789", "https://www.example.com/video"]
    for link in invalid_links:
        with pytest.raises(ValidationError):
            validate_youtube_link(link)
