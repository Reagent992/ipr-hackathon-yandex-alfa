from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STATUSES = [
    ("STATUS_ABSENT", "Отсутствует"),
    ("STATUS_COMPLETED", "Выполнен"),
    ("STATUS_NOT_COMPLETED", "Не выполнен"),
    ("STATUS_IN_PROGRESS", "В работе"),
    ("STATUS_CANCELLED", "Отменен"),
    ("STATUS_DELAYED", "Отстает"),
]


class IPR(models.Model):
    title = models.CharField("Название ИПР", max_length=100)
    description = models.CharField("Описание ИПР", max_length=500)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель ИПР",
        related_name="created_ipr",
    )
    creation_date = models.DateField("Дата создания ИПР", auto_now_add=True)
    start_date = models.DateField("Дата начала работ по ИПР")
    end_date = models.DateField("Дедлайн ИПР")
    status = models.CharField("Статус ИПР", max_length=20, choices=STATUSES)
    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель ИПР",
        on_delete=models.CASCADE,
        related_name="ipr",
    )
    usability = models.PositiveSmallIntegerField(
        verbose_name="Удобство использования ИПР", default=0
    )
    ease_of_creation = models.PositiveSmallIntegerField(
        verbose_name="Удобство создания ИПР", default=0
    )

    class Meta:
        verbose_name = "ИПР"

    def __str__(self):
        return self.title
