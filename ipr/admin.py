from django.contrib import admin

from .models import IPR


@admin.register(IPR)
class IPRAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "creator",
        "creation_date",
        "start_date",
        "end_date",
        "status",
        "executor",
    )
    search_fields = ("title", "executor", "author")
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
