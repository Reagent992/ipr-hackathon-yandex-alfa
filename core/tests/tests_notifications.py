from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone
from notifications.models import Notification

from ipr.models import IPR
from tasks.models import Task, TaskStatus

User = get_user_model()


class NotificationsTest(TestCase):
    def setUp(self):
        """Тестовые данные."""
        # ---------------------------------------------------------Пользователи
        self.creator = User.objects.create_user(
            username="creator",
            email="creator@example.com",
            password="password",
        )
        self.executor = User.objects.create_user(
            username="executor",
            email="executor@example.com",
            password="password",
        )
        # ------------------------------------------------------------------ИПР
        self.ipr = IPR.objects.create(
            title="Test IPR",
            description="Test IPR Description",
            creator=self.creator,
            creation_date=timezone.now(),
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
            status=TaskStatus.IN_PROGRESS,
            executor=self.executor,
        )
        self.ipr_content_type_id = ContentType.objects.get_for_model(
            self.ipr
        ).id
        self.ipr_notification = Notification.objects.filter(
            target_object_id=self.ipr.id,
            target_content_type_id=self.ipr_content_type_id,
        ).first()
        # ---------------------------------------------------------------Задача
        self.task = Task.objects.create(
            name="Test Task",
            creator=self.creator,
            executor=self.executor,
            creation_date=timezone.now(),
            start_date=timezone.now() + timezone.timedelta(days=1),
            end_date=timezone.now() + timezone.timedelta(days=2),
        )
        self.task_content_type_id = ContentType.objects.get_for_model(
            self.task
        ).id
        self.task_notification = Notification.objects.filter(
            target_object_id=self.task.id,
            target_content_type_id=self.task_content_type_id,
        ).first()
        # ---------------------------------------------------------------------
        self.AMOUNT_OF_NOTIFICATIONS = 2

    def test_notifications_created(self):
        """Проверка количества созданный уведомлений."""
        self.assertEqual(
            Notification.objects.count(), self.AMOUNT_OF_NOTIFICATIONS
        )

    def test_created_ipr_notification(self):
        """Тест создания уведомления о новом ИПР."""
        self.assertIsNotNone(
            self.ipr_notification, "Объект уведомления не найден"
        )
        self.assertEqual(
            self.ipr_notification.recipient,
            self.executor,
            "Не правильный получатель",
        )
        self.assertEqual(
            self.ipr_notification.verb,
            f"Вам назначен новый ИПР: {self.ipr.title}",
            "Не правильное содержание уведомления",
        )

    def test_created_task_notification(self):
        """Тест создания уведомления о новой задаче."""
        self.assertIsNotNone(self.task_notification, "Объект задачи не найден")
        self.assertEqual(
            self.task_notification.recipient,
            self.executor,
            "Не правильный получатель",
        )
        self.assertEqual(
            self.task_notification.verb,
            f"Вам добавлена новая задача: {self.task.name}",
            "Не правильное содержание уведомления",
        )

    def test_edited_ipr_notification(self):
        """Тест создания уведомления об изменениях в начальной дате ИПР."""

        new_start_date = timezone.now() + timezone.timedelta(days=5)
        self.ipr.start_date = new_start_date
        self.ipr.save()
        updated_ipr_notification = Notification.objects.first()
        expected_msg = (
            f'Дата начала работы по ИПР "{self.ipr.title}"'
            f" изменена на {self.ipr.start_date}"
        )
        self.assertEqual(
            updated_ipr_notification.verb,
            expected_msg,
            (
                "Не правильное содержание уведомления"
                " об изменении start_date в ИПР"
            ),
        )

    def test_edited_ipr_end_date_notification(self):
        """Тест создания уведомления об изменении даты окончания IPR."""

        new_end_date = timezone.now() + timezone.timedelta(days=10)
        self.ipr.end_date = new_end_date
        self.ipr.save()
        updated_ipr_notification = Notification.objects.first()
        expected_msg = (
            f'Дата окончания работы по ИПР "{self.ipr.title}"'
            f" изменена на {self.ipr.end_date}"
        )
        self.assertEqual(
            updated_ipr_notification.verb,
            expected_msg,
            "Не правильное содержание уведомления об изменении end_date в ИПР",
        )

    def test_notification_created_after_ipr_complete(self):
        """Тест создания уведомления о завершении ИПР."""

        self.ipr.status = TaskStatus.COMPLETE
        self.ipr.save()
        updated_ipr_notification = Notification.objects.first()
        expected_msg = (
            f"{self.ipr.executor.get_full_name()}"
            f" закрыл ИПР: {self.ipr.title}"
        )
        self.assertEqual(
            updated_ipr_notification.verb,
            expected_msg,
            "Не правильное содержание уведомления о завершении ИПР",
        )
