from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from ipr.models import IPR

from .models import Skill, Task, TaskStatus

User = get_user_model()


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="user1", password="password1", email="user1@mail.ru"
        )
        cls.user2 = User.objects.create_user(
            username="user2", password="password2", email="user2@mail.ru"
        )
        cls.skill1 = Skill.objects.create(skill_name="Skill 1")
        cls.skill2 = Skill.objects.create(skill_name="Skill 2")
        cls.ipr = IPR.objects.create(
            title="Test IPR",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            creator=cls.user1,
            executor=cls.user2,
        )
        cls.task1 = Task.objects.create(
            name="Task 1",
            description="Description for Task 1",
            creator=cls.user1,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10),
            status=TaskStatus.IN_PROGRESS,
            executor=cls.user2,
            ipr=cls.ipr,
        )
        cls.task1.skill.add(cls.skill1)
        cls.task2 = Task.objects.create(
            name="Task 2",
            description="Description for Task 2",
            creator=cls.user2,
            start_date=date(2024, 1, 5),
            end_date=date(2024, 1, 15),
            status=TaskStatus.COMPLETE,
            executor=cls.user1,
            ipr=cls.ipr,
        )
        cls.task2.skill.add(cls.skill2)

    def test_task_creation(self):
        self.assertEqual(self.task1.name, "Task 1")
        self.assertEqual(self.task2.name, "Task 2")
        self.assertEqual(self.task1.creator, self.user1)
        self.assertEqual(self.task2.creator, self.user2)
        self.assertEqual(self.task1.start_date, date(2024, 1, 1))
        self.assertEqual(self.task2.start_date, date(2024, 1, 5))
        self.assertEqual(self.task1.end_date, date(2024, 1, 10))
        self.assertEqual(self.task2.end_date, date(2024, 1, 15))
        self.assertEqual(self.task1.status, TaskStatus.IN_PROGRESS)
        self.assertEqual(self.task2.status, TaskStatus.COMPLETE)
        self.assertEqual(self.task1.executor, self.user2)
        self.assertEqual(self.task2.executor, self.user1)
        self.assertEqual(self.task1.ipr, self.ipr)
        self.assertEqual(self.task2.ipr, self.ipr)
        self.assertTrue(self.skill1 in self.task1.skill.all())
        self.assertTrue(self.skill2 in self.task2.skill.all())

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
        new_status = TaskStatus.NOT_COMPLETE
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
