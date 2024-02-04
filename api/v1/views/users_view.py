from django.db.models import F, Value
from django.db.models.functions import Coalesce, Concat
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as UserViewSetFromDjoser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
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
    search_fields = (
        "last_name",
        "first_name",
        "patronymic",
        "position__name",
    )
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    ordering_fields = ("full_name", "position_name")

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.annotate(
            full_name=Coalesce(
                Concat(
                    "last_name",
                    Value(" "),
                    "first_name",
                    Value(" "),
                    "patronymic",
                ),
                Value(""),
            ),
            position_name=Coalesce(F("position__name"), Value("")),
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
