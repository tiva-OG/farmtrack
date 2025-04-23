from django.urls import path
from .views import SalesReportView, ExpensesReportView, ProfitReportView, TrendsReportView

urlpatterns = [
    path("sales/", SalesReportView.as_view(), name="sales-report"),
    path("expenses/", ExpensesReportView.as_view(), name="expenses-report"),
    path("profit/", ProfitReportView.as_view(), name="profit-report"),
    path("trends/", TrendsReportView.as_view(), name="trends-report"),
]


# api/reports/

# monthly/ => return this month's summary for the logged-in user
# 1. Total Revenue, TR (from Sale)
# 2. Total Expenses, TE (from Expense)
# 3. Net Profit (TR - TE)
# 4. Top-selling Livestock (by quantity or value)
# 5. Feed/Livestock Consumption Summary

# send-email/ => trigger email with this month's report


# Report Timeframe Support
# - Bi-weekly   2-weeks
# - Monthly     4-weeks
# - Bi-monthly  8-weeks
# - Quarterly   3-months
# - 6-months    6-months
# - Yearly      12-months

# Key reports to provide:

# A) Summary Financial Report
# - Total Revenue, TR (from Sale)
# - Total Expenses, TE (from Expense)
# - Net Profit
# - Top-selling Livestock (by quantity or value)
# - Highest Expense Category (by quantity or value)
# - Feed/Livestock Consumption Summary

# B) Inventory Activity Report
# - Feed consumed vs purchased (in quantity and cost)
# - Livestock additions vs mortality (with associated costs)
# - Stock level trends over time

# C) Sales Trends Report
# - Daily/weekly/monthly sales trend (chart data)
# - Top-selling livestock or feed items
# - Average sale value

# D) Expense Breakdown Report
# - Comparison between actual feed consumed and feed bought

# E) Livestock Health & Performance Report
# - Mortality rates
# - Growth trends (based on quantity and sale timing)
# - Cost vs Revenue per livestock type
