from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("sales.urls")),
    path("api/", include("expenses.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/inventory/", include("inventory.urls")),
    path("api/farmlytics/", include("farmlytics.urls")),
    path("api/notifications/", include("notifications.urls")),
]
