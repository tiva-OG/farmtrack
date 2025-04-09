from rest_framework import status
from django.urls import reverse
from .test_setup import TestSetup
import pdb


class TestViews(TestSetup):

    def test_feed_list(self):
        add_res = self.client.post(reverse(self.feed_list_url), self.feed_data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse(self.feed_list_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.feed_data["name"])
        self.assertEqual(response.data[0]["action"], self.feed_data["action"])
        self.assertEqual(response.data[0]["quantity"], self.feed_data["quantity"])
        self.assertEqual(response.data[0]["cost"], self.feed_data["cost"])

    def test_feed_update(self):
        add_res = self.client.post(reverse(self.feed_list_url), self.feed_data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        response = self.client.put(reverse(self.feed_update_url, kwargs={"pk": add_res.data["id"]}), {"name": "Fish Feed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feed_delete(self):
        add_res = self.client.post(reverse(self.feed_list_url), self.feed_data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(reverse(self.feed_delete_url, kwargs={"pk": add_res.data["id"]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_livestock_list(self):
        add_res = self.client.post(reverse(self.livestock_list_url), self.livestock_data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse(self.livestock_list_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.livestock_data["name"])
        self.assertEqual(response.data[0]["action"], self.livestock_data["action"])
        self.assertEqual(response.data[0]["quantity"], self.livestock_data["quantity"])
        self.assertEqual(response.data[0]["cost"], self.livestock_data["cost"])

    def test_livestock_update(self):
        add_res = self.client.post(reverse(self.livestock_list_url), self.livestock_data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        response = self.client.put(reverse(self.livestock_update_url, kwargs={"pk": add_res.data["id"]}), {"action": "Dead"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_livestock_delete(self):
        add_res = self.client.post(reverse(self.livestock_list_url), self.livestock_data)
        self.assertEqual(add_res.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(reverse(self.livestock_delete_url, kwargs={"pk": add_res.data["id"]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
