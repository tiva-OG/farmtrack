from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from datetime import timedelta

from .serializers import CustomTokenObtainSerializer, OnboardUserSerializer, RegisterUserSerializer, UserSerializer

User = get_user_model()


# ========================================== Register user ==========================================
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data
        serializer = RegisterUserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()

            # Implement 2FA Logic
            user.is_active = True  # this should come in onboarding i.e. after 2FA
            user.save()

            return Response({"detail": "OTP sent to email 'Please proceed to onboarding'"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================== Onboard user ==========================================
class OnboardUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        user_data = request.data
        serializer = OnboardUserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Onboarding complete."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================== Get & Update user profile ==========================================
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=["GET", "PUT", "PATCH"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user

        if request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ========================================== Login and get access & refresh tokens ==========================================
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get("refresh")
        cookie_max_age = 3600 * 24 * 1  # 1 day
        expires = timezone.now() + timedelta(seconds=cookie_max_age)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="Lax",
            secure=False,  # set to True in production
            expires=expires,
        )
        # remove refresh from the response body
        response.data.pop("refresh", None)

        return response


# ========================================== Refresh access token ==========================================
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"detail": "Refresh token not found in cookie"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # get user to include email in response
            user = User.objects.get(id=refresh["user_id"])
            response = Response({"access": access_token, "email": user.email}, status=status.HTTP_200_OK)

            return response

        except TokenError as e:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


# ========================================== Logout user ==========================================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("refresh_token")

        return response
