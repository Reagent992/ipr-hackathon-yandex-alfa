# Generated by Django 5.0.1 on 2024-01-21 17:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IPR",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=100, verbose_name="Название ИПР"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=500, verbose_name="Описание ИПР"
                    ),
                ),
                (
                    "creation_date",
                    models.DateField(
                        auto_now_add=True, verbose_name="Дата создания ИПР"
                    ),
                ),
                (
                    "start_date",
                    models.DateField(verbose_name="Дата начала работ по ИПР"),
                ),
                ("end_date", models.DateField(verbose_name="Дедлайн ИПР")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("STATUS_ABSENT", "Отсутствует"),
                            ("STATUS_COMPLETED", "Выполнен"),
                            ("STATUS_NOT_COMPLETED", "Не выполнен"),
                            ("STATUS_IN_PROGRESS", "В работе"),
                            ("STATUS_CANCELLED", "Отменен"),
                            ("STATUS_DELAYED", "Отстает"),
                        ],
                        max_length=20,
                        verbose_name="Статус ИПР",
                    ),
                ),
                (
                    "usability",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Удобство использования ИПР"
                    ),
                ),
                (
                    "ease_of_creation",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Удобство создания ИПР"
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_ipr",
                        to="ipr.comment",
                        verbose_name="Комментарий к ИПР",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creator_ipr",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Создатель ИПР",
                    ),
                ),
                (
                    "executor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="executor_ipr",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Исполнитель ИПР",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_ipr",
                        to="ipr.task",
                        verbose_name="Задача",
                    ),
                ),
            ],
            options={
                "verbose_name": "ИПР",
            },
        ),
    ]
