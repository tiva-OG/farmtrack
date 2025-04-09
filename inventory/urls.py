from django.urls import path
from .views import (
    FeedListCreate,
    FeedDetailView,
    LivestockListCreate,
    LivestockDetailView,
)

urlpatterns = [
    path("feed/", FeedListCreate.as_view(), name="feed_list"),
    path("feed/<str:pk>/", FeedDetailView.as_view(), name="feed_detail"),
    path("livestock/", LivestockListCreate.as_view(), name="livestock_list"),
    path("livestock/<str:pk>/", LivestockDetailView.as_view(), name="livestock_detail"),
]
