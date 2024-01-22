from djoser.serializers import UserSerializer

from users.models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

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
