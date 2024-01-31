from django.db import models


class Status(models.TextChoices):
    COMPLETE = "complete", "Выполнен"
    IN_PROGRESS = "in_progress", "В работе"
    CANCEL = "cancel", "Отменен"
    TRAIL = "trail", "Отстает"
