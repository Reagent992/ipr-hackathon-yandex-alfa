from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Task
