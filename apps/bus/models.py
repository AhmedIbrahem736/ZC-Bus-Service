from django.db import models
from apps.users.models import User
from apps.base.models import CustomBaseModel
from django.utils.translation import gettext_lazy as _


class BusRoute(CustomBaseModel):
    destination = models.CharField(max_length=100, unique=True, blank=False)
    code = models.CharField(max_length=50, unique=True)
    driver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bus_routes')
    capacity = models.IntegerField(default=0)
    plate_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.destination
    

class BusStop(CustomBaseModel):
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=255, blank=False)
    map_location = models.CharField(max_length=255)
    departure_time = models.TimeField(_("Departure Time"))
    arrival_time = models.TimeField(_("Arrival Time"))
    bus_route = models.ForeignKey(BusRoute, on_delete=models.PROTECT, related_name='bus_stops')

    def __str__(self):
        return self.name