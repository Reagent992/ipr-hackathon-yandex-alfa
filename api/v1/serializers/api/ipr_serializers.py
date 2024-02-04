from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.serializers.api.task_serializer import TaskSerializer
from api.v1.serializers.api.users_serializer import CustomUserSerializer
from ipr.models import IPR

User = get_user_model()


class UserSerializer(CustomUserSerializer):
    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "position",
            "userpic",
        )
        model = User


class IPRSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)

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


class IPRSerializerPost(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

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
        )
        model = IPR

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return IPRSerializer(instance, context=context).data


class IPRStatusSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)
    progress = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "creator",
            "executor",
            "start_date",
            "end_date",
            "status",
            "progress",
        )
        model = IPR
