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
from core.statuses import Status
from ipr.models import IPR


class IPRViewSet(ModelViewSet):
    serializer_class = IPRSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IPRFilter
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if not self.request.query_params and self.action == "list":
            return IPR.objects.filter(executor=self.request.user)
        return IPR.objects.select_related("executor", "creator")

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return IPRSerializerPost
        return IPRSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = [TeamBossPermission]
        return super(IPRViewSet, self).get_permissions()

    @action(
        detail=True,
        methods=["get"],
    )
    def status(self, request, pk):
        """Дополнительный эндпоинт и View-функция
        для отображения прогресса выполнения ИПР"""
        ipr = get_object_or_404(IPR, id=pk)
        tasks_without_trail = ipr.tasks.exclude(status=Status.TRAIL).count()
        tasks_is_complete = ipr.tasks.filter(status=Status.COMPLETE).count()
        progress = tasks_without_trail / 100 * tasks_is_complete

        context = {
            "request": request,
            "progress": progress,
        }
        serializer = IPRSerializer(ipr, context=context)
        return Response(serializer.data)
