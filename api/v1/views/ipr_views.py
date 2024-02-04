from django.db.models import Value
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.filters import IPRFilter
from api.v1.permissions import TeamBossPermission
from api.v1.serializers.api.ipr_serializers import (
    IPRSerializer,
    IPRSerializerPost,
    IPRStatusSerializer,
)
from core.statuses import Status
from ipr.models import IPR


@extend_schema(tags=["ИПР"])
@extend_schema_view(
    list=extend_schema(
        summary="Список ИПР",
        description=(
            "<ul><h3>По умолчанию выдает список ИПР пользователя отправившего"
            " запрос на данный эндпоинт</h3><li>"
            "Руководителю команды доступна фильтрация по id исполнителя ИПР"
            " <code>./?user_id=1</code></li>"
        ),
    ),
    retrieve=extend_schema(summary="ИПР пользователя"),
    create=extend_schema(
        summary="Создание ИПР",
        responses=IPRSerializer,
    ),
    partial_update=extend_schema(
        summary="Частичное обновление ИПР",
        responses=IPRSerializer,
    ),
)
class IPRViewSet(ModelViewSet):
    serializer_class = IPRSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IPRFilter
    http_method_names = ["get", "post", "patch", "head", "options", "delete"]

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

    @extend_schema(
        summary="Подробный статус выполнения ИПР",
        description=(
            "В поле <i><b>progress<b><i> "
            "лежит процентное содержание выполненных задач."
        ),
    )
    @action(
        detail=True,
        methods=["get"],
    )
    def status(self, request, pk):
        """Дополнительный эндпоинт и View-функция
        для отображения прогресса выполнения ИПР"""
        ipr = get_object_or_404(IPR, id=pk)
        tasks_not_canceled = ipr.tasks.exclude(status=Status.CANCEL).count()
        tasks_is_complete = ipr.tasks.filter(status=Status.COMPLETE).count()
        progress = 0
        if tasks_not_canceled > 0:
            progress = 100 / tasks_not_canceled * tasks_is_complete
        query = IPR.objects.annotate(progress=Value(progress)).get(id=pk)
        context = {
            "request": request,
        }
        serializer = IPRStatusSerializer(query, context=context)
        return Response(serializer.data)
