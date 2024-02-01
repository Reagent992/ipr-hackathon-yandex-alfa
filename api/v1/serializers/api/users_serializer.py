from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Position

User = get_user_model()


class PositionsSerializer(ModelSerializer):
    """Сериализатор должностей."""

    class Meta:
        model = Position
        fields = ("name",)


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    position = serializers.CharField(source="position.name", read_only=True)
    ruled_team = serializers.IntegerField(
        source="managed_team.id", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "position",
            "is_boss",
            "date_joined",
            "last_login",
            "userpic",
            "ruled_team",
            "team",
        )
