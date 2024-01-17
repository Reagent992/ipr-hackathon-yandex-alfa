from django.contrib import admin

from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_create',
                    'deadline', 'status', 'type')


admin.site.register(Task, TaskAdmin)
