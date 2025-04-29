from django.db.models import Sum

from expenses.models import Expense
from inventory.models import LivestockActivity
from farmlytics.utils import get_timeframe_range


def generate_expenses_report(user, timeframe="monthly", mode="calendar"):
    start_date, end_date = get_timeframe_range(timeframe, mode)

    expenses_qs = Expense.objects.filter(user=user, entry_date__range=(start_date, end_date))
    total_cost = expenses_qs.aggregate(total=Sum("cost"))["total"] or 0

    feed_qs = Expense.objects.filter(user=user, source="feed", entry_date__range=(start_date, end_date))
    feed_cost = feed_qs.aggregate(total=Sum("cost"))["total"] or 0

    mortality_qs = LivestockActivity.objects.filter(user=user, action="dead", entry_date__range=(start_date, end_date))
    mortality_cost = mortality_qs.aggregate(total=Sum("cost"))["total"] or 0

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_cost": total_cost,
        "feed_cost": feed_cost,
        "mortality_cost": mortality_cost,
    }
