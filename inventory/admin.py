from django.contrib import admin
from .models import FeedActivity, LivestockActivity

admin.site.register(FeedActivity)
admin.site.register(LivestockActivity)
