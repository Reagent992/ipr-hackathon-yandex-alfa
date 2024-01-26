from rest_framework import generics, status
from rest_framework.response import Response

from api.v1.serializers.ratings import RatingSerializer
from ipr.models import IPR
from ratings.models import Rating
from tasks.models import Task


class TaskRatingCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return Rating.objects.filter(
            content_type__model="task", object_id=task_id
        )

    def post(self, request, *args, **kwargs):
        task_id = self.kwargs.get("task_id")
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content_object=task, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IPRRatingCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        ipr_id = self.kwargs.get("ipr_id")
        return Rating.objects.filter(
            content_type__model="ipr", object_id=ipr_id
        )

    def post(self, request, *args, **kwargs):
        ipr_id = self.kwargs.get("ipr_id")
        try:
            ipr = IPR.objects.get(id=ipr_id)
        except IPR.DoesNotExist:
            return Response(
                {"error": "IPR not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content_object=ipr, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
