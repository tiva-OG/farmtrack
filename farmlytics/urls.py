from django.urls import path
from .views import (
    DashboardView,
    AnalyticsView,
    SalesExpensesView,
)


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("sales-and-expenses/", SalesExpensesView.as_view(), name="sales-and-expenses"),
]
