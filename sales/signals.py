from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from inventory.models import LivestockActivity
from .models import Sale


@receiver(post_save, sender=LivestockActivity)
def update_or_create_sale_from_activity(sender, instance, **kwargs):
    if instance.action == "Sold":
        sale, created = Sale.objects.update_or_create(
            livestock_activity=instance,
            defaults={
                "user": instance.user,
                "name": instance.name,
                "quantity": instance.quantity,
                "revenue": instance.cost,
            },
        )
    else:  # if action has changed from 'Sold', delete the sale
        Sale.objects.filter(livestock_activity=instance).delete()


@receiver(pre_delete, sender=LivestockActivity)
def delete_sale_from_activity(sender, instance, **kwargs):
    Sale.objects.filter(livestock_activity=instance).delete()
