from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ipr.models import IPR
from tasks.models import Task

User = get_user_model()


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@mail.com",
            password="password",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@mail.com",
            password="password",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user2)
        self.ipr = IPR.objects.create(
            title="Test IPR",
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            creator=self.user1,
            executor=self.user2,
        )
        self.task1 = Task.objects.create(
            name="Task 1",
            description="Description 1",
            creator=self.user1,
            executor=self.user2,
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            ipr=self.ipr,
        )
        self.task2 = Task.objects.create(
            name="Task 2",
            description="Description 2",
            creator=self.user1,
            executor=self.user2,
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            ipr=self.ipr,
        )

    def test_get_tasks_list(self):
        """
        Проверка получения списка задач (GET)
        """
        url = reverse("tasks-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.count())

    def test_create_task(self):
        """
        Проверка создания новой задачи (POST)
        """
        url = reverse("tasks-list")
        data = {
            "name": "New Task",
            "description": "New Description",
            "creator": self.user1.id,
            "creation_date": timezone.now().date(),
            "start_date": (timezone.now() + timezone.timedelta(days=1)).date(),
            "end_date": (timezone.now() + timezone.timedelta(days=2)).date(),
            "executor": self.user2.id,
            "ipr": self.ipr.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    # TODO: PUT-метод недоступен, надо переделать на PATCH
    # def test_update_task(self):
    #     """
    #     Проверка обновления задачи (PUT)
    #     """
    #     task_id = self.task2.pk
    #     url = reverse("tasks-detail", kwargs={"pk": task_id})
    #     data = {
    #         "name": "Updated Task",
    #         "description": "Updated Description",
    #       "start_date": (timezone.now() + timezone.timedelta(days=4)).date(),
    #         "end_date": (timezone.now() + timezone.timedelta(days=6)).date(),
    #     }
    #     response = self.client.put(url, data, format="json")

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.task2.refresh_from_db()
    #     self.assertEqual(self.task2.name, "Updated Task")

    def test_delete_task(self):
        """
        Проверка удаления задачи (DELETE)
        """
        task_id = self.task2.pk
        url = reverse("tasks-detail", kwargs={"pk": task_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
