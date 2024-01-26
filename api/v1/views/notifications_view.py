from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.serializers.api.notifications_serializer import (
    NotificationSerializer,
)
from api.v1.serializers.internal.dummy_serializer import DummySerializer


@extend_schema(tags=["Уведомления"])
@extend_schema_view(
    list=extend_schema(
        summary="Список уведомлений",
        description=(
            "Список уведомлений, "
            "уведомления именно для пользователя делающего запрос."
        ),
    ),
    retrieve=extend_schema(
        summary="Уведомление",
    ),
    partial_update=extend_schema(
        summary="Отметить уведомление как прочитанное",
        description=(
            "Чтобы отметить уведомление как прочитанное, "
            "нужно изменить значение unread."
        ),
    ),
    mark_all_as_read=extend_schema(
        methods=["get"],
        summary="Отметить все уведомления пользователя как прочтенные",
        responses={status.HTTP_200_OK: DummySerializer},
    ),
)
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def partial_update(self, request, pk):
        """Отметить уведомление как прочитанное."""
        notification = self.get_object()
        if request.user != notification.recipient:
            return Response(
                {"message": "Уведомление не принадлежит пользователю."},
                status=status.HTTP_403_FORBIDDEN,
            )
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    def get_queryset(self):
        """Персонализированная выдача списка уведомлений."""
        return self.request.user.notifications.unread()

    @action(methods=["get"], detail=False)
    def mark_all_as_read(self, request):
        """Отметить все уведомления пользователя как прочтенные."""
        request.user.notifications.mark_all_as_read()
        return Response(
            {"message": "Уведомления отмечены как прочтенные."},
            status=status.HTTP_200_OK,
        )
