from django.contrib.auth import get_user_model
from rest_framework import viewsets

from api.v1.serializers.api.task_serializer import (
    TaskSerializer,
    TaskSerializerPost,
)
from tasks.models import Task

User = get_user_model()


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
        return self.request.user.tasks.all()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return TaskSerializerPost
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
