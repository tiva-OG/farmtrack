from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from inventory.models import FeedActivity, LivestockActivity

User = get_user_model()


class Expense(models.Model):
    SOURCE_CHOICES = [
        ("feed", "Feed"),
        ("livestock", "Livestock"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=20)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    entry_date = models.DateField()

    feed_activity = models.OneToOneField(
        FeedActivity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="expense_record",
    )

    livestock_activity = models.OneToOneField(
        LivestockActivity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="expense_record",
    )

    def __str__(self):
        return f"{self.name} - {self.quantity} units - {self.cost} cost"
