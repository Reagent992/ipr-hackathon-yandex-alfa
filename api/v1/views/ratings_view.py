from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.v1.serializers.ratings import RatingSerializer
from ipr.models import IPR
from ratings.models import Rating
from tasks.models import Task


class RatingCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    content_model = None

    def get_content_object(self):
        object_id = self.kwargs.get(f"{self.content_model}_id")
        return get_object_or_404(self.content_model, id=object_id)

    def get_queryset(self):
        content_object = self.get_content_object()
        return Rating.objects.filter(
            content_type__model=self.content_model, object_id=content_object.id
        )

    def post(self, request, *args, **kwargs):
        content_object = self.get_content_object()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                content_object=content_object, user=self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskRatingCreateView(RatingCreateListView):
    content_model = Task


class IPRRatingCreateView(RatingCreateListView):
    content_model = IPR
