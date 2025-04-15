from rest_framework import serializers
from .models import FeedActivity, LivestockActivity


class FeedActivitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = FeedActivity
        fields = ["id", "user", "name", "action", "quantity", "cost", "entry_date"]


class LivestockActivitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = LivestockActivity
        fields = ["id", "user", "name", "action", "quantity", "cost", "entry_date"]
