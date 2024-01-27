from notifications.models import Notification
from rest_framework import serializers

from api.v1.serializers.api.users_serializer import CustomUserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомлений."""

    recipient = CustomUserSerializer(read_only=True, many=False)
    actor = CustomUserSerializer(read_only=True, many=False)

    class Meta:
        model = Notification
        fields = (
            "id",
            "verb",
            "unread",
            "timestamp",
            "recipient",
            "actor",
        )

    # TODO: Добавить ссылку на объект уведомления.
    # url = reverse('your_nested_detail_view_name',
    #     kwargs={'content_type': contentType, 'pk': objectId})
    # >>> reverse("users-detail", args=[user.id])
    # >>> '/api/v1/users/5/'
    # request.build_absolute_uri('/some-relative-path/')
    # т.е. всего 3 варианта, можно if-ами пройти.
    # if isinstance(notification.target, IPR):
