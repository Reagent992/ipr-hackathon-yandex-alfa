from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import TokenProxy

from users.models import Position, Team, User

admin.site.unregister(TokenProxy)
admin.site.unregister(Group)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Команда."""

    list_display = (
        "name",
        "boss",
        "created_at",
    )
    search_fields = (
        "name",
        "boss__last_name",
        "boss__first_name",
        "boss__patronymic",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = ("boss",)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Пользователи."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "username",
                    "position",
                    "team",
                    "userpic",
                    "image_preview",
                )
            },
        ),
        (
            "Привилегии",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "username",
                    "userpic",
                    "position",
                    "team",
                )
            },
        ),
    )

    list_display = (
        "name",
        "position",
        "team",
        "email",
        "userpic_thumbnail",
    )
    search_fields = (
        "email",
        "last_name",
        "first_name",
        "patronymic",
        "position",
    )
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)
    readonly_fields = ("image_preview",)
    autocomplete_fields = ("position", "team")

    @admin.display(description="ФИО")
    def name(self, obj: User) -> str:
        """ФИО пользователя."""
        return obj.get_full_name()

    @admin.display(description="Аватар")
    def userpic_thumbnail(self, obj: User):
        """Малый аватар в общем списке пользователей."""
        return (
            mark_safe(f'<img src={obj.userpic.url} width="80">')
            if obj.userpic
            else None
        )

    @admin.display(description="Текущий аватар")
    def image_preview(self, obj: User):
        """Большой аватар в редактирование пользователя."""
        return (
            mark_safe(f'<img src="{obj.userpic.url}" width="275">')
            if obj.userpic
            else "Аватар не загружен."
        )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Должности сотрудников."""

    list_display = ("name",)
    search_fields = ("name",)
