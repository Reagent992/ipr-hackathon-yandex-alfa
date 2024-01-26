from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from tasks.models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    creator = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = (
            "name",
            "description",
            "creator",
            "creation_date",
            "start_date",
            "end_date",
            "status",
        )
        model = Task
