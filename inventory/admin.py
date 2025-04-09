from django.contrib import admin
from inventory.models import Feed, Livestock

admin.site.register([Feed, Livestock])
