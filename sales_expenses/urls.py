from django.urls import path

from .views import SalesTrendView, SalesExpensesListView, SalesExpensesChartView, AnalyticsChartView

urlpatterns = [
    path("sales-expenses/", SalesExpensesListView.as_view(), name="sales_expenses_list"),
    path("sales-trend/", SalesTrendView.as_view(), name="sales_trend"),
    path("sales-expenses-chart/", SalesExpensesChartView.as_view(), name="sales_expenses_chart"),
    path("analytics-chart/", AnalyticsChartView.as_view(), name="analytics_chart"),
]
