from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from inventory.utils import set_initial_inventory

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "farm_name", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class OnboardUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    feed_low_stock_threshold = serializers.IntegerField()
    livestock_type = serializers.CharField()

    initial_livestock_activity = serializers.ListField(child=serializers.DictField(), required=False)
    initial_feed_activity = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "feed_low_stock_threshold",
            "livestock_type",
            "initial_livestock_activity",
            "initial_feed_activity",
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.livestock_type = validated_data.get("livestock_type")
        instance.feed_low_stock_threshold = validated_data.get("feed_low_stock_threshold")
        instance.is_active = True
        instance.is_staff = True
        instance.save()

        initial_livestock_activity = validated_data.get("initial_livestock_activity", [])
        initial_feed_activity = validated_data.get("initial_feed_activity", [])

        set_initial_inventory(instance, initial_livestock_activity, initial_feed_activity)

        return instance


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
