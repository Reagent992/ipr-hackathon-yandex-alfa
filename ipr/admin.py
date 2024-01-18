from models import IPR

from django.contrib import admin


@admin.register(IPR)
class IPRAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "creator",
        "creation_date",
        "start_date",
        "end_date",
        "status",
        "executor",
        "task",
        "comment",
    )
    search_fields = ("title", "task", "executor", "author", "comment")
    list_filter = (
        "creation_date",
        "start_date",
        "status",
        "creator",
        "executor",
        "title",
    )
    ordering = ("-creation_date",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("creator", "executor")
