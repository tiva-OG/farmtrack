from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "quantity", "cost", "entry_date")
    search_fields = ("name", "user__email")
    list_filter = ("name", "entry_date")
