from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import uuid
from datetime import timedelta

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    farm_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    livestock_type = models.CharField(max_length=100, blank=True, null=True)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    is_onboarded = models.BooleanField(default=False)  # flag to prevent user from accessing  onboarding is complete

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.farm_name}"


class OTP(models.Model):
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_expired(self):
        return timezone.now() > self.expires_at


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.first_name} at {self.entry_time}"

    class Meta:
        verbose_name = "Password Reset"
        verbose_name_plural = "Password Reset"
        ordering = ("-entry_time",)


class ShortenedLink(models.Model):
    short_code = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:6])
    original_url = models.URLField()
    entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} => {self.original_url}"
