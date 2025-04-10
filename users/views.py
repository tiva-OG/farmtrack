from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

import random

from .models import ShortenedLink, OTP
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    OnboardingSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)


User = get_user_model()

# Simple Backend Health Check View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    print("DEBUGGING CSRF ERROR")
    return JsonResponse({"status": "ok", "message": "Backend is LIVE!"})





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

            send_mail(
                subject="Verify your FarmTrack Account",
                message=f"""
                Hi {user.email},

                Thanks for signing up for FarmTrack!

                To activate your account, please use the OTP below:
                Your OTP: [{otp_code}]

                This code is valid for 5 minutes.

                If you didn't request this, please ignore this message contact our support team at {settings.SUPPORT_EMAIL}

                Best regards,
                Farm Track Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response(
                {"message": "OTP sent to email"},
                status=status.HTTP_201_CREATED,
            )

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

            # generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/password-reset/confirm/{uid}/{token}/"

            # create short link
            short_link = ShortenedLink.objects.create(original_url=reset_url)
            short_url = f"{settings.FRONTEND_URL}/password-reset/{short_link.short_code}/"

            # send email
            subject = "Password Reset Request"
            message = f"""
            <p>Dear {user.first_name},</p>
            <br />
            <p>We received a request to reset your password for your Farm Track account. If you did not request this, please ignore this email.</p>
            <p>To reset your password, click the button below:</p>
            <br />
            👉  <a href="{short_url}" style="background:#28a745;color:#ffffff;padding:10px 20px;border-radius:5px;text-decoration:none;">Reset Password</a>
            <br />
            <br />
            <p>This link will expire in 24 hours for security reasons.</p>
            <p>If you have any questions, feel free to contact our support team at {settings.SUPPORT_EMAIL}.</p>
            <br />
            <p>Best regards,</p>
            <p>Farm Track Team</p>
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            email = EmailMultiAlternatives(subject, message, from_email, to_email)
            email.attach_alternative(message, "text/html")
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


def short_link_redirect(request, short_code):
    link = get_object_or_404(ShortenedLink, short_code=short_code)
    return HttpResponseRedirect(link.original_url)


# logout view to blacklist token if necessary
@api_view(["POST"])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # blacklist the refresh token
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import OTP
import random
from datetime import timedelta

User = get_user_model()


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

        send_mail(
            subject="Resend OTP - FarmTrack Account Verification",
            message=f"""
            Hi {user.email},
            
            Thanks for signing up for FarmTrack!
            
            To activate your account, please use the OTP below:

            Your OTP: [{otp_code}]

            This code is valid for 5 minutes.

            If you didn't request this, please ignore this message contact our support team at {settings.SUPPORT_EMAIL}

            Best regards,
            Farm Track Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"message": "A new OTP has been sent to your email."}, status=status.HTTP_200_OK)


# some api endpoints to include:
# - update user details
# - delete user?
# - list all user? `admin only`
