from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username
    """

    def create_user(self, email, farm_name, password=None, **kwargs):
        """
        Create and save a user with the given email, farm_name and password.
        """

        if not email:
            raise ValueError(_("Email is required"))
        if not farm_name:
            raise ValueError(_("Farm name is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, farm_name=farm_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, farm_name, password, **kwargs):
        """
        Create and save a SuperUser with the given email, farm_name and password.
        """

        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, farm_name, password, **kwargs)
