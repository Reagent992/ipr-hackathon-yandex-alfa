from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from ipr.models import IPR
from tasks.models import Task


@receiver(post_save, sender=IPR)
def created_ipr_notification(sender, instance: IPR, created, **kwargs):
    """Создание уведомления о новом ИПР."""
    # TODO: Уведомление о просьбе оценить ИПР, после его закрытия.
    # TODO: Уведомление об изменение статуса ИПР.
    if created:
        text = "Вам назначен новый ИПР"
        notify.send(sender=instance, recipient=instance.executor, verb=text)


# TODO: сигнал при создание задачи
@receiver(post_save, sender=IPR)
def created_task_notification(sender, instance: Task, created, **kwargs):
    """Создание уведомления о новой задачи."""

    if created:
        text = "Вам добавили новую задачу"
        notify.send(sender=instance, recipient=instance.executor, verb=text)


# TODO: сигнал при создание комментария
