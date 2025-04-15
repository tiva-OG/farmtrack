from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "role", "first_name", "last_name", "farm_name", "is_active", "is_staff", "is_superuser")
    list_filter = ("role", "livestock_type")
    search_fields = ("email", "farm_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Farm Info", {"fields": ("farm_name", "livestock_type", "feed_low_stock_threshold")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "farm_name", "livestock_type", "role", "is_staff", "is_superuser"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
