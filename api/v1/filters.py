from django.contrib.auth import get_user_model
from django_filters.rest_framework import BooleanFilter, FilterSet

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
