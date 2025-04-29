from django.urls import path

from .views import NotificationListView, NotificationDestroyView, NotificationMarkReadView, NotificationMarkAllReadView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<str:pk>/delete/", NotificationDestroyView.as_view(), name="notification-delete"),
    path("<str:pk>/mark-as-read/", NotificationMarkReadView.as_view(), name="mark-as-read"),
    path("mark-all-read/", NotificationMarkAllReadView.as_view(), name="mark-all-read"),
]
