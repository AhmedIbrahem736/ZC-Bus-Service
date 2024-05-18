from django.db import models
from apps.users.models import User
from apps.base.models import CustomBaseModel
from django.utils.translation import gettext_lazy as _


class SemesterChoices(models.TextChoices):
    FALL = 'Fall'
    SPRING = 'Spring'
    SUMMER = 'Summer'


class BusOffering(CustomBaseModel):
    semester = models.CharField(max_length=20, choices=SemesterChoices.choices, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    subscription_amount = models.DecimalField(max_digits=10, decimal_places=3, null=False)


class BusRoute(CustomBaseModel):
    destination = models.CharField(max_length=100, unique=True, blank=False)
    code = models.CharField(max_length=50, unique=True)
    driver = models.OneToOneField(User, on_delete=models.PROTECT, related_name='bus_route')
    capacity = models.IntegerField(default=0)
    plate_number = models.CharField(max_length=20, unique=True)
    bus_offering = models.ForeignKey(BusOffering, on_delete=models.PROTECT, related_name='bus_routes')

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


class BusSubscription(CustomBaseModel):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bus_subscriptions')
    bus_route = models.ForeignKey(BusRoute, on_delete=models.PROTECT, related_name='bus_subscriptions')
