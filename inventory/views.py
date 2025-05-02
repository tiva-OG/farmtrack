from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import FeedActivity, LivestockActivity
from .serializers import FeedActivitySerializer, LivestockActivitySerializer


# =========================== FEED ACTIVITY ===========================


class FeedActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "action", "entry_date"]

    def get_queryset(self):
        user = self.request.user
        return FeedActivity.objects.filter(user=user).exclude(action="initial").order_by("-entry_date")

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            serializer.save(user=user)
            return Response({"detail": "Feed activity entry successful."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FeedActivity.objects.filter(user=user).exclude(action="initial")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            return Response({"detail": "Initial feed activity cannot be edited."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            return Response({"detail": "Initial feed activity cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"detail": "Feed activity deleted successfully."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


# =========================== LIVESTOCK ACTIVITY ===========================


class LivestockActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = LivestockActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "action", "entry_date"]

    def get_queryset(self):
        user = self.request.user
        return LivestockActivity.objects.filter(user=user).exclude(action="initial").order_by("-entry_date")

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            serializer.save(user=user)
            return Response({"detail": "Livestock activity entry successful."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LivestockActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LivestockActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LivestockActivity.objects.filter(user=user).exclude(action="initial")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            return Response({"detail": "Initial livestock activity cannot be edited."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_locked:
            return Response({"detail": "Initial livestock activity cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"detail": "Livestock activity deleted successfully."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
