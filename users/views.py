from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import EmailMultiAlternatives, send_mail

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

import random
from datetime import datetime, timedelta

from .custom_token_generator import CustomTokenGenerator
from .models import OTP
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    OnboardingSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)


User = get_user_model()
token_generator = CustomTokenGenerator()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User logged in successfully.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "is_onboarded": user.is_onboarded,
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid login credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# REGISTER USER
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp_code = f"{random.randint(1000, 9999)}"
            expires_at = timezone.now() + timedelta(minutes=5)
            OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)

            subject = ("Verify your FarmTrack Account",)
            from_email = (settings.DEFAULT_FROM_EMAIL,)
            to_email = [user.email]

            context = {
                "user": user,
                "otp_code": otp_code,
                "current_year": datetime.now().year,
            }

            html_content = render_to_string("emails/otp.html", context)
            text_content = (
                "This email contains information to activate your FarmTrack account. Please view in an HTML-compatible client."
            )

            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("otp")

        if not email or not code:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp_record = OTP.objects.filter(user=user, code=code, is_used=False).last()

        if not otp_record:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.is_expired():
            return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        otp_record.is_used = True
        otp_record.save()

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Account verified. Proceeding to onboarding.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


# COMPLETE USER ONBOARDING
class OnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = OnboardingSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Onboarding complete."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET or UPDATE USER PROFILE
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [
                AllowAny(),
            ]
        return super().get_permissions()

    @action(detail=False, methods=["GET", "PUT", "PATCH"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user  # get currently logged user

        if request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User profile updated.", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        return Response({"message": "User profile retrieved.", "data": serializer.data}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/password-reset/confirm/{uid}/{token}/"

            # send email
            subject = "Password Reset Request"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            context = {
                "user": user,
                "reset_url": reset_url,
                "settings": settings,
                "current_year": datetime.now().year,
            }

            html_content = render_to_string("emails/password_reset.html", context)
            text_content = "This email contains information to reset your FarmTrack account password. Please view in an HTML-compatible client."

            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({"message": "Password reset link sent to email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({"message": "Account already verified."}, status=status.HTTP_400_BAD_REQUEST)

        # Invalidate previous OTPs
        OTP.objects.filter(user=user, is_used=False).update(is_used=True)

        otp_code = f"{random.randint(1000, 9999)}"
        expires_at = timezone.now() + timedelta(minutes=5)
        OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)

        subject = ("Verify your FarmTrack Account",)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]

        context = {
            "user": user,
            "otp_code": otp_code,
            "current_year": datetime.now().year,
        }

        html_content = render_to_string("emails/otp.html", context)
        text_content = (
            "This email contains information to activate your FarmTrack account. Please view in an HTML-compatible client."
        )

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message": "A new OTP has been sent to your email."}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# some api endpoints to include:
# - update user details
# - delete user?
# - list all user? `admin only`
