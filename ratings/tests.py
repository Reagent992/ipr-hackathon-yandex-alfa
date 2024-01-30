from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from ipr.models import IPR
from tasks.models import Task, TaskStatus

from .models import Rating

User = get_user_model()


class RatingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="user1", password="password1", email="user1@mail.ru"
        )
        cls.user2 = User.objects.create_user(
            username="user2", password="password2", email="user2@mail.ru"
        )
        cls.ipr = IPR.objects.create(
            title="Test IPR",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            creator=cls.user1,
            executor=cls.user2,
        )

        cls.task = Task.objects.create(
            name="Task 1",
            description="Description for Task 1",
            creator=cls.user1,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            status=TaskStatus.IN_PROGRESS,
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
