from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    is_boss = serializers.SerializerMethodField()

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
        )

    def get_is_boss(self, user_obj: User) -> bool:
        """Является ли пользователь боссом."""
        return user_obj.is_boss()
