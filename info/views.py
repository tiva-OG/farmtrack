from decimal import Decimal
from datetime import timedelta, date

from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from inventory.models import Feed, Livestock
from sales_expenses.models import SalesExpenses
from .serializers import DashboardInfoSerializer, AnalyticsInfoSerializer


@csrf_exempt
def check_app(request):
    return Response({"message": "ok", "message": "Backend is LIVE!"}, status=status.HTTP_200_OK)


# DASHBOARD info:
# feed stock (w/ low_stock_threshold);
# fish_count && poultry_count;
# total_sales
# sales_trend for 14 days && last 3 inventory entries


def get_total_quantity(model, user, name, action):
    return (
        model.objects.filter(
            farmer=user,
            name__iexact=name,
            action__iexact=action,
        ).aggregate(
            total=Sum("quantity")
        )["total"]
        or 0
    )


def get_total_cost(user, record_type):
    return SalesExpenses.objects.filter(farmer=user, record_type__iexact=record_type).aggregate(total=Sum("cost"))["total"] or 0


def calculate_feed_data(user, livestock_types):
    feed_info = []

    for livestock in livestock_types:
        name = f"{livestock} Feed"
        initial = get_total_quantity(Feed, user, name, "Initial")
        bought = get_total_quantity(Feed, user, name, "Bought")
        consumed = get_total_quantity(Feed, user, name, "Consumed")
        feed_left = (initial + bought) - consumed

        feed_info.append(
            {
                "name": name,
                "initial": initial,
                "bought": bought,
                "consumed": consumed,
                "left": feed_left,
            }
        )

    return feed_info


def calculate_livestock_data(user, livestock_types):
    livestock_count = []

    for livestock in livestock_types:
        initial = get_total_quantity(Livestock, user, livestock, "Initial")
        bought = get_total_quantity(Livestock, user, livestock, "Bought")
        sold = get_total_quantity(Livestock, user, livestock, "Sold")
        dead = get_total_quantity(Livestock, user, livestock, "Dead")
        count = max((initial + bought) - (sold + dead), 0)

        livestock_count.append(
            {
                "name": livestock,
                "initial": initial,
                "bought": bought,
                "sold": sold,
                "dead": dead,
                "count": count,
            }
        )

    return livestock_count


def get_sales_data(user, period):
    today = date.today()
    start_date = today - timedelta(days=period)

    sales_data = (
        SalesExpenses.objects.filter(farmer=user, record_type="Sale", entry_date__range=(start_date, today))
        .annotate(sale_date=TruncDate("entry_date"))
        .values("sale_date")
        .annotate(total=Sum("cost"))
        .order_by("sale_date")
    )

    # map sale_date -> total sales
    sales_map = {sale["sale_date"]: sale["total"] for sale in sales_data}

    # Fill in missing dates with zero sales
    result = []
    for i in range(period + 1):
        day = start_date + timedelta(days=i)
        result.insert(0, {"date": day.strftime("%Y-%m-%d"), "total_sales": Decimal(sales_map.get(day, 0))})

    return result


class DashboardInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        livestock_type = user.livestock_type
        livestock_type = ["Fish", "Poultry"] if livestock_type == "Both" else [livestock_type]

        low_stock_threshold = user.low_stock_threshold
        feed_info = calculate_feed_data(user, livestock_type)
        livestock_count = calculate_livestock_data(user, livestock_type)
        sales_data = get_sales_data(user, period=13)

        info = {
            "low_stock_threshold": low_stock_threshold,
            "feed_info": feed_info,
            "livestock_count": livestock_count,
            "sales_data": sales_data,
        }
        serializer = DashboardInfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnalyticsInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        livestock_type = user.livestock_type
        livestock_type = ["Fish", "Poultry"] if livestock_type == "Both" else [livestock_type]

        feed_data = calculate_feed_data(user, livestock_type)
        feed_consumption = [{"name": data["name"], "consumed": data["consumed"]} for data in feed_data]

        livestock_data = calculate_livestock_data(user, livestock_type)
        livestock_sales = [{"name": data["name"], "sold": data["sold"]} for data in livestock_data]

        livestock_mortality = []
        for data in livestock_data:
            total = data["initial"] + data["bought"]
            mortality = (data["dead"] / total) * 100 if total else 0
            livestock_mortality.append({"name": data["name"], "mortality": mortality})

        info = {
            "feed_consumption": feed_consumption,
            "livestock_sales": livestock_sales,
            "livestock_mortality": livestock_mortality,
        }
        serializer = AnalyticsInfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesExpensesInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_sales = get_total_cost(user, "Sale")
        total_expenses = get_total_cost(user, "Expense")
        total_income = total_sales - total_expenses

        info = {"total_sales": total_sales, "total_expenses": total_expenses, "total_income": total_income}

        return Response(info, status=status.HTTP_200_OK)
