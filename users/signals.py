from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Team


@receiver(post_save, sender=Team)
def assign_boss_on_team_creation(sender, instance, created, **kwargs):
    """
    Сигнал, который автоматически назначает руководителя команды ее участником.
    """
    if created:
        team_position = f"Руководитель команды {instance.name}"
        instance.participants.create(
            user=instance.boss, position=team_position
        )
