from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from core.statuses import Status
from ipr.models import IPR
from tasks.models import Task

from .models import Rating

User = get_user_model()


class RatingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.setup_creation_date = timezone.now().date()
        cls.setup_start_date = (
            timezone.now() + timezone.timedelta(days=1)
        ).date()
        cls.setup_end_date = (
            timezone.now() + timezone.timedelta(days=2)
        ).date()
        cls.user1 = User.objects.create_user(
            username="user1", password="password1", email="user1@mail.ru"
        )
        cls.user2 = User.objects.create_user(
            username="user2", password="password2", email="user2@mail.ru"
        )
        cls.ipr = IPR.objects.create(
            title="Test IPR RATINGS",
            creation_date=cls.setup_creation_date,
            start_date=cls.setup_start_date,
            end_date=cls.setup_end_date,
            creator=cls.user1,
            executor=cls.user2,
        )

        cls.task = Task.objects.create(
            name="Task 1",
            description="Description for Task 1",
            creator=cls.user1,
            creation_date=cls.setup_creation_date,
            start_date=cls.setup_start_date,
            end_date=cls.setup_end_date,
            status=Status.IN_PROGRESS,
            executor=cls.user2,
            ipr=cls.ipr,
        )

    def test_rating_creation(self):
        rating_ipr = Rating.objects.create(
            content_object=self.ipr, user=self.user1, rating=4
        )
        rating_task = Rating.objects.create(
            content_object=self.task, user=self.user1, rating=5
        )

        self.assertIsInstance(rating_ipr, Rating)
        self.assertIsInstance(rating_task, Rating)

    def test_rating_str_method(self):
        rating_ipr = Rating.objects.create(
            content_object=self.ipr, user=self.user2, rating=4
        )
        expected_str_ipr = f"{self.ipr} - 4 от {self.user2}"
        self.assertEqual(str(rating_ipr), expected_str_ipr)

        rating_task = Rating.objects.create(
            content_object=self.task, user=self.user1, rating=5
        )
        expected_str_task = f"{self.task} - 5 от {self.user1}"
        self.assertEqual(str(rating_task), expected_str_task)

    def tearDown(self):
        Rating.objects.all().delete()
        Task.objects.all().delete()
        IPR.objects.all().delete()
        User.objects.all().delete()
