from django_filters import rest_framework as filters

from ipr.models import IPR


class IPRFilter(filters.FilterSet):
    executor = filters.CharFilter()

    class Meta:
        model = IPR
        fields = ["executor"]
