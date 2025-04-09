from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

import uuid

User = get_user_model()


class Feed(models.Model):
    FEED_CHOICES = [("Poultry Feed", "Poultry Feed"), ("Fish Feed", "Fish Feed")]
    ACTION_CHOICES = [("Bought", "Bought"), ("Consumed", "Consumed"), ("Initial", "Initial")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=FEED_CHOICES)
    action = models.CharField(max_length=100, choices=ACTION_CHOICES)
    quantity = models.FloatField()
    cost = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    entry_date = models.DateField(default=timezone.localdate)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feed")
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        worth = f" worth ₦{self.cost}" if self.cost else ""
        return f"{self.action} {self.quantity}kg of {self.name}{worth} on {self.entry_date}"

    class Meta:
        verbose_name = "Feed"
        verbose_name_plural = "Feed"
        ordering = ("-entry_date",)


class Livestock(models.Model):
    LIVESTOCK_CHOICES = [("Poultry", "Poultry"), ("Fish", "Fish")]
    ACTION_CHOICES = [("Bought", "Bought"), ("Sold", "Sold"), ("Dead", "Dead"), ("Initial", "Initial")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=LIVESTOCK_CHOICES)
    action = models.CharField(max_length=100, choices=ACTION_CHOICES)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    entry_date = models.DateField(default=timezone.localdate)
    is_locked = models.BooleanField(default=False)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="livestock")

    def __str__(self):
        action = "Lost" if self.action == "Dead" else self.action
        return f"{action} {self.quantity} number of {self.name} worth ₦{self.cost} on {self.entry_date}"

    class Meta:
        verbose_name = "Livestock"
        verbose_name_plural = "Livestock"
        ordering = ("-entry_date",)
