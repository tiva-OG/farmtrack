from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls")),
    path("api/", include("users.urls")),
    path("api/inventory/", include("inventory.urls")),
    path("api/", include("sales_expenses.urls")),
]
