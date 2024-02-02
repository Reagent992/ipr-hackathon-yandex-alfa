from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from core.statuses import Status
from ipr.models import IPR

from .models import Task

User = get_user_model()


class TaskModelTest(TestCase):
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
            title="Test IPR",
            creation_date=cls.setup_creation_date,
            start_date=cls.setup_start_date,
            end_date=cls.setup_end_date,
            creator=cls.user1,
            executor=cls.user2,
        )
        cls.task1 = Task.objects.create(
            name="Task 1",
            description="Description for Task 1",
            creator=cls.user1,
            creation_date=cls.setup_creation_date,
            start_date=cls.setup_start_date,
            end_date=cls.setup_end_date,
            status=Status.IN_PROGRESS,
            executor=cls.user2,
            ipr=cls.ipr,
            skill="soft",
        )
        cls.task2 = Task.objects.create(
            name="Task 2",
            description="Description for Task 2",
            creator=cls.user2,
            creation_date=cls.setup_creation_date,
            start_date=cls.setup_start_date,
            end_date=cls.setup_end_date,
            status=Status.COMPLETE,
            executor=cls.user1,
            ipr=cls.ipr,
        )

    def test_task_creation(self):
        self.assertEqual(self.task1.name, "Task 1")
        self.assertEqual(self.task2.name, "Task 2")
        self.assertEqual(self.task1.creator, self.user1)
        self.assertEqual(self.task2.creator, self.user2)
        self.assertEqual(self.task1.start_date, self.setup_start_date)
        self.assertEqual(self.task2.start_date, self.setup_start_date)
        self.assertEqual(self.task1.end_date, self.setup_end_date)
        self.assertEqual(self.task2.end_date, self.setup_end_date)
        self.assertEqual(self.task1.status, Status.IN_PROGRESS)
        self.assertEqual(self.task2.status, Status.COMPLETE)
        self.assertEqual(self.task1.executor, self.user2)
        self.assertEqual(self.task2.executor, self.user1)
        self.assertEqual(self.task1.ipr, self.ipr)
        self.assertEqual(self.task2.ipr, self.ipr)
        self.assertEqual(self.task1.skill, "soft")
        self.assertEqual(self.task2.skill, "hard")

    def test_task_str_method(self):
        self.assertEqual(str(self.task1), "Task 1")
        self.assertEqual(str(self.task2), "Task 2")

    def test_task_deletion(self):
        task_count = Task.objects.count()
        self.task1.delete()
        self.assertEqual(Task.objects.count(), task_count - 1)

    def test_task_editing(self):
        new_name = "New Task Name"
        new_description = "New Description for Task"
        new_status = Status.COMPLETE
        new_start_date = date(2024, 2, 1)
        new_end_date = date(2024, 2, 10)

        self.task1.name = new_name
        self.task1.description = new_description
        self.task1.status = new_status
        self.task1.start_date = new_start_date
        self.task1.end_date = new_end_date
        self.task1.save()

        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.name, new_name)
        self.assertEqual(updated_task.description, new_description)
        self.assertEqual(updated_task.status, new_status)
        self.assertEqual(updated_task.start_date, new_start_date)
        self.assertEqual(updated_task.end_date, new_end_date)
