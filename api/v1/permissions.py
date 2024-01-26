# from django.shortcuts import get_object_or_404
# from rest_framework import permissions
# from rest_framework.exceptions import PermissionDenied

# from users.models import MiddleUsersTeams, Team, User


# # class BossPermission(permissions.BasePermission):
# #     def has_permission(self, request, view):
# #         user = request.user
# #         executor_id = request.data.get("executor")
# #         if user.is_authenticated:
# #             team_id = get_object_or_404(Team, boss_id=request.user.id)
# #             return get_object_or_404(
# #                 MiddleUsersTeams,
# #                 team_id=team_id,
# #                 user_id=executor_id,
# #             )
# #         return False
