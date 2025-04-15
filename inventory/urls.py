from django.urls import path
from .views import (
    FeedActivityListCreateView,
    FeedActivityRetrieveUpdateDestroyView,
    LivestockActivityListCreateView,
    LivestockActivityRetrieveUpdateDestroyView,
)


urlpatterns = [
    # Feed Activity
    path("feed/", FeedActivityListCreateView.as_view(), name="feed_list_create"),
    path("feed/<int:pk>/", FeedActivityRetrieveUpdateDestroyView.as_view(), name="feed_detail"),
    # Livestock Activity
    path("livestock/", LivestockActivityListCreateView.as_view(), name="livestock_list_create"),
    path("livestock/<int:pk>/", LivestockActivityRetrieveUpdateDestroyView.as_view(), name="livestock_detail"),
]
