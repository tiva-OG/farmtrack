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
        return Notification.objects.filter(user=user)


class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            notification = Notification.objects.get(pk=pk, user=user)
            notification.is_read = True
            notification.save()

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

    def delete(self, request, pk):
        user = request.user
        try:
            notification = Notification.objects.get(pk=pk, user=user)
            notification.delete()

            return Response({"detail": "Notification deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification does not exist."}, status=status.HTTP_400_BAD_REQUEST)
