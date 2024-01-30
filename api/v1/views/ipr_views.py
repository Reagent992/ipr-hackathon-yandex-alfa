from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.filters import IPRFilter
from api.v1.permissions import TeamBossPermission
from api.v1.serializers.api.ipr_serializers import (
    IPRSerializer,
    IPRSerializerPost,
)
from core.statuses_for_ipr_tests import Status
from ipr.models import IPR
from users.models import User


class IPRViewSet(ModelViewSet):
    serializer_class = IPRSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IPRFilter

    class Meta:
        ordering = ["-creation_date"]

    def get_queryset(self):
        return IPR.objects.select_related("executor", "creator")

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PATCH":
            return IPRSerializerPost
        return IPRSerializer

    def perform_create(self, serializer):
        executor_id = self.kwargs.get("user_id")
        executor = get_object_or_404(User, id=executor_id)
        serializer.save(creator=self.request.user, executor=executor)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [TeamBossPermission]
        return super(IPRViewSet, self).get_permissions()

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def status(self, request, ipr_id):
        """Дополнительный эндпоинт и View-функция
        для отображения прогресса выполнения ИПР"""
        ipr = get_object_or_404(IPR, id=ipr_id)
        tasks_without_trail = ipr.tasks.exclude(status=Status.TRAIL).count()
        tasks_is_complete = ipr.tasks.filter(status=Status.COMPLETE).count()
        progress = tasks_without_trail / 100 * tasks_is_complete

        context = {
            "request": request,
            "progress": progress,
        }
        serializer = IPRSerializer(ipr, context=context)
        return Response(serializer.data)
