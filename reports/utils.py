from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

from sales.models import Sale


def get_timeframe_range(timeframe):
    today = date.today()

    match timeframe:
        case "bi-weekly":
            return today - relativedelta(weeks=2), today
        case "monthly":
            return today - relativedelta(months=1), today
        case "bi-monthly":
            return today - relativedelta(months=2), today
        case "quarterly":
            return today - relativedelta(months=3), today
        case "6-months":
            return today - relativedelta(months=6), today
        case "yearly":
            return today - relativedelta(years=1), today
        case _:
            raise ValueError("Invalid timeframe")


def get_grouping_trunc(timeframe):
    match timeframe:
        case "weekly" | "bi-weekly":
            return TruncDay("entry_date")
        case "monthly" | "bi-monthly" | "quarterly":
            return TruncWeek("entry_date")
        case "6-months" | "yearly":
            return TruncMonth("entry_date")
        case _:
            raise ValueError("Invalid timeframe")


def get_insights(user, timeframe):
    current_start, current_end = get_timeframe_range(timeframe)
    prev_start = current_start - (current_end - current_start)
    prev_end = current_start

    current_qs = Sale.objects.filter(user=user, entry_date__range=(current_start, current_end))
    current_sales = current_qs.aggregate(total=Sum("revenue"))["total"] or 0

    prev_qs = Sale.objects.filter(user=user, entry_date__range=(prev_start, prev_end))
    prev_sales = prev_qs.aggregate(total=Sum("revenue"))["total"] or 0

    insight = []
    if prev_sales > 0:
        change = ((current_sales - prev_sales) / prev_sales) * 100
        trend = "increased" if change > 0 else "decreased"
        insight.append(f"Your sales {trend} by {abs(round(change,2))}% compared to the previous period")
    else:
        insight.append("Not enough data to compare sales trends")

    return insight
