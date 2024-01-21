from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField

from tasks.models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    creator = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        exclude = ("creation_date",)
        model = Task
