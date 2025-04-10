from rest_framework import serializers


class DashboardInfoSerializer(serializers.Serializer):
    low_stock_threshold = serializers.IntegerField()
    feed_info = serializers.ListField(child=serializers.DictField(), required=False)
    livestock_count = serializers.ListField(child=serializers.DictField(), required=False)
    sales_data = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        fields = ["low_stock_threshold", "feed_info", "livestock_count", "sales_data"]


class AnalyticsInfoSerializer(serializers.Serializer):
    feed_consumption = serializers.ListField(child=serializers.DictField(), required=False)
    livestock_sales = serializers.ListField(child=serializers.DictField(), required=False)
    livestock_mortality = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        fields = ["feed_consumption", "livestock_sales", "livestock_mortality"]
