from rest_framework import serializers
from .models import SalesExpenses


class SalesExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesExpenses
        fields = ["id", "item", "cost", "entry_date", "record_type"]


class SalesTrendSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=20, decimal_places=2)
