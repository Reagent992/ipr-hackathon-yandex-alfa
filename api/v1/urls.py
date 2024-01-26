from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.v1.views.ratings_view import IPRRatingCreateView, TaskRatingCreateView
from api.v1.views.task import TaskViewSet
from api.v1.views.users_view import UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register("tasks", TaskViewSet, basename="tasks")
v1_router.register("users", UserViewSet)

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls.jwt")),
    path(
        "tasks/<int:task_id>/ratings/",
        TaskRatingCreateView.as_view(),
        name="task-rating-create",
    ),
    path(
        "iprs/<int:ipr_id>/ratings/",
        IPRRatingCreateView.as_view(),
        name="ipr-rating-create",
    ),
]

#  ---------------------------------------------------------------------SWAGGER
urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
