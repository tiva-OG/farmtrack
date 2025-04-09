from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from inventory.models import Feed, Livestock
from .models import SalesExpenses


@receiver(post_save, sender=Feed)
def add_sales_expenses_feed(sender, instance, created, **kwargs):
    if instance.action == "Bought":
        SalesExpenses.objects.update_or_create(
            farmer=instance.farmer,
            item="Feed",
            item_id=instance.id,
            defaults={
                "cost": instance.cost,
                "entry_date": instance.entry_date,
                "record_type": "Expense",
            },
        )


@receiver(post_save, sender=Livestock)
def add_sales_expenses_livestock(sender, instance, created, **kwargs):

    record_type = "Expense" if instance.action in ["Bought", "Dead"] else "Sale"
    SalesExpenses.objects.update_or_create(
        farmer=instance.farmer,
        item="Livestock",
        item_id=instance.id,
        defaults={
            "cost": instance.cost,
            "entry_date": instance.entry_date,
            "record_type": record_type,
        },
    )

    # SalesExpenses.objects.create(
    #     item="Livestock",
    #     item_id=instance.id,
    #     cost=instance.cost,
    #     entry_date=instance.entry_date,
    #     record_type=record_type,
    #     farmer=instance.farmer,
    # )


@receiver(post_save, sender=Feed)
def update_sales_expenses_feed(sender, instance, **kwargs):
    if instance.action == "Bought":
        SalesExpenses.objects.filter(item="Feed", item_id=instance.id).update(cost=instance.cost, entry_date=instance.entry_date)


@receiver(post_delete, sender=Feed)
@receiver(post_delete, sender=Livestock)
def delete_sales_expenses_records(sender, instance, **kwargs):
    SalesExpenses.objects.filter(item=sender.__name__, item_id=instance.id).delete()
