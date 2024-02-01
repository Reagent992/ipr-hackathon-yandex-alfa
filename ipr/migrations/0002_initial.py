# Generated by Django 5.0.1 on 2024-01-31 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("ipr", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="ipr",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_ipr",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Создатель ИПР",
            ),
        ),
        migrations.AddField(
            model_name="ipr",
            name="executor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ipr",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Исполнитель ИПР",
            ),
        ),
    ]
