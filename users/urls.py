from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserViewSet,
    RegisterView,
    OnboardingView,
    VerifyOTPView,
    ResendOTPView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    short_link_redirect,
)


router = DefaultRouter()
router.register(r"user", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token-refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("otp-resend/", ResendOTPView.as_view(), name="resend_otp"),
    path("otp-verify/", VerifyOTPView.as_view(), name="verify_otp"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("onboarding/", OnboardingView.as_view(), name="onboarding"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/<str:short_code>/", short_link_redirect, name="short_link_redirect"),
    # path("logout/", logout_view, name="logout"),
]
