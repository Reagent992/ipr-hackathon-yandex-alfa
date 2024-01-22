from django.contrib.auth import get_user_model
from django.db import models

from ipr.models import IPR

User = get_user_model()


class TaskStatus(models.TextChoices):
    NONE = "none", "Отсутствует"
    COMPLETE = "complete", "Выполнен"
    NOT_COMPLETE = "not_complete", "Не выполнен"
    IN_PROGRESS = "in_progress", "В работе"
    CANCEL = "cancel", "Отменен"
    TRAIL = "trail", "Отстает"


class Skill(models.Model):
    skill_name = models.CharField(
        max_length=255,
        verbose_name="Навык",
    )

    class Meta:
        ordering = ("skill_name",)
        verbose_name = "Навыки"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.skill_name


class Task(models.Model):
    """Модель задачи."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название задачи",
    )
    description = models.CharField(
        max_length=500,
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
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        verbose_name="Дедлайн задачи",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus,
        default=TaskStatus.NONE,
        verbose_name="Статус задачи",
    )
    skill = models.ManyToManyField(
        Skill, max_length=255, blank=True, verbose_name="Навык"
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
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name
