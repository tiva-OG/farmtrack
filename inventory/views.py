from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, exceptions, viewsets, filters

from .models import Feed, Livestock
from .serializers import FeedSerializer, LivestockSerializer


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "action", "entry_date"]  # entry_date will match string-formatted dates


# CREATE new & RETRIEVE all feed records
class FeedListCreate(generics.ListCreateAPIView):
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Feed.objects.filter(farmer=user).exclude(action="Initial")

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(farmer=self.request.user)
            return Response({"message": "Record entered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# GET, PATCH, or DELETE feed record
class FeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Feed.objects.filter(farmer=user).exclude(action="Initial")

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            return Response({"error": "Initial inventory records cannot be edited."}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.is_locked:
                return Response({"error": "Initial inventory records cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)

            self.perform_destroy(instance)
            return Response(
                {"message": f"{instance.name} record entered on {instance.entry_date} deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except exceptions.NotFound:
            return Response({"error": "Inventory not found."}, status=status.HTTP_404_NOT_FOUND)


class LivestockViewSet(viewsets.ModelViewSet):
    queryset = Livestock.objects.all()
    serializer_class = LivestockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "action", "entry_date"]  # entry_date will match string-formatted dates


# CREATE new & RETRIEVE all livestock records
class LivestockListCreate(generics.ListCreateAPIView):
    serializer_class = LivestockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Livestock.objects.filter(farmer=user).exclude(action="Initial")

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(farmer=self.request.user)
            return Response({"message": "Record entered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# GET, PATCH, or DELETE livestock record
class LivestockDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LivestockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Livestock.objects.filter(farmer=user).exclude(action="Initial")

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            return Response({"error": "Initial inventory records cannot be edited."}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.is_locked:
                return Response({"error": "Initial inventory records cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)

            self.perform_destroy(instance)
            return Response(
                {"message": f"{instance.name} record entered on {instance.entry_date} deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except exceptions.NotFound:
            return Response({"error": "Inventory not found."}, status=status.HTTP_404_NOT_FOUND)
