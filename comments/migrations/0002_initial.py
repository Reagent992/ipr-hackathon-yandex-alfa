# Generated by Django 5.0.1 on 2024-01-31 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("comments", "0001_initial"),
        ("ipr", "0001_initial"),
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор комментария",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="ipr",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="ipr.ipr",
                verbose_name="ИПР",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="tasks.task",
                verbose_name="Задача",
            ),
        ),
    ]
