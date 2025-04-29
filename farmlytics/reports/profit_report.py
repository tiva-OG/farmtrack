from django.db.models import Sum

from sales.models import Sale
from expenses.models import Expense
from farmlytics.utils import get_timeframe_range


def generate_profit_report(user, timeframe="monthly", mode="calendar"):
    start_date, end_date = get_timeframe_range(timeframe, mode)

    sales_qs = Sale.objects.filter(user=user, entry_date__range=(start_date, end_date))
    total_revenue = sales_qs.aggregate(total=Sum("revenue"))["total"] or 0

    expenses_qs = Expense.objects.filter(user=user, entry_date__range=(start_date, end_date))
    total_cost = expenses_qs.aggregate(total=Sum("cost"))["total"] or 0

    net_profit = total_revenue - total_cost
    profit_margin = (net_profit / total_revenue) * 100 if total_revenue else 0

    # compare growth to previous timeframe
    prev_start = start_date - (end_date - start_date)
    prev_end = start_date

    prev_sales_qs = Sale.objects.filter(user=user, entry_date__range=(prev_start, prev_end))
    prev_revenue = prev_sales_qs.aggregate(total=Sum("revenue"))["total"] or 0

    prev_expenses_qs = Expense.objects.filter(user=user, entry_date__range=(prev_start, prev_end))
    prev_cost = prev_expenses_qs.aggregate(total=Sum("cost"))["total"] or 0

    prev_profit = prev_revenue - prev_cost

    revenue_growth = ((total_revenue - prev_revenue) / prev_revenue) * 100 if prev_revenue else 0
    profit_growth = ((net_profit - prev_profit) / prev_profit) * 100 if prev_profit else 0

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "net_profit": net_profit,
        "profit_margin": round(profit_margin, 2),
        "profit_growth": round(profit_growth, 2),
        "revenue_growth": round(revenue_growth, 2),
    }
