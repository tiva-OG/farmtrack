from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from inventory.models import LivestockActivity

User = get_user_model()


class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # signifies livestock type
    quantity = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()

    livestock_activity = models.OneToOneField(LivestockActivity, on_delete=models.CASCADE, related_name="sale_record")

    def __str__(self):
        return f"{self.quantity} {self.name} sold on {self.entry_date}"
