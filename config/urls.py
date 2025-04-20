from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/inventory/", include("inventory.urls")),
    path("api/", include("sales.urls")),
    path("/", include("expenses.urls")),
]
