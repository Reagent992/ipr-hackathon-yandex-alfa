from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from ipr.models import IPR
from tasks.models import Task, TaskStatus


@receiver(post_save, sender=IPR)
def created_ipr_notification(sender, instance: IPR, created, **kwargs):
    """Создание уведомления о новом ИПР."""
    msg = None
    if created:
        msg = f"Вам назначен новый ИПР: {instance.title}"
        notify.send(
            sender=instance.creator,
            recipient=instance.executor,
            verb=msg,
            target=instance,
        )
    elif instance.is_dirty():  # если ИПР изменился
        old_data = instance.get_dirty_fields()
        #  ------------------------------------------Уведомления для сотрудника
        if "start_date" in old_data:
            msg = (
                f'Дата начала работы по ИПР "{instance.title}"'
                f" изменена на {instance.start_date}"
            )
            notify.send(
                sender=instance.creator,
                recipient=instance.executor,
                verb=msg,
                target=instance,
            )
        elif "end_date" in old_data:
            msg = (
                f'Дата окончания работы по ИПР "{instance.title}"'
                f" изменена на {instance.end_date}"
            )
            notify.send(
                sender=instance.creator,
                recipient=instance.executor,
                verb=msg,
                target=instance,
            )
        #  ----------------------------------------Уведомления для руководителя
        elif instance.status is TaskStatus.COMPLETE:
            msg = (
                f"{instance.executor.get_full_name()}"
                f" закрыл ИПР: {instance.title}"
            )
            notify.send(
                sender=instance.executor,
                recipient=instance.creator,
                verb=msg,
                target=instance,
            )


@receiver(post_save, sender=Task)
def created_task_notification(sender, instance: Task, created, **kwargs):
    """Создание уведомления о новой задаче."""

    if created:
        task_name = getattr(instance, "name", "")
        text = f"Вам добавлена новая задача: {task_name}"
        notify.send(
            sender=instance.creator,
            recipient=instance.executor,
            verb=text,
            target=instance,
        )
