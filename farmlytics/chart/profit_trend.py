from .sales_trend import generate_sales_trend
from .expenses_trend import generate_expenses_trend


def generate_profit_trend(user, timeframe="bi-weekly", mode="rolling"):
    sales_trend = generate_sales_trend(user, timeframe, mode)["sales"]
    expenses_trend = generate_expenses_trend(user, timeframe, mode)["expenses"]

    # sales_trend = iter(sales_trend)
    # expenses_trend = iter(expenses_trend)

    profit_trend = []

    periods = set([item["period"] for item in sales_trend] + [item["period"] for item in expenses_trend])

    print(periods)

    for period in sorted(periods):
        revenue = next((item["total"] for item in sales_trend if item["period"] == period), 0)
        expense = next((item["total"] for item in expenses_trend if item["period"] == period), 0)

        profit_trend.append({"date": period, "revenue": revenue, "expense": expense})

    return {
        "profit": profit_trend,
    }
