from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "farm_name",
            "livestock_type",
            "feed_low_stock_threshold",
            "is_active",
            "is_admin",
            "is_manager",
        )

        