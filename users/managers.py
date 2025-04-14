from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    User model manager with email as the unique identifier for authentication instead of username
    """

    def create_user(self, email, farm_name, password=None, **kwargs):
        if not email:
            raise ValueError(_("Email is required"))
        if not farm_name:
            raise ValueError(_("Farm name is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, farm_name=farm_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, farm_name="Admin Farm", password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if not kwargs.get("is_staff"):
            raise ValueError(_("Superuser must 'is_staff=True'"))
        if not kwargs.get("is_superuser"):
            raise ValueError(_("Superuser must 'is_superuser=True'"))
        if not kwargs.get("is_active"):
            raise ValueError(_("Superuser must 'is_active=True'"))

        return self.create_user(email, farm_name, password, **kwargs)
