# Send users real-time & scheduled notification for important events like:
# - low stock alerts
# - feed consumption milestones
# - livestock sales or mortality alerts
# - report availability (e.g., "Your Monthly Report is Ready")

# When & How do we trigger notifications?
# - Low Stock Detection: when inventory quantity drops below threshold -> system auto-generates a notification
# - Feed Consumption Events: big milestone in feed consumption
# - Sales/Mortality Events: after a sale is recorded or mortality is recorded -> trigger a notification
# - Scheduled Notifications (Celery Beat later): every month (or any schedule), remind users of important activities

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        is_read = self.request.query_params.get("is_read")
        queryset = Notification.objects.filter(user=user)
        if is_read:
            queryset = queryset.filter(is_read=is_read.lower() == "true")
        return queryset


class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        ids = request.data.get("ids", [])
        try:
            Notification.objects.filter(id__in=ids, user=user).update(is_read=True)
            return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification does not exist."}, status=status.HTTP_400_BAD_REQUEST)


class NotificationMarkAllReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user, is_read=False)
        notifications.update(is_read=True)

        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)


class NotificationDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Notification deleted."}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
