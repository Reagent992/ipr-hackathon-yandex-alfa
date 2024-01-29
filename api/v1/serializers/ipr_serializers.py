from django.contrib.auth import get_user_model
from rest_framework import serializers

from ipr.models import IPR

User = get_user_model()


class IPRSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    executor = serializers.RelatedField(read_only=True)

    class Meta:
        fields = (
            "title",
            "creator",
            "creation_date",
            "start_date",
            "end_date",
            "status",
            "executor",
        )
        model = IPR
