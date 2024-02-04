from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import Position, Team

User = get_user_model()


class UsersAPITests(APITestCase):
    def setUp(self):
        """Тестовые данные"""

        # ----------------------------------- Должности
        self.name = "Разработчик"
        self.name2 = "Дизайнер"
        self.name3 = "Владелец"
        self.position = Position.objects.create(name=self.name)
        self.position2 = Position.objects.create(name=self.name2)
        self.position3 = Position.objects.create(name=self.name3)

        # ------------------------------------------Пользователи и команды
        self.user0 = User.objects.create_user(
            username="user0",
            email="user0@mail.com",
            password="password",
            position=self.position,
            first_name="Oleg",
            last_name="Abramov",
            patronymic="Olegovich",
        )
        self.team0 = Team.objects.create(name="Team 0", boss=self.user0)
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@mail.com",
            password="password",
            team=self.team0,
            position=self.position2,
            first_name="Anatoliy",
            last_name="Brovnin",
            patronymic="Vladimirovich",
        )
        self.team1 = Team.objects.create(name="Team 1", boss=self.user1)
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@mail.com",
            password="password",
            team=self.team1,
            position=self.position3,
            first_name="Zina",
            last_name="Coralova",
            patronymic="Markovna",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    """Пользователи"""

    def test_get_users_list(self):
        """
        Проверка получения списка пользователей (GET).
        """

        url = reverse("users-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filtering_users(self):
        """Проверка фильтрации пользователей по id команды и отсутствию ИПР."""

        urls = ["/api/v1/users/?team=2", "/api/v1/users/?team=2&no_ipr=true"]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)

    def test_searching_users(self):
        """Проверка получения пользователя по имени или должности"""

        response = self.client.get("/api/v1/users/?search=Oleg")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("username"), self.user0.username)

    def test_retrieve_user(self):
        """Проверка получения пользователя (GET)."""

        user_id = self.user2.id
        url = reverse("users-detail", kwargs={"id": user_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("username"), self.user2.username)

    def test_users_me(self):
        """Проверка получения информации о текущем пользователе."""

        url = reverse("users-me")
        response = self.client.get(url)
        self.assertEqual(response.data.get("username"), self.user1.username)

    def test_users_positions(self):
        """Проверка получения списка должностей."""

        url = reverse("users-positions")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
