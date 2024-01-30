# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from rest_framework import permissions

# from users.models import MiddleUsersTeams, Team

# User = get_user_model()

# TODO: refactor
# class BossPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         executor_id = request.data.get("executor")
#         if (
#             user.is_authenticated
#             and request.method in permissions.SAFE_METHODS
#         ):
#             return True
#         if user.is_authenticated:
#             team_id = get_object_or_404(Team, boss_id=request.user.id)
#             if MiddleUsersTeams.objects.filter(
#                 MiddleUsersTeams,
#                 team_id=team_id,
#                 user_id=executor_id,
#             ):
#                 return True
#         return False


# class TeamBossPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         executor_id = view.kwargs.get("user_id")
#         executor = get_object_or_404(User, id=executor_id)
#         if (
#             user.is_authenticated
#             and user.get_team() == executor.get_team()
#             and user.is_boss()
#         ):
#             return True
#         return False
