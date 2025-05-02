from django.db.models import Sum, Avg

from inventory.models import FeedActivity, LivestockActivity
from farmlytics.utils import get_inventory_aggregate, get_quantity


def generate_inventory_report(user, livestock_types, timeframe="monthly", mode="calendar"):
    feed_purchased_quantity = {}
    feed_purchased_cost = {}
    feed_consumed_quantity = {}

    livestock_added_quantity = {}
    livestock_added_cost = {}
    livestock_sold_quantity = {}
    livestock_sold_cost = {}
    livestock_dead_quantity = {}
    livestock_dead_cost = {}

    for livestock in livestock_types:
        # FEED PURCHASED
        purchased_quantity = get_inventory_aggregate(FeedActivity, user, f"{livestock} feed", "purchased", "quantity", timeframe=timeframe, mode=mode)
        purchased_cost = get_inventory_aggregate(FeedActivity, user, f"{livestock} feed", "purchased", "cost", timeframe=timeframe, mode=mode)

        # FEED CONSUMED
        consumed_quantity = get_inventory_aggregate(FeedActivity, user, f"{livestock} feed", "consumed", "quantity", timeframe=timeframe, mode=mode)

        feed_purchased_quantity[f"{livestock} feed"] = purchased_quantity
        feed_purchased_cost[f"{livestock} feed"] = purchased_cost
        feed_consumed_quantity[f"{livestock} feed"] = consumed_quantity

        # LIVESTOCK ADDED
        added_quantity = get_inventory_aggregate(LivestockActivity, user, livestock, "added", "quantity", timeframe=timeframe, mode=mode)
        added_cost = get_inventory_aggregate(LivestockActivity, user, livestock, "added", "cost", timeframe=timeframe, mode=mode)

        # LIVESTOCK SOLD
        sold_quantity = get_inventory_aggregate(LivestockActivity, user, livestock, "sold", "quantity", timeframe=timeframe, mode=mode)
        sold_cost = get_inventory_aggregate(LivestockActivity, user, livestock, "sold", "cost", timeframe=timeframe, mode=mode)

        # LIVESTOCK DEAD
        dead_quantity = get_inventory_aggregate(LivestockActivity, user, livestock, "dead", "quantity", timeframe=timeframe, mode=mode)
        dead_cost = get_inventory_aggregate(LivestockActivity, user, livestock, "dead", "cost", timeframe=timeframe, mode=mode)

        livestock_added_quantity[livestock] = added_quantity
        livestock_added_cost[livestock] = added_cost
        livestock_sold_quantity[livestock] = sold_quantity
        livestock_sold_cost[livestock] = sold_cost
        livestock_dead_quantity[livestock] = dead_quantity
        livestock_dead_cost[livestock] = dead_cost

    return {
        "feed_purchased_quantity": feed_purchased_quantity,
        "feed_purchased_cost": feed_purchased_cost,
        "feed_consumed_quantity": feed_consumed_quantity,
        "livestock_added_quantity": livestock_added_quantity,
        "livestock_added_cost": livestock_added_cost,
        "livestock_sold_quantity": livestock_sold_quantity,
        "livestock_sold_cost": livestock_sold_cost,
        "livestock_dead_quantity": livestock_dead_quantity,
        "livestock_dead_cost": livestock_dead_cost,
    }


def generate_inventory_summary(user, livestock_types):
    feed_quantity = {}
    livestock_quantity = {}
    livestock_mortality = {}

    for livestock in livestock_types:
        initial_feed = get_quantity(FeedActivity, user, f"{livestock} feed", "initial")
        purchased_feed = get_quantity(FeedActivity, user, f"{livestock} feed", "purchased")
        consumed_feed = get_quantity(FeedActivity, user, f"{livestock} feed", "consumed")

        current_feed = max((initial_feed + purchased_feed) - consumed_feed, 0)
        feed_quantity[f"{livestock} feed"] = current_feed

        initial_livestock = get_quantity(LivestockActivity, user, livestock, "initial")
        added_livestock = get_quantity(LivestockActivity, user, livestock, "added")
        sold_livestock = get_quantity(LivestockActivity, user, livestock, "sold")
        dead_livestock = get_quantity(LivestockActivity, user, livestock, "dead")

        total_livestock = initial_livestock + added_livestock
        current_livestock = max(total_livestock - (sold_livestock + dead_livestock), 0)
        mortality = (dead_livestock / total_livestock) * 100 if total_livestock else 0
        livestock_quantity[livestock] = current_livestock
        livestock_mortality[livestock] = round(mortality, 2)

    return {
        "feed_quantity": feed_quantity,
        "livestock_quantity": livestock_quantity,
        "livestock_mortality": livestock_mortality,
    }
