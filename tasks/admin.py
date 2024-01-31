from django.contrib import admin

from tasks.models import Skill, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Создатель и исполнитель", {"fields": ("creator", "executor")}),
        (
            "Информация о задаче",
            {
                "fields": (
                    "name",
                    "description",
                    "ipr",
                    "status",
                    "skill",
                ),
            },
        ),
        ("Даты", {"fields": ("start_date", "end_date")}),
    )

    list_display = (
        "name",
        "get_ipr",
        "limited_description",
        "creation_date",
        "start_date",
        "end_date",
        "status",
        "display_skills",
    )
    filter_horizontal = ("skill",)
    autocomplete_fields = (
        "creator",
        "executor",
        "ipr",
    )
    list_filter = (
        "status",
        "ipr",
        "executor",
        "skill",
    )
    search_fields = (
        "name",
        "description",
        "ipr__title",
        "skill__skill_name",
        "creator__first_name",
        "creator__last_name",
        "creator__patronymic",
        "creator__position__name",
        "executor__first_name",
        "executor__last_name",
        "executor__patronymic",
        "executor__position__name",
    )
    date_hierarchy = "creation_date"
    ordering = ("-creation_date",)

    @admin.display(description="Описание")
    def limited_description(self, obj):
        max_chars = 70
        return (
            (obj.description[:max_chars] + "...")
            if len(obj.description) > max_chars
            else obj.description
        )

    @admin.display(description="Навыки")
    def display_skills(self, obj):
        return ", ".join(
            [skill.skill_name for skill in obj.skill.all() if skill]
        )

    @admin.display(description="ИПР")
    def get_ipr(self, obj):
        return obj.ipr


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("skill_name",)
    search_fields = ("skill_name",)
