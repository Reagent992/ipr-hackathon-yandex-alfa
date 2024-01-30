from django.contrib.auth import get_user_model
from django_filters.rest_framework import BooleanFilter, CharFilter, FilterSet

from ipr.models import IPR

User = get_user_model()


class CustomFilter(FilterSet):
    no_ipr = BooleanFilter(method="filter_no_ipr", label="No IPR")

    class Meta:
        model = User
        fields = ("team",)

    def filter_no_ipr(self, queryset, name, value):
        if value:
            return queryset.filter(ipr=None)
        return queryset


class IPRFilter(FilterSet):
    executor = CharFilter()

    class Meta:
        model = IPR
        fields = ["executor"]
