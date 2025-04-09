from django.test import TestCase
from datetime import date
from users.models import User
from inventory.models import Feed, Livestock


class FeedModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """create test data once for the class"""
        user = User.objects.create(email="test@mail.com", farm_name="Test Farm")
        cls.feed = Feed.objects.create(name="Bird Feed", action="Bought", quantity=10.5, cost=15000, farmer=user)

    def test_feed_creation(self):
        """check if Feed object is created correctly"""
        self.assertEqual(self.feed.name, "Bird Feed")
        self.assertEqual(self.feed.action, "Bought")
        self.assertEqual(self.feed.quantity, 10.5)
        self.assertEqual(self.feed.cost, 15000)

    def test_feed_str_method(self):
        """test the __str__ method of the Feed model"""
        self.assertEqual(str(self.feed), f"Bought 10.5kg of Bird Feed worth ₦15000 on {date.today()}")

    def test_feed_when_cost_is_null_or_blank(self):
        self.feed.cost = None
        self.feed.action = "Consumed"

        self.assertEqual(self.feed.cost, None)
        self.assertEqual(str(self.feed), f"Consumed 10.5kg of Bird Feed on {date.today()}")

    def test_feed_default_values(self):
        default_user = User.objects.create(email="default@user.com", farm_name="Default Farm")
        default_feed = Feed.objects.create(quantity=1.7, farmer=default_user)

        self.assertEqual(default_feed.name, "Fish Feed")
        self.assertEqual(default_feed.action, "Bought")
        self.assertEqual(default_feed.cost, None)
        self.assertEqual(default_feed.entry_date, date.today())


class LivestockModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="test@mail.com", farm_name="Test Farm")
        cls.livestock = Livestock.objects.create(name="Bird", action="Sold", quantity=8, cost=30000, farmer=user)

    def test_livestock_creation(self):
        self.assertEqual(self.livestock.name, "Bird")
        self.assertEqual(self.livestock.action, "Sold")
        self.assertEqual(self.livestock.quantity, 8)
        self.assertEqual(self.livestock.cost, 30000)
