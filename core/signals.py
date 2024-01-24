from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from comments.models import Comment
from ipr.models import IPR
from tasks.models import Task


@receiver(post_save, sender=IPR)
def created_ipr_notification(sender, instance: IPR, created, **kwargs):
    """Создание уведомления о новом ИПР."""
    if created:
        text = "Вам назначен новый ИПР"
        notify.send(sender=instance, recipient=instance.executor, verb=text)
    else:
        text = "Изменение в ИПР."
        notify.send(sender=instance, recipient=instance.executor, verb=text)


@receiver(post_save, sender=Task)
def created_task_notification(sender, instance: Task, created, **kwargs):
    """Создание уведомления о новой задачи."""

    if created:
        text = "Вам добавлена новая задача"
        notify.send(sender=instance, recipient=instance.executor, verb=text)
    else:
        text = "Изменение в задаче."
        notify.send(sender=instance, recipient=instance.executor, verb=text)


@receiver(post_save, sender=Comment)
def created_comment_notification(sender, instance: Comment, created, **kwargs):
    """Создание уведомления о новом комментарии."""
    if created:
        text = "Новый комментарий"
        notify.send(
            sender=instance, recipient=instance.task.executor, verb=text
        )
