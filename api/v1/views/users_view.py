from djoser.views import UserViewSet as UserViewSetFromDjoser
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination

from api.v1.serializers.api.users_serializer import CustomUserSerializer


@extend_schema(
    responses=CustomUserSerializer,
    description="Пользователи.",
)
class UserViewSet(UserViewSetFromDjoser):
    """Пользователи."""

    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
