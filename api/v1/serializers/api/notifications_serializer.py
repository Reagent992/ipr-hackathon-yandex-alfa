from notifications.models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "recipient_id",
            "actor_object_id",
            "verb",
            "unread",
            "timestamp",
            # "actor_content_type_model",
        )
