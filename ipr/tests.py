import datetime
import random
import string
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from core.statuses import Status
from ipr.models import IPR

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserTestCase(TestCase):
    def setUp(self) -> None:
        """Тестовые данные."""
        # ----------------------------------------------------------CASUAL-USER
        self.username = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        self.user_last_name = "Doe"
        self.user_first_name = "John"
        self.user = User.objects.create_user(
            username=self.username,
            email=f"{self.username}@example.com",
            last_name=self.user_last_name,
            first_name=self.user_first_name,
        )
        # -----------------------------------------------------------BOSS-USERS
        self.chief = User.objects.create_user(
            username="IlonMask",
            email="ilon@example.com",
            first_name="Ilon",
            last_name="Mask",
        )
        # -----------------------------------------------------------IPR
        self.title = "1-st title"
        self.creator = self.chief
        self.creation_date = datetime.date.today()
        self.start_date = self.creation_date + datetime.timedelta(days=5)
        self.end_date = self.start_date + datetime.timedelta(weeks=4)
        self.executor = self.user
        self.ipr = IPR.objects.create(
            title=self.title,
            creator=self.creator,
            creation_date=self.creation_date,
            start_date=self.start_date,
            end_date=self.end_date,
            executor=self.executor,
        )

    """IPR"""

    def test_str(self):
        self.assertEqual(
            self.ipr.__str__(),
            self.title,
            "Метод __str__ выдал неверный результат",
        )

    def test_user_creation(self):
        """Проверка корректности созданных пользовательских данных.."""
        ipr_from_db = IPR.objects.get(executor=self.executor)
        self.assertEqual(ipr_from_db.creator, self.creator)
        self.assertEqual(
            ipr_from_db.title, self.title, "Неверное название ИПР"
        )
        self.assertEqual(
            ipr_from_db.creation_date,
            self.creation_date,
            "Неверная дата создания ИПР",
        )
        self.assertEqual(
            ipr_from_db.start_date, self.start_date, "Неверная дата начала ИПР"
        )
        self.assertEqual(
            ipr_from_db.end_date, self.end_date, "Неверная дата дедлайна ИПР"
        )
        self.assertEqual(
            ipr_from_db.status, Status.IN_PROGRESS, "Неверный статус ИПР"
        )
