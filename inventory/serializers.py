from rest_framework import serializers

from .models import Feed, Livestock


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["id", "name", "action", "quantity", "cost", "entry_date"]
        extra_kwargs = {"farmer": {"read_only": True}}


class LivestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livestock
        fields = ["id", "name", "action", "quantity", "cost", "entry_date"]
        extra_kwargs = {"farmer": {"read_only": True}}


class InitialInventorySerializer(serializers.ModelSerializer):
    livestock = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        required=False,
    )

    feed = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        required=False,
    )
