from django.db import models
from apps.users.models import User
from apps.base.models import CustomBaseModel

class BusRoute(CustomBaseModel):
    destination = models.CharField(max_length=100, unique=True, blank=False)
    code = models.CharField(max_length=50, unique=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bus_routes', unique=True)
    capacity = models.IntegerField(default=0)
    plate_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.destination