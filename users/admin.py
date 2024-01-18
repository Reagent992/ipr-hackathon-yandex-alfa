from typing import Optional

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from users.models import Member, Team, User

admin.site.unregister(Group)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Сотрудники."""

    # TODO: Добавить поиск и фильтрацию.
    list_display = (
        "member",
        "userpic_thumbnail",
        "team",
        "position",
        "joined_at",
    )

    @admin.display(description="Аватар")
    def userpic_thumbnail(self, obj: Member):
        """Маленький аватар пользователя."""
        return (
            mark_safe(f'<img src={obj.member.userpic.url} width="80">')
            if obj.member.userpic
            else None
        )

    # @admin.display(description="Последний ИПР")
    # def get_iprs(self, obj: User) -> str:
    #     # TODO: Вывести ссылку на редактирование последнего IPR.
    #     return ""


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Команда."""

    # TODO: Добавить поиск и фильтрацию.
    # TODO: Добавить текущий ИПР.

    list_display = (
        "name",
        "boss",
        "created_at",
    )


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
    ordering = ("-date_joined",)
    readonly_fields = ("image_preview",)
    # TODO: Добавить поиск и фильтрацию.

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
        return user.get_first_team_name()
