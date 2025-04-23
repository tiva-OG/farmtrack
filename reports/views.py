from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import (
    generate_sales_report,
    generate_expenses_report,
    generate_profit_report,
    generate_trends_report,
)


class SalesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        timeframe = request.query_params.get("timeframe", "monthly")

        data = generate_sales_report(user, timeframe)

        return Response(data, status=status.HTTP_200_OK)


class ExpensesReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        timeframe = request.query_params.get("timeframe", "monthly")

        data = generate_expenses_report(user, timeframe)

        return Response(data, status=status.HTTP_200_OK)


class ProfitReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        timeframe = request.query_params.get("timeframe", "monthly")

        data = generate_profit_report(user, timeframe)

        return Response(data, status=status.HTTP_200_OK)


class TrendsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        timeframe = request.query_params.get("timeframe", "monthly")

        data = generate_trends_report(user, timeframe)

        return Response(data, status=status.HTTP_200_OK)
