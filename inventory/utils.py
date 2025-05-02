from .models import FeedActivity, LivestockActivity


def set_initial_inventory(user, livestock_data, feed_data):
    if feed_data:
        for item in feed_data:
            FeedActivity.objects.create(
                user=user,
                name=item["name"],
                action="initial",
                quantity=item["quantity"],
                cost=item.get("cost", 0),
                is_locked=True,
            )

    if livestock_data:
        for item in livestock_data:
            LivestockActivity.objects.create(
                name=item["name"],
                action="initial",
                quantity=item["quantity"],
                cost=item.get("cost", 0),
                is_locked=True,
                user=user,
            )
