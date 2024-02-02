from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions

User = get_user_model()


class TeamBossPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        executor_id = request.data.get("executor")
        executor = get_object_or_404(User, id=executor_id)
        user = request.user
        if (
            user.is_authenticated
            and user.is_boss()
            and user.managed_team == executor.team
        ):
            return True
        return False
