from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Farm Manager"),
    )

    LIVESTOCK_CHOICES = (
        ("fish", "Fish"),
        ("poultry", "Poultry"),
        ("both", "Both"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="manager")

    # Farm-specific fields
    farm_name = models.CharField(max_length=100)
    livestock_type = models.CharField(max_length=10, choices=LIVESTOCK_CHOICES, default="both")
    feed_low_stock_threshold = models.PositiveIntegerField(default=20)

    # Roles
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
