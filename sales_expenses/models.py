from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

import uuid

User = get_user_model()


class SalesExpenses(models.Model):
    ITEM_CHOICES = [("Feed", "Feed"), ("Livestock", "Livestock")]
    RECORD_TYPE_CHOICES = [("Sale", "Sale"), ("Expense", "Expense")]

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.CharField(max_length=255, choices=ITEM_CHOICES)
    item_id = models.UUIDField()
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    entry_date = models.DateField(default=timezone.localdate)
    record_type = models.CharField(max_length=255, choices=RECORD_TYPE_CHOICES)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_expenses")

    def __str__(self):
        return f"{self.farmer.first_name} made a(n) {self.record_type} worth ₦{self.cost} on {self.entry_date}"

    class Meta:
        verbose_name = "Sale & Expense"
        verbose_name_plural = "Sales & Expenses"
        ordering = ("-entry_date",)
