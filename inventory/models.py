from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class FeedActivity(models.Model):
    FEED_TYPE_CHOICES = [
        ("fish feed", "Fish Feed"),
        ("poultry feed", "Poultry Feed"),
    ]
    ACTION_CHOICES = [
        ("purchased", "Purchased"),
        ("consumed", "Consumed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feed_activities")
    name = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    entry_date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.name} - {self.action} ({self.quantity})"

    class Meta:
        verbose_name = "Feed Activity"
        verbose_name_plural = "Feed Activities"
        ordering = ("-entry_date",)


class LivestockActivity(models.Model):
    ACTION_CHOICES = [
        ("added", "Added"),
        ("sold", "Sold"),
        ("dead", "Dead"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="livestock_activities")
    name = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.name} - {self.action} ({self.quantity})"

    class Meta:
        verbose_name = "Livestock Activity"
        verbose_name_plural = "Livestock Activities"
        ordering = ("-entry_date",)
