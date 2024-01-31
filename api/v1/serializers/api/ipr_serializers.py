from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.serializers.api.users_serializer import CustomUserSerializer
from api.v1.serializers.task import TaskSerializer
from core.statuses import Status
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
    status = serializers.SerializerMethodField()

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

    def get_status(self, obj):
        if obj.status == Status.IN_PROGRESS and obj.start_date > obj.end_date:
            obj.status = Status.TRAIL
            obj.save()
        return obj.status


class IPRSerializerPost(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    executor = serializers.PrimaryKeyRelatedField(read_only=True)

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
