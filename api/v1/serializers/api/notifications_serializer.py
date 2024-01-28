from notifications.models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомлений."""

    recipient_id = serializers.IntegerField(
        read_only=True, source="recipient.id"
    )
    actor_id = serializers.IntegerField(read_only=True, source="actor.id")
    target_object_id = serializers.IntegerField(read_only=True)
    target_content_type = serializers.CharField(
        source="target.__class__.__name__", read_only=True
    )

    class Meta:
        model = Notification
        fields = (
            "id",
            "verb",
            "unread",
            "target_object_id",
            "target_content_type",
            "timestamp",
            "recipient_id",
            "actor_id",
        )
