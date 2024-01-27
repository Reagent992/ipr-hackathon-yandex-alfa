from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """Добавление signals.py."""
        try:
            import core.signals  # noqa
        except ImportError:
            pass
