from django.db import models
from apps.users.models import User
from apps.base.models import CustomBaseModel
from apps.semester.models import Semester
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.bus.models import BusRoute

class Subscription(CustomBaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    bus_route = models.ForeignKey(BusRoute, on_delete=models.PROTECT)
    class Meta:
        unique_together = ['user', 'semester']

    def __str__(self):
        return f"{self.user} - {self.semester}"