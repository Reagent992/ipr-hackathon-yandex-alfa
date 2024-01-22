from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username_custom(username: str):
    """Запрет определенных никнеймов."""
    if username.lower() in settings.RESTRICTED_USERNAMES:
        raise ValidationError(
            f"Имя пользователя {username} запрещено.",
        )
