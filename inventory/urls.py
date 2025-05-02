from django.urls import path
from .views import (
    FeedActivityListCreateView,
    FeedActivityDetailView,
    LivestockActivityListCreateView,
    LivestockActivityDetailView,
)


urlpatterns = [
    # Feed Activity
    path("feed/", FeedActivityListCreateView.as_view(), name="feed-list-create"),
    path("feed/<int:pk>/", FeedActivityDetailView.as_view(), name="feed-detail"),
    # Livestock Activity
    path("livestock/", LivestockActivityListCreateView.as_view(), name="livestock-list-create"),
    path("livestock/<int:pk>/", LivestockActivityDetailView.as_view(), name="livestock-detail"),
]
