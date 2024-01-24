import random
import string

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Team

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self) -> None:
        """Тестовые данные."""
        # ----------------------------------------------------------CASUAL-USER
        self.username = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        self.user_last_name = "Doe"
        self.user_first_name = "John"
        self.user_patronymic = "Smith"
        self.user_full_name = "Doe John Smith"
        self.position = "Developer"
        self.user = User.objects.create_user(
            username=self.username,
            email=f"{self.username}@example.com",
            last_name=self.user_last_name,
            first_name=self.user_first_name,
            patronymic=self.user_patronymic,
            position=self.position,
        )
        # -----------------------------------------------------------BOSS-USERS
        self.chief_full_name = "Ilon Mask X"
        self.chief = User.objects.create_user(
            username="IlonMask",
            email="ilon@example.com",
            first_name="Ilon",
            last_name="Mask",
            patronymic="X",
            position="Low CEO",
        )
        self.ceo = "Tim Cook Apple"
        self.ceo = User.objects.create_user(
            username="TimCook",
            email="tim@apple.com",
            first_name="Tim",
            last_name="Cook",
            patronymic="Apple",
            position="Big CEO",
        )
        # ---------------------------------------------------------------------
        self.amount_of_users = 3
        # -----------------------------------------------------------------TEAM
        self.low_team_name = "Team X"
        self.low_team = Team.objects.create(
            name=self.low_team_name, boss=self.chief
        )
        self.big_team_name = "Team Apple"
        self.big_team = Team.objects.create(
            name=self.big_team_name, boss=self.ceo
        )
        # ---------------------------------------------------------------------
        self.amount_of_teams = 2
        # --------------------------------------------------------Team Joining
        self.low_team.users.add(self.user)
        self.big_team.users.add(self.chief)

    def test_user_receives_notification(self):
        """Пользователь получает уведомление."""
        # TODO:
        pass
