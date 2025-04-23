from django.db.models import Sum, Avg

from sales.models import Sale
from expenses.models import Expense
from inventory.models import FeedActivity, LivestockActivity
from .utils import get_timeframe_range, get_grouping_trunc, get_insights


def generate_sales_report(user, timeframe):
    start_date, end_date = get_timeframe_range(timeframe)

    sales_qs = Sale.objects.filter(user=user, entry_date__range=(start_date, end_date))
    sold_items_qs = LivestockActivity.objects.filter(user=user, action="sold", entry_date__range=(start_date, end_date))

    total_revenue = sales_qs.aggregate(total=Sum("revenue"))["total"] or 0
    number_of_sales = sales_qs.count()
    average_sale_value = sales_qs.aggregate(average=Avg("revenue"))["average"] or 0
    sold_items = sold_items_qs.values("name").annotate(total_qty=Sum("quantity")).order_by("-total_qty")
    top_items_sold = [{"name": item["name"], "quantity": item["total_qty"]} for item in sold_items]

    return {
        "total_revenue": total_revenue,
        "number_of_sales": number_of_sales,
        "average_sale_value": average_sale_value,
        "top_items_sold": top_items_sold,
        "start_date": start_date,
        "end_date": end_date,
    }


def generate_expenses_report(user, timeframe):
    start_date, end_date = get_timeframe_range(timeframe)

    expenses_qs = Expense.objects.filter(user=user, entry_date__range=(start_date, end_date))
    total_expenses = expenses_qs.aggregate(total=Sum("cost"))["total"] or 0

    feed_qs = Expense.objects.filter(user=user, source="feed", entry_date__range=(start_date, end_date))
    feed_expenses = feed_qs.aggregate(total=Sum("cost"))["total"] or 0

    mortality_qs = LivestockActivity.objects.filter(user=user, action="dead", entry_date__range=(start_date, end_date))
    mortality_cost = mortality_qs.aggregate(total=Sum("cost"))["total"] or 0

    return {
        "total_expenses": total_expenses,
        "feed_expenses": feed_expenses,
        "mortality_cost": mortality_cost,
        "start_date": start_date,
        "end_date": end_date,
    }


def generate_profit_report(user, timeframe):
    sales_report = generate_sales_report(user, timeframe)
    expenses_report = generate_expenses_report(user, timeframe)

    total_sales = sales_report["total_revenue"]
    total_expenses = expenses_report["total_expenses"]

    return {
        "net_profit": total_sales - total_expenses,
        **sales_report,
        **expenses_report,
    }


def generate_inventory_report(user, timeframe):
    start_date, end_date = get_timeframe_range(timeframe)

    feed_purchased_qs = FeedActivity.objects.filter(user=user, action="purchased", entry_date__range=(start_date, end_date))
    feed_purchased = feed_purchased_qs.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0

    feed_consumed_qs = FeedActivity.objects.filter(user=user, action="consumed", entry_date__range=(start_date, end_date))
    feed_consumed = feed_consumed_qs.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0

    livestock_added_qs = LivestockActivity.objects.filter(user=user, action="added", entry_date__range=(start_date, end_date))
    livestock_added = livestock_added_qs.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0

    livestock_sold_qs = LivestockActivity.objects.filter(user=user, action="sold", entry_date__range=(start_date, end_date))
    livestock_sold = livestock_sold_qs.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0

    livestock_dead_qs = LivestockActivity.objects.filter(user=user, action="dead", entry_date__range=(start_date, end_date))
    livestock_dead = livestock_dead_qs.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0

    return {
        "feed_purchased": feed_purchased,
        "feed_consumed": feed_consumed,
        "livestock_added": livestock_added,
        "livestock_sold": livestock_sold,
        "livestock_dead": livestock_dead,
    }


def generate_trends_report(user, timeframe):
    start_date, end_date = get_timeframe_range(timeframe)
    trunc_date = get_grouping_trunc(timeframe)

    sales_qs = Sale.objects.filter(user=user, entry_date__range=(start_date, end_date))
    sales_trend = sales_qs.annotate(period=trunc_date).values("period").annotate(total=Sum("revenue")).order_by("period")

    feed_qs = FeedActivity.objects.filter(user=user, action="consumed", entry_date__range=(start_date, end_date))
    feed_trend = feed_qs.annotate(period=trunc_date).values("period").annotate(total_qty=Sum("quantity")).order_by("period")

    expenses_qs = Expense.objects.filter(user=user, entry_date__range=(start_date, end_date))
    expenses_trend = expenses_qs.annotate(period=trunc_date).values("period").annotate(total=Sum("cost")).order_by("period")

    insights = get_insights(user, timeframe)

    return {
        "sales_trend": list(sales_trend),
        "expenses_trend": list(expenses_trend),
        "feed_consumption_trend": list(feed_trend),
        "insights": insights,
    }
