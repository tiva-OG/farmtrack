from django.db.models import Sum

from inventory.models import FeedActivity, LivestockActivity
from farmlytics.utils import get_timeframe_range, get_grouping_trunc


def generate_feed_trend(user, timeframe="bi-weekly", mode="rolling"):
    start_date, end_date = get_timeframe_range(timeframe, mode)
    trunc_group = get_grouping_trunc(timeframe)

    feed_purchased_qs = FeedActivity.objects.filter(user=user, action="purchased", entry_date__range=(start_date, end_date))
    feed_purchased_trend = feed_purchased_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("quantity")).order_by("period")

    feed_consumed_qs = FeedActivity.objects.filter(user=user, action="consumed", entry_date__range=(start_date, end_date))
    feed_consumed_trend = feed_consumed_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("quantity")).order_by("period")

    return {
        "feed_purchased": list(feed_purchased_trend),
        "feed_consumed": list(feed_consumed_trend),
    }


def generate_livestock_trend(user, timeframe="bi-weekly", mode="rolling"):
    start_date, end_date = get_timeframe_range(timeframe, mode)
    trunc_group = get_grouping_trunc(timeframe)

    livestock_added_qs = LivestockActivity.objects.filter(user=user, action="added", entry_date__range=(start_date, end_date))
    livestock_added_trend = livestock_added_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("quantity")).order_by("period")

    livestock_sold_qs = LivestockActivity.objects.filter(user=user, action="sold", entry_date__range=(start_date, end_date))
    livestock_sold_trend = livestock_sold_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("quantity")).order_by("period")

    livestock_dead_qs = LivestockActivity.objects.filter(user=user, action="dead", entry_date__range=(start_date, end_date))
    livestock_dead_trend = livestock_dead_qs.annotate(period=trunc_group).values("period").annotate(total=Sum("quantity")).order_by("period")

    return {
        "livestock_added": list(livestock_added_trend),
        "livestock_sold": list(livestock_sold_trend),
        "livestock_dead": list(livestock_dead_trend),
    }
