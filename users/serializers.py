from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "first_name",
            "last_name",
            "farm_name",
            "livestock_type",
            "feed_low_stock_threshold",
            "is_active",
            "is_staff",
        ]


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_active:
            raise serializers.ValidationError("Your account is deactivated.", code="authorization")

        data["email"] = user.email
        data["role"] = user.role
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["farm_name"] = user.farm_name
        data["livestock_type"] = user.livestock_type
        data["feed_low_stock_threshold"] = user.feed_low_stock_threshold

        return data
