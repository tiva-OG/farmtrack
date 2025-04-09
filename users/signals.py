from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

from .models import User


@receiver(post_delete, sender=User)
def delete_associated_file(sender, instance, **kwargs):
    """delete image from filesystem  if it exists"""

    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
