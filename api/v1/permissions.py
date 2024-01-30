from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions

User = get_user_model()


class TeamBossPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        executor_id = view.kwargs.get("user_id")
        executor = get_object_or_404(User, id=executor_id)
        if (
            user.is_authenticated
            and user.team == executor.team
            and user.is_boss()
        ):
            return True
        return False
