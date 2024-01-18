from models import IPR
from rest_framework import serializers


class IPRSerializer(serializers.ModelSerializer):
    executor = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = IPR
        fields = "__all__"
