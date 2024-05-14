from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course, Subscription
from users.models import User


class MaterialsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="example@example.com", is_staff=True, is_superuser=True
        )
        self.user.set_password("Admin")
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.lessons = Lesson.objects.create(title="test_lesson", owner=self.user)
        self.course = Course.objects.create(title="test_course", owner=self.user)

    def test_create_lesson(self):
        url = reverse("materials:lesson-create")
        data = {"title": "test_lesson", "owner": self.user.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    # def test_list_lesson(self):
    #     url = reverse("materials:lesson-list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(
    #         response.json(),
    #         {
    #             "count": 1,
    #             "next": None,
    #             "previous": None,
    #             "results": [
    #                 {
    #                     "id": 6,
    #                     "title": "test_lesson",
    #                     "description": None,
    #                     "preview": None,
    #                     "video_link": None,
    #                     "course": None,
    #                     "owner": 4,
    #                 }
    #             ],
    #         },
    #     )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        url = reverse("materials:lesson-delete", args=(self.lessons.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        url = reverse("materials:lesson-update", args=(self.lessons.pk,))
        data = {
            "title": "test_lesson_21",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "test_lesson_21")

    def test_detail_lesson(self):
        les_detail = Lesson.objects.create(
            owner=self.user,
            title="detail",
            description="description",
            video_link="youtube.com/watch/123456",
        )

        response = self.client.get(reverse("materials:lesson-view", args=[les_detail.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": 5,
                "title": "detail",
                "description": "description",
                "preview": None,
                "video_link": "youtube.com/watch/123456",
                "course": None,
                "owner": 3,
            },
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="user@example.com",
            is_staff=True,
            is_active=True,
            is_superuser=False
        )
        self.user.set_password("123qwe")
        self.user.save()
        self.course = Course.objects.create(
            title="course1", description="testing", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        url = reverse("materials:subscriptions")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(), {'message': 'Подписка на курс успешно добавлена'})
