from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from faker import Faker
from users.models import User


class TestSetup(APITestCase):

    def setUp(self):
        self.feed_list_url = "feed-list"
        self.feed_update_url = "feed-update"
        self.feed_delete_url = "feed-delete"
        self.livestock_list_url = "livestock-list"
        self.livestock_update_url = "livestock-update"
        self.livestock_delete_url = "livestock-delete"

        self.user_data = {"email": "test@user.com", "farm_name": "Test Farm", "password": "test_password"}
        self.feed_data = {"name": "Bird Feed", "action": "Bought", "quantity": 10.7, "cost": 20000}
        self.livestock_data = {"name": "Fish", "action": "Consumed", "quantity": 5, "cost": 45000}

        self.user = User.objects.create_user(**self.user_data)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
