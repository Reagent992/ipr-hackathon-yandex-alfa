from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.statuses import Status
from ipr.models import IPR
from tasks.models import Task
from users.models import Team

User = get_user_model()


class IPRAPITests(APITestCase):
    def setUp(self):
        """Тестовые данные"""
        # ------------------------------------------Пользователи и команды
        self.user0 = User.objects.create_user(
            username="user0",
            email="user0@mail.com",
            password="password",
        )
        self.team0 = Team.objects.create(name="Team 0", boss=self.user0)
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@mail.com",
            password="password",
            team=self.team0,
        )
        self.team1 = Team.objects.create(name="Team 1", boss=self.user1)
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@mail.com",
            password="password",
            team=self.team1,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        # ------------------------------------------ИПР
        self.ipr0 = IPR.objects.create(
            title="Test IPR 0",
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            creator=self.user0,
            executor=self.user1,
        )
        self.ipr = IPR.objects.create(
            title="Test IPR 2",
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            creator=self.user1,
            executor=self.user2,
        )
        # -------------------------------------------Задачи
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
            status=Status.COMPLETE,
        )

    """ИПР"""

    def test_get_ipr_list(self):
        """
        Проверка получения списка ИПР (GET)
        """
        url = reverse("ipr-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_ipr(self):
        """Проверка получения ИПР пользователя"""
        ipr_id = self.ipr.id
        url = reverse("ipr-detail", kwargs={"pk": ipr_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.ipr.title)

    def test_create_ipr(self):
        """
        Проверка создания нового ИПР (POST)
        """
        url = reverse("ipr-list")
        data = {
            "title": "New IPR",
            "creator": self.user1.id,
            "creation_date": timezone.now().date(),
            "start_date": (timezone.now() + timezone.timedelta(days=1)).date(),
            "end_date": (timezone.now() + timezone.timedelta(days=2)).date(),
            "executor": self.user2.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IPR.objects.count(), 3)

    def test_update_ipr(self):
        """
        Проверка обновления ИПР (PATCH)
        """
        ipr_id = self.ipr.pk
        url = reverse("ipr-detail", kwargs={"pk": ipr_id})
        data = {
            "title": "Updated IPR",
            "start_date": (timezone.now() + timezone.timedelta(days=4)).date(),
            "end_date": (timezone.now() + timezone.timedelta(days=6)).date(),
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ipr.refresh_from_db()
        self.assertEqual(self.ipr.title, "Updated IPR")

    def test_ipr_status(self):
        """
        Проверка получения статуса выполнения ИПР (GET)
        """
        ipr_id = self.ipr.id
        url = reverse("ipr-status", kwargs={"pk": ipr_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("progress"), 50)
