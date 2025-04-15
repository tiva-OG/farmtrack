from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, exceptions
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
        return FeedActivity.objects.filter(user=user).order_by("-entry_date")

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            serializer.save(user=user)
            return Response({"detail": "Feed activity entry successful."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FeedActivity.objects.filter(user=user)


# =========================== LIVESTOCK ACTIVITY ===========================


class LivestockActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = LivestockActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "action", "entry_date"]

    def get_queryset(self):
        user = self.request.user
        return LivestockActivity.objects.filter(user=user).order_by("-entry_date")

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            serializer.save(user=user)
            return Response({"detail": "Livestock activity entry successful."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LivestockActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LivestockActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LivestockActivity.objects.filter(user=user)
