from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.v1.views.task import TaskViewSet

v1_router = routers.DefaultRouter()
v1_router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

# ----------------------------------------------------------------------SWAGGER
schema_view = get_schema_view(
    openapi.Info(
        title="IPR API",
        default_version="v1",
        description="Документация для приложения ИПР.",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
