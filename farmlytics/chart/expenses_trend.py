from decimal import Decimal
from django.db.models import Sum

from expenses.models import Expense
from farmlytics.utils import get_timeframe_range, get_timeframe_period, get_grouping_trunc


def generate_expenses_trend(user, timeframe="bi-weekly", mode="rolling"):
    start_date, end_date = get_timeframe_range(timeframe, mode)
    period, timedelta = get_timeframe_period(timeframe)
    trunc_group = get_grouping_trunc(timeframe)

    expenses_qs = Expense.objects.filter(user=user, entry_date__range=(start_date, end_date))
    expenses_data = expenses_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("cost")).order_by("period")

    expenses_map = {expense["period"]: expense["total"] for expense in expenses_data}

    if mode == "rolling":
        # fill in missing timestamp with zeros
        expenses_map = {sale["period"]: sale["total"] for sale in expenses_data}
        timestamp = start_date
        expenses_trend = []

        for i in range(period):
            timestamp = timestamp + timedelta
            expenses_trend.insert(0, {"period": timestamp.strftime("%Y-%m-%d"), "total": Decimal(expenses_map.get(timestamp, 0))})

    else:
        expenses_trend = [
            {"period": expense["period"].strftime("%Y-%m-%d"), "total": Decimal(expense["total"])} for expense in expenses_data.reverse()
        ]

    return {
        "expenses": expenses_trend,
    }
