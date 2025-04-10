from datetime import timedelta
from collections import defaultdict

from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth, ExtractWeek

from inventory.models import Feed, Livestock


def get_weekly_sales_purchases(user, weeks):
    now = timezone.now()
    start_date = now - timedelta(weeks=weeks)

    sales = (
        Livestock.objects.filter(farmer=user, action__iexact="Sold", entry_date__gte=start_date)
        .annotate(week=ExtractWeek("entry_date"))
        .values("week")
        .annotate(total=Sum("cost"))
    )

    purchases = (
        Feed.objects.filter(farmer=user, action__iexact="Bought", entry_date__gte=start_date)
        .annotate(week=ExtractWeek("entry_date"))
        .values("week")
        .annotate(total=Sum("cost"))
    )

    result = defaultdict(lambda: {"sales": 0, "purchases": 0})

    for s in sales:
        result[s["week"]]["sales"] = s["total"]
    for p in purchases:
        result[p["week"]]["purchases"] = p["total"]

    return [
        {
            "week": f"{now.year}-W{week}",
            "sales": data["sales"],
            "purchases": data["purchases"],
        }
        for week, data in sorted(result.items())
    ]


def get_monthly_net_income(user, months):
    now = timezone.now()
    start_date = now - timedelta(days=months * 30)

    sales = (
        Livestock.objects.filter(farmer=user, action__iexact="Sold", entry_date__gte=start_date)
        .annotate(month=TruncMonth("entry_date"))
        .values("month")
        .annotate(total=Sum("cost"))
    )

    feed_bought = (
        Feed.objects.filter(farmer=user, action__iexact="Bought", entry_date__gte=start_date)
        .annotate(month=TruncMonth("entry_date"))
        .values("month")
        .annotate(total=Sum("cost"))
    )
    livestock_dead = (
        Livestock.objects.filter(farmer=user, action__iexact="Dead", entry_date__gte=start_date)
        .annotate(month=TruncMonth("entry_date"))
        .values("month")
        .annotate(total=Sum("cost"))
    )

    expenses = feed_bought.union(livestock_dead)

    result = defaultdict(lambda: {"sales": 0, "expenses": 0})

    for s in sales:
        result[s["month"]]["sales"] += s["total"]
    for e in expenses:
        result[e["month"]]["expenses"] += e["total"]

    return [
        {
            "month": month.strftime("%Y-%m"),
            "net_income": data["sales"] - data["expenses"],
        }
        for month, data in sorted(result.items())
    ]
