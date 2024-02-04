from django.contrib.auth import get_user_model
from rest_framework import serializers

from tasks.models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "creator",
            "executor",
            "creation_date",
            "start_date",
            "end_date",
            "status",
            "ipr",
            "skill",
        )
        model = Task


class TaskSerializerPost(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "creator",
            "executor",
            "creation_date",
            "start_date",
            "end_date",
            "status",
            "ipr",
            "skill",
        )
        model = Task
