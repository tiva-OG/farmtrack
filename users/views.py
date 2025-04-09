from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import ShortenedLink
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    OnboardingSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)


User = get_user_model()


# REGISTER USER
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User created successfully. Proceeding to onboarding.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# some api endpoints to include:
# - update user details
# - delete user?
# - list all user? `admin only`
