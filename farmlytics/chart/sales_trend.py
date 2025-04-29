from decimal import Decimal
from django.db.models import Sum

from sales.models import Sale
from farmlytics.utils import get_timeframe_range, get_timeframe_period, get_grouping_trunc


def generate_sales_trend(user, timeframe="bi-weekly", mode="rolling"):
    start_date, end_date = get_timeframe_range(timeframe, mode)
    period, timedelta = get_timeframe_period(timeframe)
    trunc_group = get_grouping_trunc(timeframe)

    sales_qs = Sale.objects.filter(user=user, entry_date__range=(start_date, end_date))
    sales_data = sales_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("revenue")).order_by("period")

    if mode == "rolling":
        # fill in missing timestamp with zeros
        sales_map = {sale["period"]: sale["total"] for sale in sales_data}
        timestamp = start_date
        sales_trend = []
        
        for i in range(period):
            timestamp = timestamp + timedelta
            sales_trend.insert(0, {"period": timestamp.strftime("%Y-%m-%d"), "total": Decimal(sales_map.get(timestamp, 0))})

    else:
        sales_trend = [{"period": sale["period"].strftime("%Y-%m-%d"), "total": Decimal(sale["total"])} for sale in sales_data]

    return {
        "sales": sales_trend,
    }
