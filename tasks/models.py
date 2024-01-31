from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from ipr.models import IPR

User = get_user_model()


class TaskStatus(models.TextChoices):
    COMPLETE = "complete", "Выполнен"
    IN_PROGRESS = "in_progress", "В работе"
    CANCEL = "cancel", "Отменен"
    TRAIL = "trail", "Отстает"


class Skill(models.Model):
    skill_name = models.CharField(
        max_length=settings.SKILL_LEN,
        verbose_name="Навык",
    )

    class Meta:
        ordering = ("skill_name",)
        verbose_name = "Навыки"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.skill_name


class Task(DirtyFieldsMixin, models.Model):
    """Модель задачи."""

    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name="Название задачи",
    )
    description = models.CharField(
        max_length=settings.DESCRIPTION_LEN,
        null=True,
        blank=True,
        verbose_name="Описание задачи",
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель задачи",
        related_name="created_tasks",
    )
    creation_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания задачи",
    )
    start_date = models.DateField(
        verbose_name="Дата начала работ по задаче",
    )
    end_date = models.DateField(
        verbose_name="Дедлайн задачи",
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus,
        default=TaskStatus.IN_PROGRESS,
        verbose_name="Статус задачи",
    )
    skill = models.ManyToManyField(
        Skill, max_length=settings.SKILL_LEN, verbose_name="Навык"
    )
    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель задачи",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    ipr = models.ForeignKey(
        IPR,
        verbose_name="ИПР",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
    )

    class Meta:
        ordering = ("-creator",)
        verbose_name = "Задачи"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name
