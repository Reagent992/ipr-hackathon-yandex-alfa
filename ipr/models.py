from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STATUSES = [
    "Отсутствует",
    "Выполнен",
    "Не выполнен",
    "В работе",
    "Отменен",
    "Отстает",
]


class Task(models.Model):
    pass


class Comment(models.Model):
    pass


class IPR(models.Model):
    title = models.CharField("Название ИПР", max_length=100)
    description = models.CharField("Описание ИПР", max_length=500)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель ИПР",
        related_name="creator_ipr",
    )
    creation_date = models.DateField(
        "Дата создания ИПР", auto_now=True, auto_now_add=True
    )
    start_date = models.DateField("Дата начала работ по ИПР")
    end_date = models.DateField("Дедлайн ИПР")
    status = models.CharField("Статус ИПР", max_length=20, choices=STATUSES)
    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель ИПР",
        on_delete=models.CASCADE,
        related_name="executor_ipr",
    )
    task = models.ForeignKey(
        Task,
        verbose_name="Задача",
        on_delete=models.CASCADE,
        related_name="task_ipr",
    )
    comment = models.ForeignKey(
        Comment,
        verbose_name="Комментарий к ИПР",
        on_delete=models.CASCADE,
        related_name="comment_ipr",
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
