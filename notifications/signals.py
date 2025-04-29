from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models import FeedActivity, LivestockActivity
from .services import notify_low_feed_stock, notify_high_mortality, notify_large_sale, notify_high_expense


# ======================== Low Feed Stock Handler ========================
@receiver(post_save, sender=FeedActivity)
def check_low_feed_stock(sender, instance, created, **kwargs):
    if created and instance.action.lower() == "consumed":
        notify_low_feed_stock(instance.user, instance)


# ======================== High Mortality Handler ========================
@receiver(post_save, sender=LivestockActivity)
def check_high_mortality(sender, instance, created, **kwargs):
    if created and instance.action.lower() == "dead":
        notify_high_mortality(instance.user, instance)


# ======================== Large Sale Handler ========================
@receiver(post_save, sender=LivestockActivity)
def check_large_sale(sender, instance, created, **kwargs):
    if created and instance.action.lower() == "sold":
        notify_large_sale(instance.user, instance)


# ======================== High Expense Handler ========================
@receiver(post_save, sender=FeedActivity)
def check_high_expense_from_feed(sender, instance, created, **kwargs):
    if created and instance.action.lower() == "bought":
        notify_high_expense(instance.user, instance)


@receiver(post_save, sender=LivestockActivity)
def check_high_expense_from_livestock(sender, instance, created, **kwargs):
    if created and instance.action.lower() == "added":
        notify_high_expense(instance.user, instance)
