from drf_spectacular.utils import extend_schema, extend_schema_view
from notifications.models import Notification
from rest_framework import viewsets

from api.v1.serializers.api.notifications_serializer import (
    NotificationSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список уведомлений",
        description=(
            "Список уведомлений, "
            "уведомления именно для пользователя делающего запрос."
        ),
    ),
    retrieve=extend_schema(
        summary="Получить уведомление",
    ),
    partial_update=extend_schema(
        summary="Отметить уведомление как прочитанное",
        description=(
            "Чтобы отметить уведомление как прочитанное, "
            "нужно изменить значение unread."
        ),
    ),
)
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    http_method_names = ["get", "patch", "head", "options"]
    queryset = Notification.objects.all()
    # TODO: Отчистка уведомлений.

    def get_queryset(self):
        """Персонализированная выдача списка уведомлений."""
        user = self.request.user
        return Notification.objects.filter(recipient=user)
