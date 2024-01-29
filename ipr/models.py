from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


STATUSES = [
    ("complete", "Выполнен"),
    ("in_progress", "В работе"),
    ("canceled", "Отменен"),
    ("trail", "Отстает"),
]


class IPR(models.Model):
    title = models.CharField("Название ИПР", max_length=100)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель ИПР",
        related_name="created_ipr",
    )
    creation_date = models.DateField("Дата создания ИПР", auto_now_add=True)
    start_date = models.DateField(
        "Дата начала работ по ИПР", blank=True, null=True
    )
    end_date = models.DateField("Дедлайн ИПР")
    status = models.CharField(
        "Статус ИПР", max_length=20, choices=STATUSES, default=STATUSES[0]
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
