from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.utils import timezone
from notifications.signals import notify

from ipr.models import IPR
from tasks.models import Task


@receiver(post_save, sender=IPR)
def created_ipr_notification(sender, instance: IPR, created, **kwargs):
    """Создание уведомления о новом ИПР."""
    if created:
        # TODO: Улучшить текст
        text = "Вам назначен новый ИПР"
        notify.send(
            sender=instance.creator,
            recipient=instance.executor,
            verb=text,
            target=instance,
        )
    else:
        # TODO: Улучшить текст
        text = "Изменение в ИПР."
        notify.send(
            sender=instance.creator,
            recipient=instance.executor,
            verb=text,
            target=instance,
        )


@receiver(post_save, sender=Task)
def created_task_notification(sender, instance: Task, created, **kwargs):
    """Создание уведомления о новой задачи."""

    if created:
        text = "Вам добавлена новая задача"
        notify.send(
            sender=instance.creator,
            recipient=instance.executor,
            verb=text,
            target=instance,
        )
    else:
        text = "Изменение в задаче."
        notify.send(
            sender=instance.creator,
            recipient=instance.executor,
            verb=text,
            target=instance,
        )


@receiver(post_init, sender=Task)
@receiver(post_init, sender=IPR)
def set_delayed_status(sender, instance, **kwargs):
    if (
        instance.end_date
        and instance.end_date < timezone.now().date()
        and instance.status != "trail"
    ):
        instance.status = "trail"
        instance.save()
