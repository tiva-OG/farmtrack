from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from inventory.models import FeedActivity, LivestockActivity
from .models import Expense


# ======================== FeedActivity Handler ========================ssssss
@receiver(post_save, sender=FeedActivity)
def update_or_create_sale_from_feed(sender, instance, **kwargs):
    if instance.action == "Purchased":
        expense, created = Expense.objects.update_or_create(
            feed_activity=instance,
            defaults={
                "user": instance.user,
                "name": instance.name,
                "quantity": instance.quantity,
                "cost": instance.cost,
                "source": "feed",
            },
        )
    else:
        Expense.objects.filter(feed_activity=instance).delete()


@receiver(pre_delete, sender=FeedActivity)
def delete_sale_from_feed(sender, instance, **kwargs):
    Expense.objects.filter(feed_activity=instance).delete()


# ======================== LivestockActivity Handler ========================
@receiver(post_save, sender=LivestockActivity)
def update_or_create_sale_from_livestock(sender, instance, **kwargs):
    if instance.action in ["Purchased", "Dead"]:
        expense, created = Expense.objects.update_or_create(
            livestock_activity=instance,
            defaults={
                "user": instance.user,
                "name": instance.name,
                "quantity": instance.quantity,
                "cost": instance.cost,
                "source": "livestock",
            },
        )
    else:
        Expense.objects.filter(livestock_activity=instance).delete()


@receiver(pre_delete, sender=LivestockActivity)
def delete_sale_from_livestock(sender, instance, **kwargs):
    Expense.objects.filter(livestock_activity=instance).delete()
