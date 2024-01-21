from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STATUS_CHOICES = (
    ("none", "Отсутствует"),
    ("complete", "Выполнен"),
    ("not_complete", "Не выполнен"),
    ("in_progress", "В работе"),
    ("cancel", "Отменен"),
    ("trail", "Отстает"),
)


class Skill(models.Model):
    skill_name = models.CharField(max_length=255, verbose_name = "Навык",
                                  help_text="Введите название навыка",
                                  )

    class Meta:
        ordering = ('skill_name',)
        verbose_name = "Навыки"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.skill_name


class Task(models.Model):
    """Модель задачи."""
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
        related_name="creator_task",
    )
    creation_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания задачи",
    )
    start_date = models.DateField("Дата начала работ по задаче", null=True,
                                  blank=True,)
    end_date = models.DateField(verbose_name="Дедлайн задачи",  null=True,
                                blank=True,)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][1], verbose_name="Статус задачи"
    )
    skill = models.ManyToManyField(
        Skill,
        max_length=255, blank=True,
        verbose_name="Навык"
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
