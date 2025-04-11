from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from sales_expenses.services import get_monthly_net_income, get_weekly_sales_purchases
from .serializers import DashboardInfoSerializer, AnalyticsInfoSerializer
from .services import (
    calculate_feed_data,
    calculate_livestock_data,
    get_sales_data,
    get_total_cost,
    send_analytics_report,
)

from django.shortcuts import render


def preview_email(request):
    user = {"first_name": "Tiva"}
    weekly_data = [
        {"week": "Week 1", "sales": "₦20,000", "purchases": "₦10,000"},
        {"week": "Week 2", "sales": "₦25,000", "purchases": "₦15,000"},
        {"week": "Week 3", "sales": "₦30,000", "purchases": "₦18,000"},
        {"week": "Week 4", "sales": "₦22,000", "purchases": "₦12,000"},
    ]
    monthly_data = [
        {"month": "Nov", "net_income": "₦80,000"},
        {"month": "Dec", "net_income": "₦100,000"},
        {"month": "Jan", "net_income": "₦90,000"},
        {"month": "Feb", "net_income": "₦110,000"},
        {"month": "Mar", "net_income": "₦95,000"},
        {"month": "Apr", "net_income": "₦105,000"},
    ]
    return render(
        request,
        "emails/password_reset.html",
        {
            "user": user,
            "weekly_data": weekly_data,
            "monthly_data": monthly_data,
        },
    )


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


class AnalyticsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        weekly_data = get_weekly_sales_purchases(user, weeks=4)
        monthly_data = get_monthly_net_income(user, months=6)

        try:
            send_analytics_report(user, weekly_data, monthly_data)
            return Response({"message": "Analytics report has been sent to email"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to send report: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
