from decimal import Decimal
from collections import defaultdict
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

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
        .order_by("week")
    )

    purchases = (
        Feed.objects.filter(farmer=user, action__iexact="Bought", entry_date__gte=start_date)
        .annotate(week=ExtractWeek("entry_date"))
        .values("week")
        .annotate(total=Sum("cost"))
        .order_by("week")
    )

    weekly_map = defaultdict(lambda: {"sales": 0, "purchases": 0})
    for s in sales:
        weekly_map[s["week"]]["sales"] = s["total"]
    for p in purchases:
        weekly_map[p["week"]]["purchases"] = p["total"]

    # construct full timeline with zeros where necessary
    result = []
    for i in range(1, weeks + 1):
        _date = start_date + timedelta(weeks=i)
        week = _date.isocalendar()[1]

        result.append(
            {
                "week": f"{now.year}-W{week}",
                "sales": Decimal(weekly_map.get(week, {}).get("sales", 0)),
                "purchases": Decimal(weekly_map.get(week, {}).get("purchases", 0)),
            }
        )

    return result


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

    monthly_map = defaultdict(lambda: {"sales": 0, "expenses": 0})
    for s in sales:
        monthly_map[s["month"]]["sales"] += s["total"]
    for e in expenses:
        monthly_map[e["month"]]["expenses"] += e["total"]

    # construct full timeline with zeros where necessary
    result = []
    for i in range(1, months + 1):
        _date = start_date + relativedelta(months=i)
        month = date(_date.year, int(_date.strftime("%m")), 1)

        net_sales = Decimal(monthly_map.get(month, {}).get("sales", 0))
        net_expenses = Decimal(monthly_map.get(month, {}).get("expenses", 0))

        result.append(
            {
                "month": month.strftime("%b, %Y"),
                "net_income": net_sales - net_expenses,
            }
        )

    return result
