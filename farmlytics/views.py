from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from farmlytics.chart.sales_trend import generate_sales_trend
from farmlytics.chart.profit_trend import generate_profit_trend
from farmlytics.chart.expenses_trend import generate_expenses_trend
from farmlytics.reports.sales_report import generate_sales_report
from farmlytics.reports.profit_report import generate_profit_report
from farmlytics.reports.expenses_report import generate_expenses_report
from farmlytics.reports.inventory_report import generate_inventory_summary, generate_inventory_report


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        feed_low_stock_threshold = user.feed_low_stock_threshold
        livestock_types = ["fish", "poultry"] if user.livestock_type == "both" else [user.livestock_type]

        timeframe = request.query_params.get("timeframe", "monthly")

        # current feed-quantity for each livestock
        # current livestock-quantity for each livestock
        # livestock mortality for each livestock
        inventory_summary = generate_inventory_summary(user, livestock_types)

        # total revenue for current timeframe
        sales_report = generate_sales_report(user, timeframe)

        # sales vs expense for 14-day period (rolling)
        profit_trend = generate_profit_trend(user)

        data = {
            "feed_low_stock_threshold": feed_low_stock_threshold,
            "total_revenue": sales_report["total_revenue"],
            "profit_trend": profit_trend,
            **inventory_summary,
        }

        return Response(data, status=status.HTTP_200_OK)


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        livestock_types = ["fish", "poultry"] if user.livestock_type == "both" else [user.livestock_type]

        TIMEFRAME = "monthly"
        MODE = "calendar"

        # feed consumption
        # livestock sales
        # mortality rate
        inventory_report = generate_inventory_report(user, livestock_types, TIMEFRAME, MODE)
        inventory_summary = generate_inventory_summary(user, livestock_types)

        # sales vs purchase for 1-month[4-weeks] (rolling)
        profit_trend = generate_profit_trend(user, TIMEFRAME, MODE)
        # profit_trend = generate_sales_trend(user, timeframe, mode)

        data = {
            "feed_consumption": inventory_report["feed_consumed_quantity"],
            "livestock_sales": inventory_report["livestock_sold_quantity"],
            "livestock_mortality": inventory_summary["livestock_mortality"],
            "profit_trend": profit_trend["profit"],
        }

        return Response(data, status=status.HTTP_200_OK)


class SalesExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        livestock_types = ["fish", "poultry"] if user.livestock_type == "both" else [user.livestock_type]

        TIMEFRAME = "weekly"

        profit_report = generate_profit_report(user)
        inventory_report = generate_inventory_report(user, livestock_types)
        sales_trend = generate_sales_trend(user, TIMEFRAME)

        data = {
            **profit_report,
            **inventory_report,
            **sales_trend,
        }

        return Response(data, status=status.HTTP_200_OK)
