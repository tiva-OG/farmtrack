from rest_framework import serializers
from .models import Sale


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ["id", "name", "quantity", "revenue", "entry_date"]
