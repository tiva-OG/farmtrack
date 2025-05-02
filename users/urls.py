from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView, OnboardUserView, RegisterUserView, UserViewSet

router = DefaultRouter()
router.register(r"user", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterUserView.as_view(), name="register-user"),
    path("onboard/", OnboardUserView.as_view(), name="onboard-user"),
]
