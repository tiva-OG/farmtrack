from django.urls import path

from .views import SalesTrendView, SalesExpensesListView, AnalyticsChartView

urlpatterns = [
    path("sales-expenses/", SalesExpensesListView.as_view(), name="sales_expenses_list"),
    path("sales-trend/", SalesTrendView.as_view(), name="sales_trend"),
    path("analytics-chart/", AnalyticsChartView.as_view(), name="analytics_chart"),
]
