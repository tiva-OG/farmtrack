from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "quantity", "revenue", "entry_date")
    search_fields = ("name", "user__email")
    list_filter = ("name", "entry_date")
