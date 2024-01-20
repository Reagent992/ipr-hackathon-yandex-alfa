from typing import Optional
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    patronymic = models.CharField(
        max_length=150, verbose_name="Отчество", blank=True
    )
    userpic = models.ImageField(
        verbose_name="Аватар пользователя",
        upload_to="userpic/",
        help_text="Загрузка аватара пользователя",
        blank=True,
    )
    position = models.CharField(
        max_length=150, verbose_name="Должность", blank=True
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

    def get_team(self) -> Optional["Team"]:
        """Возвращает команду пользователя, если она существует."""
        return self.team.first() if self.team.exists() else None


class Team(models.Model):
    """Команда."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Название команды")
    boss = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="managed_team",
        verbose_name="Руководитель",
    )
    users = models.ManyToManyField(
        User,
        through="MiddleUsersTeams",
        related_name="team",
        verbose_name="Участники команды",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self) -> str:
        return self.name


class MiddleUsersTeams(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name="Команда",
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
        related_name="participates",
    )
    joined_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата вступления"
    )

    class Meta:
        ordering = ("-joined_at",)
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команды"
        unique_together = ("user",)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.team.name})"
