from typing import Optional

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from users.models import Member, Team, User

admin.site.unregister(Group)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Сотрудники."""

    list_display = (
        "member",
        "userpic_thumbnail",
        "team",
        "position",
        "joined_at",
    )
    list_filter = ("team",)
    search_fields = ("position",)
    date_hierarchy = "joined_at"
    autocomplete_fields = (
        "team",
        "member",
    )

    @admin.display(description="Аватар")
    def userpic_thumbnail(self, obj: Member):
        """Маленький аватар пользователя."""
        return (
            mark_safe(f'<img src={obj.member.userpic.url} width="80">')
            if obj.member.userpic
            else None
        )


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
        "team",
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
        return obj.get_full_name()

    @admin.display(description="Аватар")
    def userpic_thumbnail(self, obj: User):
        """Поле с иконкой картинки."""
        return (
            mark_safe(f'<img src={obj.userpic.url} width="80">')
            if obj.userpic
            else None
        )

    @admin.display(description="Текущий аватар")
    def image_preview(self, obj: User):
        if obj.userpic:
            return mark_safe(f'<img src="{obj.userpic.url}" />')
        return "Аватар не загружен."

    @admin.display(description="Команда")
    def team(self, user: User) -> Optional[str]:
        return user.get_last_team_name()
