from django.conf import settings
from django.db import models
from ipr.models import IPR
from task.models import Task
from users.models import User


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
    )
    ipr = models.ForeignKey(
        IPR,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="ИПР",
    )
    task = models.ForeignKey(
        Task,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Задача",
    )

    text = models.TextField(
        verbose_name="Комментарий",
        max_length=settings.MAX_LEN_COMMENT_TEXT,
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
