from farmlytics.reports.inventory_report import generate_inventory_summary
from farmlytics.utils import get_inventory_aggregate, get_sale_expense_aggregate
from inventory.models import LivestockActivity
from expenses.models import Expense
from sales.models import Sale

from .utils import create_notification


def notify_low_feed_stock(user, feed_activity):
    """
    notify user if feed stock is below threshold
    """

    LOW_STOCK_THRESHOLD = user.feed_low_stock_threshold or 20
    LIVESTOCK_TYPES = ["fish", "poultry"] if user.livestock_type == "both" else [user.livestock_type]

    available_feed = generate_inventory_summary(user, LIVESTOCK_TYPES)["feed_quantity"][feed_activity.name]

    if available_feed < LOW_STOCK_THRESHOLD:
        create_notification(
            user=user,
            title="Low Feed Stock Alert",
            message=f"Your stock of {feed_activity.name} is critically low ({available_feed:.2f}kg left). Consider restocking!",
        )


def notify_high_mortality(user, livestock_activity):
    """
    notify user if mortality is highest in month or ever recorded
    """

    OVERALL_DEAD = get_inventory_aggregate(LivestockActivity, user, livestock_activity.name, "dead", "quantity")
    MONTHLY_DEAD = get_inventory_aggregate(LivestockActivity, user, livestock_activity.name, "dead", "quantity", timeframe="monthly", mode="calendar")

    print(f"MONTHLY DEAD: {MONTHLY_DEAD}")
    print(f"OVERALL DEAD: {OVERALL_DEAD}")

    if livestock_activity.quantity > MONTHLY_DEAD:
        create_notification(
            user=user,
            title="Monthly High Livestock Mortality",
            message=f"You recorded a monthly high mortality - {livestock_activity.quantity} {livestock_activity.name} deaths today. Please investigate the cause.",
        )
    if livestock_activity.quantity > OVERALL_DEAD:
        create_notification(
            user=user,
            title="Overall High Livestock Mortality",
            message=f"You recorded an overall high mortality - {livestock_activity.quantity} {livestock_activity.name} deaths today. Please investigate the cause.",
        )


def notify_large_sale(user, sale):
    """
    notify user if sale is largest in month or ever recorded
    """

    OVERALL_SALE = get_sale_expense_aggregate(Sale, user, sale.name, "revenue")
    MONTHLY_SALE = get_sale_expense_aggregate(Sale, user, sale.name, "revenue", timeframe="monthly", mode="calendar")

    if sale.cost > MONTHLY_SALE:
        create_notification(
            user=user,
            title="Monthly High Sale",
            message=f"You made your largest monthly sale worth ₦{sale.cost:.2f}",
        )
    if sale.cost > OVERALL_SALE:
        create_notification(
            user=user,
            title="Overall High Sale",
            message=f"You made your overall largest sale worth ₦{sale.cost:.2f}",
        )


def notify_high_expense(user, expense):
    """
    notify user if expense is highest in month or ever recorded
    """

    OVERALL_EXPENSE = get_sale_expense_aggregate(Expense, user, expense.name, "cost")
    MONTHLY_EXPENSE = get_sale_expense_aggregate(Expense, user, expense.name, "cost", timeframe="monthly", mode="calendar")

    if expense.cost > MONTHLY_EXPENSE:
        create_notification(
            user=user,
            title="Monthly High Expense",
            message=f"You recorded your highest monthly expense of ₦{expense.cost:.2f}",
        )
    if expense.cost > OVERALL_EXPENSE:
        create_notification(
            user=user,
            title="Overall High Expense",
            message=f"You recorded your overall highest expenses of ₦{expense.cost:.2f}",
        )
