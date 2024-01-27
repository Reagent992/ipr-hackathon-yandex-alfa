import random
import shutil
import string
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from users.models import Position, Team

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserTestCase(TestCase):
    def setUp(self) -> None:
        """Тестовые данные."""
        # ----------------------------------------------------------------IMAGE
        self.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00"
            b"\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00"
            b"\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        self.uploaded = SimpleUploadedFile(
            name="small.gif", content=self.small_gif, content_type="image/gif"
        )
        # -----------------------------------------------------POSITIONS-CREATE
        self.basic_position = Position.objects.create(name="Basic")
        self.advanced_position = Position.objects.create(name="Advanced")
        self.pro_position = Position.objects.create(name="Pro")
        # ----------------------------------------------------------CASUAL-USER
        self.username = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        self.user_last_name = "Doe"
        self.user_first_name = "John"
        self.user_patronymic = "Smith"
        self.user_full_name = "Doe John Smith"
        self.user = User.objects.create_user(
            username=self.username,
            email=f"{self.username}@example.com",
            last_name=self.user_last_name,
            first_name=self.user_first_name,
            patronymic=self.user_patronymic,
            position=self.basic_position,
            userpic=self.uploaded,
        )
        # -----------------------------------------------------------BOSS-USERS
        self.chief_full_name = "Ilon Mask X"
        self.chief = User.objects.create_user(
            username="IlonMask",
            email="ilon@example.com",
            first_name="Ilon",
            last_name="Mask",
            patronymic="X",
            position=self.advanced_position,
            userpic=self.uploaded,
        )
        self.ceo = "Tim Cook Apple"
        self.ceo = User.objects.create_user(
            username="TimCook",
            email="tim@apple.com",
            first_name="Tim",
            last_name="Cook",
            patronymic="Apple",
            position=self.pro_position,
            userpic=self.uploaded,
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
        # ---------------------------------------------------------------AMOUNT
        self.amount_of_teams = 2
        # --------------------------------------------------------JOINING-TEAMS
        self.low_team.participants.add(self.user)

    def tearDown(self) -> None:
        """Удаляем временную папку для медиа-файлов."""
        shutil.rmtree(TEMP_MEDIA_ROOT)

    """User"""

    def test_get_full_name(self):
        self.assertEqual(
            self.user.get_full_name(),
            self.user_full_name,
            "Метод get_full_name выдал неверный результат",
        )

    def test_str(self):
        self.assertEqual(
            self.user.__str__(),
            self.user_full_name,
            "Метод __str__ выдал неверный результат",
        )

    def test_user_creation(self):
        """Проверка корректности созданных пользовательских данных.."""
        user_from_db = User.objects.get(username=self.username)

        self.assertEqual(user_from_db.email, f"{self.username}@example.com")
        self.assertEqual(
            user_from_db.last_name, self.user_last_name, "Неверная Фамилия"
        )
        self.assertEqual(
            user_from_db.first_name, self.user_first_name, "Неверное имя"
        )
        self.assertEqual(
            user_from_db.patronymic, self.user_patronymic, "Неверное отчество"
        )
        with user_from_db.userpic.open() as userpic_file:
            userpic_content = userpic_file.read()
        self.assertEqual(userpic_content, self.small_gif, "Неверная картинка")

    """Team"""

    def test_team_creation(self):
        """Создание команды."""
        self.assertTrue(isinstance(self.low_team, Team))
        self.assertEqual(
            self.low_team.name, self.low_team_name, "Неверное имя команды"
        )
        self.assertEqual(
            self.low_team.__str__(),
            self.low_team_name,
            "Метод __str__ выдал неверный результат",
        )
        self.assertEqual(
            self.low_team.boss, self.chief, "Назначен неверный руководитель"
        )
        self.assertEqual(
            Team.objects.count(),
            self.amount_of_teams,
            "Не совпадает количество команд",
        )

    def test_user_participates_in_one_team(self):
        """Пользователь состоит в команде."""
        self.assertIn(self.user, self.low_team.participants.all())

    def test_user_not_participates_in_any_team(self):
        """Босс не состоит в команде, которой руководит."""
        self.assertTrue(self.chief.team != self.low_team.boss)
