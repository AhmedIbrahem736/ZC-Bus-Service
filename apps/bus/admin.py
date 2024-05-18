from django.contrib import admin
from .models import BusRoute, BusStop, BusSubscription, BusOffering, BusReservation

admin.site.register(BusRoute)
admin.site.register(BusStop)
admin.site.register(BusSubscription)
admin.site.register(BusOffering)
admin.site.register(BusReservation)
