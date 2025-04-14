from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "is_admin", "is_manager", "is_staff")
    list_filter = ("is_admin", "is_manager")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Farm Info", {"fields": ("farm_name", "livestock_type", "feed_low_stock_threshold")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_admin", "is_manager", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide"), "fields": ("email", "password1", "password2", "is_admin", "is_manager", "is_staff")}),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
