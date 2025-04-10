from decimal import Decimal
from datetime import timedelta, date

from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from inventory.models import Feed, Livestock
from sales_expenses.models import SalesExpenses


def get_total_quantity(model, user, name, action):
    return (
        model.objects.filter(
            farmer=user,
            name__iexact=name,
            action__iexact=action,
        ).aggregate(
            total=Sum("quantity")
        )["total"]
        or 0
    )


def get_total_cost(user, record_type):
    return SalesExpenses.objects.filter(farmer=user, record_type__iexact=record_type).aggregate(total=Sum("cost"))["total"] or 0


def calculate_feed_data(user, livestock_types):
    feed_info = []

    for livestock in livestock_types:
        name = f"{livestock} Feed"
        initial = get_total_quantity(Feed, user, name, "Initial")
        bought = get_total_quantity(Feed, user, name, "Bought")
        consumed = get_total_quantity(Feed, user, name, "Consumed")
        feed_left = (initial + bought) - consumed

        feed_info.append(
            {
                "name": name,
                "initial": initial,
                "bought": bought,
                "consumed": consumed,
                "left": feed_left,
            }
        )

    return feed_info


def calculate_livestock_data(user, livestock_types):
    livestock_count = []

    for livestock in livestock_types:
        initial = get_total_quantity(Livestock, user, livestock, "Initial")
        bought = get_total_quantity(Livestock, user, livestock, "Bought")
        sold = get_total_quantity(Livestock, user, livestock, "Sold")
        dead = get_total_quantity(Livestock, user, livestock, "Dead")
        count = max((initial + bought) - (sold + dead), 0)

        livestock_count.append(
            {
                "name": livestock,
                "initial": initial,
                "bought": bought,
                "sold": sold,
                "dead": dead,
                "count": count,
            }
        )

    return livestock_count


def get_sales_data(user, period):
    today = date.today()
    start_date = today - timedelta(days=period)

    sales_data = (
        SalesExpenses.objects.filter(farmer=user, record_type="Sale", entry_date__range=(start_date, today))
        .annotate(sale_date=TruncDate("entry_date"))
        .values("sale_date")
        .annotate(total=Sum("cost"))
        .order_by("sale_date")
    )

    # map sale_date -> total sales
    sales_map = {sale["sale_date"]: sale["total"] for sale in sales_data}

    # Fill in missing dates with zero sales
    result = []
    for i in range(period + 1):
        day = start_date + timedelta(days=i)
        result.insert(0, {"date": day.strftime("%Y-%m-%d"), "total_sales": Decimal(sales_map.get(day, 0))})

    return result


def send_analytics_report(user, weekly_data, monthly_data):
    subject = "Your FarmTrack Analytics Report"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    context = {
        "user": user,
        "weekly_data": weekly_data,
        "monthly_data": monthly_data,
    }

    html_content = render_to_string("emails/analytics_report.html", context)
    text_content = "This email contains your recent FarmTrack analytics. Please view in an HTML-compatible client."

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
