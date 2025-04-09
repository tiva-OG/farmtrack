from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.models import User
from .test_setup import TestSetup
import pdb


class TestViews(TestSetup):

    def test_user_cannot_register_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["farm_name"], self.user_data["farm_name"])

    def test_user_can_register_with_default_values(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], self.default_values["first_name"])
        self.assertEqual(response.data["last_name"], self.default_values["last_name"])
        self.assertEqual(response.data["livestock_type"], self.default_values["livestock_type"])
        self.assertEqual(response.data["low_stock_threshold"], self.default_values["low_stock_threshold"])

    def test_user_cannot_access_protected_views_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_access_protected_views_when_authenticated(self):
        self.user = User.objects.create_user(**self.user_data)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        response = self.client.get(self.profile_url)
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
