from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from notifications.models import Notification
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.statuses import Status
from ipr.models import IPR

User = get_user_model()


class NotificationAPITestCase(APITestCase):
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
        self.client = APIClient()
        self.client.force_authenticate(user=self.executor)
        # ----------------------------------------------------------------ИПР-1
        self.ipr1 = IPR.objects.create(
            title="Test IPR",
            creator=self.creator,
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            status=Status.IN_PROGRESS,
            executor=self.executor,
        )
        self.ipr_content_type_id = ContentType.objects.get_for_model(
            self.ipr1
        ).id
        self.ipr_notification = Notification.objects.filter(
            target_object_id=self.ipr1.id,
            target_content_type_id=self.ipr_content_type_id,
        ).first()
        # ----------------------------------------------------------------ИПР-2
        self.ipr2 = IPR.objects.create(
            title="Test IPR 2",
            creator=self.creator,
            creation_date=timezone.now().date(),
            start_date=(timezone.now() + timezone.timedelta(days=1)).date(),
            end_date=(timezone.now() + timezone.timedelta(days=2)).date(),
            status=Status.IN_PROGRESS,
            executor=self.executor,
        )
        self.ipr2_content_type_id = ContentType.objects.get_for_model(
            self.ipr2
        ).id
        self.ipr2_notification = Notification.objects.filter(
            target_object_id=self.ipr2.id,
            target_content_type_id=self.ipr2_content_type_id,
        ).first()
        # ------------------------------------------------------------Константы
        self.AMOUNT_OF_NOTIFICATIONS = 2
        # ------------------------------------------------------------Эндпоинты
        self.all_notifications_url = reverse("notifications-list")
        self.one_notification_url = reverse(
            "notifications-detail",
            kwargs={"pk": self.ipr_notification.id},
        )
        self.notifications_mark_all_as_read_url = reverse(
            "notifications-mark-all-as-read"
        )
        self.notifications_unseen_count_url = reverse("notifications-unseen")

    def test_list_notifications(self):
        """Тест эндпоинта уведомлений."""
        response = self.client.get(self.all_notifications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.AMOUNT_OF_NOTIFICATIONS)

    def test_mark_notification_as_read(self):
        """Тест эндпоинта отметки уведомления как прочтенного."""
        self.assertTrue(self.ipr_notification.unread)
        response = self.client.patch(
            self.one_notification_url, {"unread": False}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ipr_notification.refresh_from_db()
        self.assertFalse(self.ipr_notification.unread)

    def test_mark_all_notifications_as_read(self):
        """Тест эндпоинта отметки всех уведомлений пользователя
        как прочтенных."""
        self.assertTrue(self.executor.notifications.unread().count() > 0)
        response = self.client.get(self.notifications_mark_all_as_read_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.executor.notifications.unread().count(), 0)

    def test_unseen_notifications_count(self):
        """Тест эндпоинта получения количества непрочитанных уведомлений."""
        response = self.client.get(self.notifications_unseen_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unseen"], self.AMOUNT_OF_NOTIFICATIONS)
