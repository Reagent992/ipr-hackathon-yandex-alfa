import random
import shutil
import string
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserTestCase(TestCase):
    def setUp(self) -> None:
        """Тестовые данные."""
        super().setUp()
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
        self.username = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        self.full_name = "Doe John Smith"
        self.user = User.objects.create_user(
            username=self.username,
            email=f"{self.username}@example.com",
            last_name="Doe",
            first_name="John",
            patronymic="Smith",
            userpic=self.uploaded,
        )
        # TODO: Проверить правильность сохранения данных.
        # TODO: Тесты для команды.
        # TODO: Тесты для участника команды.

    def tearDown(self) -> None:
        """Удаляем временную папку для медиа-файлов."""
        super().tearDown()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), self.full_name)

    def test_str(self):
        self.assertEqual(str(self.user), self.full_name)
