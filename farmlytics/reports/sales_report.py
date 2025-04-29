from django.db.models import Sum, Avg

from sales.models import Sale
from inventory.models import LivestockActivity
from farmlytics.utils import get_timeframe_range


def generate_sales_report(user, timeframe="monthly", mode="calendar"):
    start_date, end_date = get_timeframe_range(timeframe, mode)

    sales_qs = Sale.objects.filter(user=user, entry_date__range=(start_date, end_date))
    total_revenue = sales_qs.aggregate(total=Sum("revenue"))["total"] or 0
    num_of_sales = sales_qs.count()
    avg_sale_value = sales_qs.aggregate(average=Avg("revenue"))["average"] or 0

    sold_livestock_qs = LivestockActivity.objects.filter(user=user, action="sold", entry_date__range=(start_date, end_date))
    sold_livestock_qty = sold_livestock_qs.values("name").annotate(total_qty=Sum("quantity")).order_by("-total_qty")
    sold_livestock_qty = [{"name": item["name"], "quantity": item["total_qty"]} for item in sold_livestock_qty]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_revenue": total_revenue,
        "num_of_sales": num_of_sales,
        "avg_sale_value": avg_sale_value,
        "sold_livestock_qty": sold_livestock_qty,
    }
