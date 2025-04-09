from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.profile_url = reverse("profile")

        self.user_data = {"email": "test@user.com", "farm_name": "Test Farm", "password": "test_password"}
        self.default_values = {"first_name": "Dew", "last_name": "Tee", "livestock_type": "Fish", "low_stock_threshold": 10}

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
