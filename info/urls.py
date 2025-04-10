from django.urls import path

from .views import AnalyticsInfoView, DashboardInfoView, SalesExpensesInfoView, check_app


urlpatterns = [
    path("info/", check_app, name="check_app"),
    path("dashboard/", DashboardInfoView.as_view(), name="dashboard_info"),
    path("analytics/", AnalyticsInfoView.as_view(), name="analytics_info"),
    path("sales-expenses/", SalesExpensesInfoView.as_view(), name="sales_expenses_info"),
]
