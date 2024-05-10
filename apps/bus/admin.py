from django.contrib import admin
from .models import BusRoute, BusStop

admin.site.register(BusRoute)
admin.site.register(BusStop)