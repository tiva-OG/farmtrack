from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    LIVESTOCK_CHOICES = (
        ("fish", "Fish"),
        ("poultry", "Poultry"),
        ("both", "Both"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    # Farm-specific fields
    farm_name = models.CharField(max_length=100)
    livestock_type = models.CharField(max_length=10, choices=LIVESTOCK_CHOICES, default="both")
    feed_low_stock_threshold = models.PositiveIntegerField(default=50)

    # Roles
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.farm_name} ({self.email})"
