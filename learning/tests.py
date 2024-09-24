from django.core.exceptions import ValidationError
from learning.validators import validate_youtube_link
import pytest

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from learning.models import Lesson, Course, Subscription


def test_validate_youtube_link():
    # Корректные ссылки
    valid_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ"
    ]
    for link in valid_links:
        try:
            validate_youtube_link(link)
        except ValidationError:
            pytest.fail(f"Validation failed for valid link: {link}")

    # Некорректные ссылки
    invalid_links = [
        "https://vimeo.com/123456789",
        "https://www.example.com/video"
    ]
    for link in invalid_links:
        with pytest.raises(ValidationError):
            validate_youtube_link(link)


class LessonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='password')
        self.course = Course.objects.create(title="Test Course")
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {"title": "New Lesson", "course": self.course.id}
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_lesson(self):
        response = self.client.get(f"/api/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Test Lesson")

    def test_update_lesson(self):
        data = {"title": "Updated Lesson"}
        response = self.client.put(f"/api/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, 204)


class SubscriptionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='password')
        self.course = Course.objects.create(title="Test Course")
        self.client.force_authenticate(user=self.user)

    def test_add_subscription(self):
        response = self.client.post("/api/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post("/api/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
