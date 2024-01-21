from typing import Optional

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from users.models import MiddleUsersTeams, Team, User

admin.site.unregister(Group)


class MiddleUsersTeamsInline(admin.TabularInline):
    """Дополнительное поле для добавления участников в команду."""

    model = MiddleUsersTeams
    extra = 1
    autocomplete_fields = ("user",)


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
    inlines = [MiddleUsersTeamsInline]
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = ("boss",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи."""

    exclude = (
        "last_login",
        "date_joined",
        "groups",
        "user_permissions",
        "is_staff",
    )
    list_display = (
        "name",
        "position",
        "team_name",
        "email",
        "userpic_thumbnail",
    )
    search_fields = (
        "email",
        "last_name",
        "first_name",
        "patronymic",
    )
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)
    readonly_fields = ("image_preview",)

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

    @admin.display(description="Команда")
    def team_name(self, user: User) -> Optional[str]:
        return user.get_team().name if user.get_team() else None
