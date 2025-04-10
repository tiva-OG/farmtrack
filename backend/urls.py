from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("sales_expenses.urls")),
    path("api/auth/", include("rest_framework.urls")),
    path("api/inventory/", include("inventory.urls")),
    path("api/info/", include("info.urls")),
]
