from .models import Feed, Livestock
from django.utils import timezone


# if user selects `Fish` or `Poultry`, frontend should return
# [{"name": "Fish"...}] -> always return a list of JSON
# if user selects `Both`, frontend should return
# [{"name": "Fish",...}, {"name": "Poultry"}]


def seed_initial_inventory(user, livestock_data, feed_data):
    if livestock_data:
        for item in livestock_data:
            Livestock.objects.create(
                name=item["name"],
                action="Initial",
                quantity=item["quantity"],
                cost=item.get("cost", 0),
                is_locked=True,
                farmer=user,
            )

    if feed_data:
        for item in feed_data:
            Feed.objects.create(
                name=item["name"],
                action="Initial",
                quantity=item["quantity"],
                cost=item.get("cost", 0),
                is_locked=True,
                farmer=user,
            )
