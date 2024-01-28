from django.contrib import admin

from ratings.models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "content_type",
        "object_id",
        "content_object",
        "user",
        "rating",
        "created_at",
    )


admin.site.register(Rating, RatingAdmin)
