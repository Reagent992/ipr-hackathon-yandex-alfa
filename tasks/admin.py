from django.contrib import admin

from tasks.models import Task, Skill


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "creationdate",
                    "startdate", "enddate", "status", "display_skills")
    
    def display_skills(self, obj):
        return ', '.join([skill.name for skill in obj.skill.all()])


class SkillAdmin(admin.ModelAdmin):
    list_display = ['skill_name']


admin.site.register(Skill, SkillAdmin)
admin.site.register(Task, TaskAdmin)
