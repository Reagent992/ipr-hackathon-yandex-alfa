from rest_framework import viewsets

from tasks.models import Task
from api.v1.serializers.task import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)
