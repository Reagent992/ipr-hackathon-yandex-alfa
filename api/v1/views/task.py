from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.v1.serializers.task import TaskSerializer
from tasks.models import Task

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if self.request.query_params:
            return Task.objects.filter(
                executor=self.request.query_params.get("user_id")
            )
        return Task.objects.filter(executor=self.request.user)

    def perform_create(self, serializer):
        executor_id = self.request.data.get("executor")
        executor = get_object_or_404(User, pk=executor_id)
        serializer.save(creator=self.request.user, executor=executor)
