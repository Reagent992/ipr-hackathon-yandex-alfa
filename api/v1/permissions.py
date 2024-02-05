from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from tasks.models import Task

User = get_user_model()


class TeamBossPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == "POST":
            executor_id = request.data.get("executor")
            executor = get_object_or_404(User, id=executor_id)
            if (
                user.is_authenticated
                and user.is_boss()
                and user.managed_team == executor.team
            ):
                return True
            return False
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        if isinstance(obj, Task):
            if (
                request.method == "PATCH"
                and "status" in request.data
                and request.data["status"] == "complete"
            ):
                return request.user == obj.executor
        return False
