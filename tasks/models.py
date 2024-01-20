# import datetime
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    """Модель задачи."""
    STATUS_CHOICES = (
        ("none", "Отсутствует"),
        ("complete", "Выполнен"),
        ("not_complete", "Не выполнен"),
        ("in_progress", "В работе"),
        ("cancel", "Отменен"),
        ("trail", "Отстает"),
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Название задачи",
        help_text="Введите название задачи",
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Описание задачи",
        help_text="Добавьте текст описания группы",
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель задачи",
        related_name="creator_ipr",
    )
    creationdate = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания задачи",
    )
    startdate = models.DateField("Дата начала работ по задаче", null=True,
                                  blank=True,)
    enddate = models.DateField(verbose_name="Дедлайн задачи",  null=True,
                                blank=True,)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][1], verbose_name="Статус задачи"
    )
    type = models.CharField(
        max_length=200,
        verbose_name="Тип задачи",
        help_text="Выберите тип задачи",
    )
    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель задачи",
        on_delete=models.CASCADE,
        related_name="executor_task",
    )

    class Meta:
        verbose_name = "Задачa"
        verbose_name_plural = "Задачa"

    def __str__(self):
        return self.name
