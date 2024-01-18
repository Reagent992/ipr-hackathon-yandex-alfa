from models import IPR
from rest_framework import viewsets
from serializers import IPRSerializer

from django.db.models import Count


class IPRViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        query = IPR.objects.select_related("executor", "creator").annotate(tasks_done=Count("executor__task"))
        return query