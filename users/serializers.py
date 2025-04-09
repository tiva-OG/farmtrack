from datetime import timedelta
from django.utils.timezone import now
from rest_framework import serializers
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from inventory.utils import seed_initial_inventory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "farm_name",
            "first_name",
            "last_name",
            "profile_picture",
            "livestock_type",
            "low_stock_threshold",
            "is_onboarded",
        ]
        extra_kwargs = {"email": {"required": True}}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "farm_name", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class OnboardingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    low_stock_threshold = serializers.IntegerField()
    livestock_type = serializers.CharField()
    livestock_data = serializers.ListField(child=serializers.DictField(), required=False)
    feed_data = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "low_stock_threshold",
            "livestock_type",
            "livestock_data",
            "feed_data",
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.livestock_type = validated_data.get("livestock_type")
        instance.low_stock_threshold = validated_data.get("low_stock_threshold")
        instance.is_onboarded = True
        instance.save()

        livestock_data = validated_data.get("livestock_data", [])
        feed_data = validated_data.get("feed_data", [])

        seed_initial_inventory(instance, livestock_data, feed_data)

        return instance


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data["uidb64"]))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link.")

        # token expiration logic?

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or Expired token.")

        return {"user": user, "new_password": data["new_password"]}

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
