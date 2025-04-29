from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    User model manager with email as the unique identifier for authentication instead of username
    """

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(_("Email is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("role", "admin")

        return self.create_user(email, password, **kwargs)
