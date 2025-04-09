from django.urls import path

from .views import SalesTrendView, SalesExpensesListView

urlpatterns = [
    path("sales-expenses/", SalesExpensesListView.as_view(), name="sales_expenses_list"),
    path("sales-trend/", SalesTrendView.as_view(), name="sales_trend"),
]
