from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.serializers.task import TaskSerializer
from ipr.models import IPR

User = get_user_model()


class IPRSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "creator",
            "executor",
            "creation_date",
            "start_date",
            "end_date",
            "status",
            "tasks",
        )
        model = IPR
