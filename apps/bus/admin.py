from django.contrib import admin
from .models import BusRoute, BusStop, BusChat

admin.site.register(BusRoute)
admin.site.register(BusStop)
admin.site.register(BusChat)