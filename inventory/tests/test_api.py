from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from inventory.models import Feed, Livestock


class FeedAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@user.com", farm_name="Test User", password="test_word")
        self.feed = Feed.objects.create(quantity=4.1, cost=35000, farmer=self.user)

    def test_get_feed_list(self):
        """test API endpoints to fetch feed list"""
        # self.client.force_login(self.user)
        # response = self.client.get(reverse("feed-list"))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)
        # self.assertEqual(response.data[0]["action"], "Bought")
        pass

    # def test_add_feed_item(self):
    #     """test adding a new feed item via API"""
    #     response = self.client.post(reverse("feed-list"), {"action": "Consumed", "quantity": 1.65}, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertTrue(Feed.objects.filter(action="Consumed").exists())
