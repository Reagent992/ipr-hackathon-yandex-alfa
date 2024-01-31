# Generated by Django 5.0.1 on 2024-01-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ipr", "0004_remove_ipr_creation_date_alter_ipr_start_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ipr",
            name="creation_date",
            field=models.DateField(
                auto_now_add=True,
                default="2023-01-01",
                verbose_name="Дата создания ИПР",
            ),
            preserve_default=False,
        ),
    ]