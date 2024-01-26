from rest_framework import serializers

from ratings.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            "id",
            "content_type",
            "object_id",
            "user",
            "rating",
            "created_at",
        ]
        read_only_fields = ["user"]
