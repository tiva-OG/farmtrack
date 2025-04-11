from django.urls import path

from .views import (
    AnalyticsInfoView,
    AnalyticsReportView,
    DashboardInfoView,
    SalesExpensesInfoView,
    SalesExpensesLossView,
    preview_email,
)


urlpatterns = [
    path("dashboard/", DashboardInfoView.as_view(), name="dashboard_info"),
    path("analytics/", AnalyticsInfoView.as_view(), name="analytics_info"),
    path("analytics/report/", AnalyticsReportView.as_view(), name="analytics_report"),
    path("sales-expenses/", SalesExpensesInfoView.as_view(), name="sales_expenses_info"),
    path("multiple-chart/", SalesExpensesLossView.as_view(), name="sales_expenses_loss"),
    path("preview-email/", preview_email, name="preview_email"),
]
