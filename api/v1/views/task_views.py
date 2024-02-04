from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.v1.serializers.api.task_serializer import (
    TaskSerializer,
    TaskSerializerPost,
)
from tasks.models import Task

User = get_user_model()


@extend_schema(tags=["Задачи"])
@extend_schema_view(
    list=extend_schema(
        summary="Список задач", description="Описание списка задач."
    ),
    retrieve=extend_schema(
        summary="Получение задачи", description="Описание получения задачи."
    ),
    create=extend_schema(
        summary="Создание задачи", description="Описание создания задачи."
    ),
    partial_update=extend_schema(
        summary="Частичное обновление задачи",
        description="Описание частичного обновления задачи.",
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

    def get_queryset(self):
        if self.request.query_params.get("user_id"):
            return Task.objects.filter(
                executor=self.request.query_params.get("user_id")
            )
        return Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return TaskSerializerPost
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
