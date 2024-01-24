from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import validate_username_custom


class User(AbstractUser):
    """Расширенная модель пользователя."""

    email = models.EmailField(
        "Электронная почта",
        unique=True,
        db_index=True,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=settings.NAME_LENGTH,
    )
    first_name = models.CharField(
        "Имя",
        max_length=settings.NAME_LENGTH,
    )
    patronymic = models.CharField(
        "Отчество",
        max_length=settings.NAME_LENGTH,
        blank=True,
    )
    username = models.CharField(
        "Имя пользователя",
        max_length=settings.NAME_LENGTH,
        unique=True,
        validators=(
            UnicodeUsernameValidator,
            validate_username_custom,
        ),
    )
    userpic = models.ImageField(
        "Аватар пользователя",
        upload_to="userpic/",
        help_text="Загрузка аватара пользователя",
        blank=True,
        null=True,
    )
    position = models.CharField(
        "Должность",
        max_length=settings.NAME_LENGTH,
        blank=True,
        null=True,
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.SET_NULL,
        verbose_name="Команда",
        related_name="participants",
        null=True,
        blank=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
    )

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        """ФИО."""
        names = (self.last_name, self.first_name, self.patronymic)
        return " ".join(names) if any(names) else self.username or self.email

    def is_boss(self) -> bool:
        """Является ли пользователь руководителем команды."""
        return hasattr(self, "managed_team") and self.managed_team is not None


class Team(models.Model):
    """Команда."""

    name = models.CharField(
        max_length=settings.NAME_LENGTH, verbose_name="Название команды"
    )
    boss = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="managed_team",
        verbose_name="Руководитель",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self) -> str:
        return self.name
