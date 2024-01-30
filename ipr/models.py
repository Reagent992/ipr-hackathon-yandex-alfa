from django.contrib.auth import get_user_model
from django.db import models

from core.statuses_for_ipr_tests import Status

User = get_user_model()


class IPR(models.Model):
    title = models.CharField("Название ИПР", max_length=100)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель ИПР",
        related_name="created_ipr",
    )
    creation_date = models.DateField("Дата создания ИПР", auto_now_add=True)
    start_date = models.DateField("Дата начала работ по ИПР")
    end_date = models.DateField("Дедлайн ИПР")
    status = models.CharField(
        "Статус ИПР", max_length=20, choices=Status, default=Status.IN_PROGRESS
    )
    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель ИПР",
        on_delete=models.CASCADE,
        related_name="ipr",
    )

    class Meta:
        verbose_name = "ИПР"

    def __str__(self):
        return self.title
