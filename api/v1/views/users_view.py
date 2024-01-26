from django.conf import settings
from django.db.models import CharField, ExpressionWrapper, F, Value
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as UserViewSetFromDjoser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.v1.filters import CustomFilter
from api.v1.serializers.api.users_serializer import (
    CustomUserSerializer,
    PositionsSerializer,
)
from users.models import Position


@extend_schema(tags=["Пользователи"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список пользователей."),
        description=(
            "<ul><h3>Поддерживается:</h3><li>Сортировка по имени "
            "<code>./?ordering=full_name</code>  "
            "и должности <code>./?ordering=-position_name</code></li>"
            "<li>Поиск по ФИО и должности <code>./?search=Мирон</code></li>"
            "<li>Ограничение pagination <code>./?limit=5</code>.</li>"
            "<li>Фильтр по id команды <code>./?team=1</code></li>"
            "<li>Фильтр по id команды и отсутствию ИПР "
            "<code>./?team=1&no_ipr=true</code></li></ul>"
        ),
    ),
    retrieve=extend_schema(summary="Профиль пользователя"),
    me=extend_schema(summary="Текущий пользователь"),
)
class UserViewSet(UserViewSetFromDjoser):
    """Пользователи."""

    filterset_class = CustomFilter
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        OrderingFilter,
    )
    if settings.USE_POSTGRESQL:  # TODO: Проверить.
        search_fields = (
            "@last_name",
            "@first_name",
            "@patronymic",
            "@position__name",
        )
    else:
        search_fields = (
            "last_name",
            "first_name",
            "patronymic",
            "position__name",
        )
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ["get", "head", "options"]
    ordering_fields = ("full_name", "position_name")

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.annotate(
            full_name=ExpressionWrapper(
                F("last_name") + F("first_name") + F("patronymic"),
                output_field=CharField(),
            ),
            position_name=ExpressionWrapper(
                F("position__name") if F("position__name") else Value(""),
                output_field=CharField(),
            ),
        )

    @extend_schema(
        summary="Список должностей",
    )
    @action(
        methods=["get"], detail=False, serializer_class=PositionsSerializer
    )
    def positions(self, request):
        """Список должностей."""
        queryset = Position.objects.all()
        serializer = PositionsSerializer(queryset, many=True)
        return Response(serializer.data)
