from django.contrib import admin

from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "creationdate",
                    "startdate", "enddate", "status", "type")


admin.site.register(Task, TaskAdmin)
