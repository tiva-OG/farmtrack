from datetime import date
from calendar import monthrange
from dateutil.relativedelta import relativedelta

from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth


def get_timeframe_range(timeframe, mode="rolling"):
    today = date.today()

    if mode == "rolling":
        match timeframe:
            case "weekly":
                return today - relativedelta(weeks=1), today
            case "bi-weekly":
                return today - relativedelta(weeks=2), today
            case "monthly":
                return today - relativedelta(months=1), today
            case "bi-monthly":
                return today - relativedelta(months=2), today
            case "quarterly":
                return today - relativedelta(months=3), today
            case "6-months":
                return today - relativedelta(months=6), today
            case "yearly":
                return today - relativedelta(years=1), today
            case _:
                raise ValueError("Invalid timeframe")

    elif mode == "calendar":
        match timeframe:
            case "weekly":  # date from week start (Monday) to week end (Sunday)
                start_date = today - relativedelta(days=today.weekday())
                end_date = start_date + relativedelta(days=6)
                return start_date, end_date
            case "bi-weekly":  # from 1st to 15th of the month, or 16th to end of the month
                if today.day <= 15:
                    start_date = today.replace(day=1)
                    end_date = today.replace(day=15)
                else:
                    start_date = today.replace(day=16)
                    end_date = today.replace(day=monthrange(today.year, today.month)[1])
                return start_date, end_date
            case "monthly":  # first and last day of this month
                start_date = today.replace(day=1)  # first day of this month
                end_date = today.replace(day=monthrange(today.year, today.month)[1])  # last day of this month
                return start_date, end_date
            case "quarterly":  # first and last day of the quarter
                quarter = (today.month - 1) // 3 + 1
                start_month = (quarter - 1) * 3 + 1
                end_month = quarter * 3
                start_date = today.replace(month=start_month, day=1)
                end_date = today.replace(month=end_month, day=monthrange(today.year, end_month)[1])
                return start_date, end_date
            case "yearly":
                start_date = today.replace(month=1, day=1)
                end_date = today.replace(month=12, day=31)
                return start_date, end_date


def get_timeframe_period(timeframe):
    match timeframe:
        case "weekly":
            return 7, relativedelta(days=1)
        case "bi-weekly":
            return 14, relativedelta(days=1)
        case "monthly":
            return 4, relativedelta(weeks=1)
        case "bi-monthly":
            return 8, relativedelta(weeks=1)
        case "quarterly":
            return 12, relativedelta(weeks=1)
        case "6-months":
            return 6, relativedelta(months=1)
        case "yearly":
            return 12, relativedelta(months=1)
        case _:
            raise ValueError("Invalid timeframe")


def get_grouping_trunc(timeframe):
    match timeframe:
        case "weekly" | "bi-weekly":
            return TruncDay("entry_date")
        case "monthly" | "bi-monthly" | "quarterly":
            return TruncWeek("entry_date")
        case "6-months" | "yearly":
            return TruncMonth("entry_date")
        case _:
            raise ValueError("Invalid timeframe")


def get_inventory_aggregate(model, user, name, action, field, **kwargs):
    timeframe = kwargs.get("timeframe")
    mode = kwargs.get("mode")

    if timeframe and mode:
        start_date, end_date = get_timeframe_range(timeframe, mode)
        queries = model.objects.filter(user=user, name=name, action=action, entry_date__range=(start_date, end_date))
    else:
        queries = model.objects.filter(user=user, name=name, action=action)

    aggregate = queries.aggregate(total=Sum(field))["total"] or 0

    return aggregate


def get_sale_expense_aggregate(model, user, name, field, **kwargs):
    timeframe = kwargs.get("timeframe")
    mode = kwargs.get("mode")

    if timeframe and mode:
        start_date, end_date = get_timeframe_range(timeframe, mode)
        queries = model.objects.filter(user=user, name=name, entry_date__range=(start_date, end_date))
    else:
        queries = model.objects.filter(user=user, name=name)

    aggregate = queries.aggregate(total=Sum(field))["total"] or 0

    return aggregate


def get_quantity(model, user, name, action, **kwargs):
    timeframe = kwargs.get("timeframe")
    mode = kwargs.get("mode")

    if timeframe and mode:
        start_date, end_date = get_timeframe_range(timeframe, mode)
        queries = model.objects.filter(user=user, name=name, action=action, entry_date__range=(start_date, end_date))
    else:
        queries = model.objects.filter(user=user, name=name, action=action)

    quantity = queries.aggregate(total=Sum("quantity"))["total"] or 0

    return quantity


def get_cost(model, user, name, action, **kwargs):
    timeframe = kwargs.get("timeframe")
    mode = kwargs.get("mode")

    if timeframe and mode:
        start_date, end_date = get_timeframe_range(timeframe, mode)
        queries = model.objects.filter(user=user, name=name, action=action, entry_date__range=(start_date, end_date))
    else:
        queries = model.objects.filter(user=user, name=name, action=action)

    cost = queries.aggregate(total=Sum("cost"))["total"] or 0

    return cost
