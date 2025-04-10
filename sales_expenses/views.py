from decimal import Decimal
from datetime import timedelta, date

from django.db.models import Sum
from django.db.models.functions import TruncDate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from .models import SalesExpenses
from .serializers import SalesExpensesSerializer, SalesTrendSerializer


class SalesExpensesFilter(FilterSet):
    record_type = filters.CharFilter(field_name="record_type", lookup_expr="iexact")
    item = filters.CharFilter(field_name="item", lookup_expr="iexact")
    entry_date = filters.DateFromToRangeFilter()

    class Meta:
        model = SalesExpenses
        fields = ["record_type", "item", "entry_date"]


class SalesExpensesListView(ListAPIView):
    serializer_class = SalesExpensesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SalesExpensesFilter
    ordering_fields = ["entry_date", "cost"]
    ordering = ["-entry_date"]

    def get_queryset(self):
        user = self.request.user
        return SalesExpenses.objects.filter(farmer=user)


class SalesTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()
        start_date = today - timedelta(days=13)  # last 14 days including today

        # query only `Sale` entries for this user
        sales_data = (
            SalesExpenses.objects.filter(farmer=user, record_type="Sale", entry_date__range=(start_date, today))
            .annotate(sale_date=TruncDate("entry_date"))
            .values("sale_date")
            .annotate(total=Sum("cost"))
            .order_by("sale_date")
        )

        # build a lookup dictionary of date -> total cost
        sales_map = {sale["sale_date"]: sale["total"] for sale in sales_data}

        # construct full timeline with zeros where necessary
        result = []
        for i in range(13):
            day = start_date + timedelta(days=i)
            result.append({"date": day.strftime("%Y-%m-%d"), "total_sales": Decimal(sales_map.get(day, 0))})

        serializer = SalesTrendSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
